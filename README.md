# Expansão do Modelo Preditivo de Wahbi et al. para LTVTA em Laminopatias

> **Proposta de Inclusão de Fibrose Miocárdica por RMC e Duração do QRS**

**Autores:** Alexandre da Fonseca · Paloma de Almeida Taboada  
**Orientador:** Prof. Argemiro Pentian Junior  
**Instituição:** FATEC Dep. Ary Fossen Jundiaí — Curso de Ciência de Dados  
**Disciplina:** Projeto Integrador III — 5º Semestre (2026)

---

## Sobre o Projeto

Este repositório contém o artigo científico e a análise computacional desenvolvidos como Projeto Integrador III, propondo a **expansão do modelo preditivo de Wahbi et al. (2019)** para risco de Taquiarritmia Ventricular Ameaçadora à Vida (LTVTA) em portadores de mutações no gene **LMNA** (laminopatias).

### Contexto Clínico

Laminopatias são doenças hereditárias causadas por mutações no gene LMNA, com alta incidência de morte súbita cardíaca por taquiarritmias ventriculares. O modelo de Wahbi et al. (2019), baseado em regressão de Fine-Gray com cinco variáveis clínicas, é atualmente a principal ferramenta de estratificação de risco para indicação de cardioversor-desfibrilador implantável (CDI).

### Proposta

O artigo propõe adicionar **duas variáveis** ao modelo original:

| Nova Variável | Justificativa | HR esperado |
|---|---|---|
| **LGE por RMC** — fibrose miocárdica detectada por Ressonância Magnética Cardíaca com Gadolínio | Substrato anatômico para reentrada arrítmica; preditor independente de MSC em cardiomiopatias | 2,0–4,0 |
| **Duração do QRS** — no eletrocardiograma de superfície | Marcador de disfunção do sistema de condução His-Purkinje; reflete mecanismo fisiopatológico distinto do BAV | 1,10–1,30 por 10 ms |

---

## Estrutura do Repositório

```
├── analise_modelo_laminopatias.ipynb          # Notebook principal (análise computacional)
├── dataset_sintetico_laminopatias.csv         # Dataset sintético parametrizado (n=600)
├── Artigo Projeto Integrador 3 - Alexandre_Paloma.docx   # Artigo científico completo
├── relatorio_analise_laminopatias_wahbi.docx  # Relatório de avaliação do orientador
├── wahbi-et-al-2019-(...).pdf                 # Artigo original de Wahbi et al. (referência)
├── fig1_distribuicoes.png                     # Figura 1 — Distribuições das variáveis
├── fig2_prevalencias.png                      # Figura 2 — Prevalências vs. literatura
├── fig3_correlacao.png                        # Figura 3 — Matriz de correlação
├── fig4_desempenho.png                        # Figura 4 — Curvas de incidência por quartil
├── fig5_sensibilidade.png                     # Figura 5 — Análise de sensibilidade dos HR
└── fig6_tornado.png                           # Figura 6 — Contribuição por variável (tornado)
```

---

## Análise Computacional

O notebook `analise_modelo_laminopatias.ipynb` implementa:

### Dataset Sintético
- **600 pacientes** simulados com parâmetros calibrados a partir dos dados de Wahbi et al. (2019) e literatura específica de laminopatias
- Seed fixo (`np.random.seed(42)`) para reprodutibilidade total
- Riscos competidores: LTVTA (~13%), óbito por outras causas (~10%), censurado (~77%)

### Variáveis do dataset

| Coluna | Tipo | Parâmetros de simulação |
|---|---|---|
| `sexo_masculino` | Binária | Prevalência 60% (Wahbi: 58–64%) |
| `mutacao_nao_missense` | Binária | Prevalência 44% |
| `bloqueio_av` | Binária | Prevalência 43% |
| `tvns` | Binária | Prevalência 33% |
| `feve` | Contínua | Normal(48, 11)%, truncada [15, 75] |
| `lge_presente` | Binária | Prevalência 55% (Hasselberg 2014) |
| `lge_pct` | Contínua | % do miocárdio; média ~10% nos LGE+ |
| `duracao_qrs` | Contínua | Normal(115, 28) ms; correlacionada com BAV |
| `tempo_seguimento` | Contínua | Até 5 anos |
| `evento` | Categórica | 0=censurado, 1=LTVTA, 2=óbito competidor |

### Modelos Comparados

| Modelo | Variáveis | C-index |
|---|---|---|
| **Wahbi original** | 5 (sexo, mutação, BAV, TVNS, FEVE) | **0,768** (ref: 0,776) |
| **Modelo Expandido** | 7 (+ LGE + QRS) | **0,794** (+0,026) |

**Hazard Ratios estimados das novas variáveis:**
- LGE presente: **HR = 2,26** (faixa proposta: 2,0–4,0 ✓)
- Duração QRS (por 10 ms): **HR = 1,23** (faixa proposta: 1,10–1,30 ✓)

---

## Como Reproduzir a Análise

### Pré-requisitos

```bash
pip install numpy pandas matplotlib seaborn scipy scikit-survival lifelines
```

### Executar o notebook

```bash
jupyter notebook analise_modelo_laminopatias.ipynb
```

Execute as células em ordem. A **Seção 1** regenera o `dataset_sintetico_laminopatias.csv` e todas as figuras.

> **Nota metodológica:** O modelo de Fine-Gray exato requer a biblioteca `cmprsk` do R. Para comparação do desempenho discriminativo em Python, são utilizados modelos de risco causa-específico de Cox (`CoxPHSurvivalAnalysis` do `scikit-survival`), metodologicamente válidos para comparação relativa de C-index entre modelos na mesma população.

---

## Referências Principais

- **Wahbi K et al.** Development and validation of a new risk prediction score for life-threatening ventricular tachyarrhythmias in laminopathies. *Circulation.* 2019;140:293–302.
- **Halliday BP et al.** Outcome in dilated cardiomyopathy related to the extent, location, and pattern of late gadolinium enhancement. *JACC Cardiovasc Imaging.* 2019;12(8):1645–1655.
- **Gulati A et al.** Association of fibrosis with mortality and sudden cardiac death in patients with nonischemic dilated cardiomyopathy. *JAMA.* 2013;309:896–908.
- **Fine JP, Gray RJ.** A proportional hazards model for the subdistribution of a competing risk. *J Am Stat Assoc.* 1999;94:496–509.

---

## Licença

Projeto acadêmico — uso educacional. Os dados clínicos são **sintéticos**, gerados por simulação paramétrica; não representam pacientes reais.
