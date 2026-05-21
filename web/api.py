from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

# Coeficientes estimados pelo modelo Cox causa-específico (Seções 3 e 4 do notebook)
COEFS_WAHBI = {
    'sexo_masculino':       0.878,
    'mutacao_nao_missense': 0.903,
    'bloqueio_av':          1.199,
    'tvns':                 0.954,
    'feve':                -0.030,  # por 1% de FEVE
}

COEFS_EXPANDIDO = {
    'sexo_masculino':       1.011,
    'mutacao_nao_missense': 0.908,
    'bloqueio_av':          0.950,
    'tvns':                 0.966,
    'feve':                -0.033,  # por 1% de FEVE
    'lge_presente':         0.815,
    'duracao_qrs':          0.021,  # por 1 ms de QRS
}

# Médias populacionais da coorte simulada (n=600)
MEDIAS = {
    'sexo_masculino':       0.582,
    'mutacao_nao_missense': 0.443,
    'bloqueio_av':          0.425,
    'tvns':                 0.322,
    'feve':                48.0,
    'lge_presente':         0.548,
    'duracao_qrs':        115.0,
}

# Incidência cumulativa de LTVTA em 5 anos para o paciente médio: 12,8%
P_LTVTA_MEDIA = 0.128


def calcular_sobrevida_basal(coefs: dict) -> float:
    """Estima S0(5) tal que 1 - S0(5)^exp(LP_médio) = P_LTVTA_MEDIA."""
    lp_medio = sum(coefs[k] * MEDIAS[k] for k in coefs)
    s0 = (1.0 - P_LTVTA_MEDIA) ** (1.0 / math.exp(lp_medio))
    return s0


def prever_risco(coefs: dict, dados_paciente: dict) -> float:
    """Retorna risco de LTVTA em 5 anos (0–1) via modelo de Cox."""
    lp = sum(coefs[k] * dados_paciente[k] for k in coefs)
    s0 = calcular_sobrevida_basal(coefs)
    risco = 1.0 - s0 ** math.exp(lp)
    return max(0.0, min(1.0, risco))


def categorizar_risco(risco_pct: float) -> dict:
    if risco_pct < 5.0:
        return {'nivel': 'baixo', 'cor': '#2E7D32', 'label': 'Baixo Risco', 'icone': '●'}
    elif risco_pct < 15.0:
        return {'nivel': 'intermediario', 'cor': '#F57C00', 'label': 'Risco Intermediário', 'icone': '●'}
    else:
        return {'nivel': 'alto', 'cor': '#C62828', 'label': 'Alto Risco', 'icone': '●'}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/prever', methods=['POST'])
def prever():
    dados = request.get_json(force=True)

    paciente = {
        'sexo_masculino':       int(bool(dados.get('sexo_masculino', 0))),
        'mutacao_nao_missense': int(bool(dados.get('mutacao_nao_missense', 0))),
        'bloqueio_av':          int(bool(dados.get('bloqueio_av', 0))),
        'tvns':                 int(bool(dados.get('tvns', 0))),
        'feve':                 float(dados.get('feve', 48)),
        'lge_presente':         int(bool(dados.get('lge_presente', 0))),
        'duracao_qrs':          float(dados.get('duracao_qrs', 115)),
    }

    # Validações básicas
    erros = []
    if not (15 <= paciente['feve'] <= 75):
        erros.append('FEVE deve estar entre 15% e 75%')
    if not (80 <= paciente['duracao_qrs'] <= 220):
        erros.append('Duração do QRS deve estar entre 80 ms e 220 ms')
    if erros:
        return jsonify({'erro': ' | '.join(erros)}), 400

    risco_w   = prever_risco(COEFS_WAHBI,     paciente) * 100
    risco_exp = prever_risco(COEFS_EXPANDIDO, paciente) * 100

    return jsonify({
        'wahbi': {
            'risco':    round(risco_w, 1),
            'categoria': categorizar_risco(risco_w),
        },
        'expandido': {
            'risco':    round(risco_exp, 1),
            'categoria': categorizar_risco(risco_exp),
        },
        'delta': round(risco_exp - risco_w, 1),
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
