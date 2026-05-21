# CLAUDE.md — Contexto do Projeto para Sessões Futuras

Este arquivo documenta todo o histórico de trabalho realizado com Claude Code neste projeto. Leia-o integralmente no início de qualquer nova sessão antes de fazer qualquer alteração.

---

## Identificação do Projeto

**Título:** Expansão do Modelo Preditivo de Wahbi et al. para Taquiarritmias Ventriculares em Laminopatias: Proposta de Inclusão de Fibrose Miocárdica por RMC e Duração do QRS

**Autores:** Alexandre da Fonseca · Paloma de Almeida Taboada  
**Orientador:** Prof. Argemiro Pentian Junior  
**Instituição:** FATEC Dep. Ary Fossen Jundiaí — Curso de Ciência de Dados  
**Disciplina:** Projeto Integrador III — 5º Semestre (2026)  
**Repositório GitHub:** https://github.com/alefonsecabb/laminopatias-modelo-preditivo  

---

## Resumo da Proposta do Artigo

O artigo propõe expandir o modelo Fine-Gray de Wahbi et al. (2019) — que estratifica risco de Taquiarritmia Ventricular Ameaçadora à Vida (LTVTA) em portadores de mutações no gene LMNA — adicionando duas variáveis não contempladas no modelo original:

| Nova variável | Tipo | HR hipotético |
|---|---|---|
| LGE por RMC (fibrose miocárdica) | Binária + contínua (% do miocárdio) | 2,0–4,0 |
| Duração do QRS (ECG de superfície) | Contínua (ms) | 1,10–1,30 por 10 ms |

**Modelo original de Wahbi et al.:** 5 variáveis (sexo masculino, mutação não-missense LMNA, BAV, TVNS, FEVE), C-index 0,776 (derivação) / 0,800 (validação).

---

## Estrutura de Arquivos Atual

```
PROJETO_INTEGRADOR_III/
├── CLAUDE.md                                          ← este arquivo
├── README.md                                          ← documentação do repositório
├── .gitignore                                         ← exclui _BACKUP.docx, __pycache__, .claude/
│
├── analise_modelo_laminopatias.ipynb                  ← notebook Python completo (7 seções)
├── dataset_sintetico_laminopatias.csv                 ← dataset sintético n=600
│
├── fig1_distribuicoes.png                             ← EDA: distribuições das variáveis
├── fig2_prevalencias.png                              ← EDA: prevalências vs. literatura
├── fig3_correlacao.png                                ← EDA: matriz de correlação
├── fig4_desempenho.png                                ← curvas de incidência por quartil
├── fig5_sensibilidade.png                             ← análise de sensibilidade dos HR
├── fig6_tornado.png                                   ← contribuição por variável (tornado)
│
├── Artigo Projeto Integrador 3  - Alexandre_Paloma.docx        ← versão com correções intermediárias
├── Artigo Projeto Integrador 3  - Alexandre_Paloma_BACKUP.docx ← backup antes das correções (excluído do git)
├── Artigo Projeto Integrador 3  - Alexandre_Paloma_FINAL.docx  ← versão com todas as correções (sem seção 4.4)
├── Artigo Projeto Integrador 3  - Alexandre_Paloma_FINAL_v2.docx ← VERSÃO MAIS ATUALIZADA (com seção 4.4)
│
├── relatorio_analise_laminopatias_wahbi.docx          ← relatório de avaliação do orientador
└── wahbi-et-al-2019-(...).pdf                         ← artigo original de Wahbi et al. (referência)
```

> **Arquivo canônico do artigo:** `Artigo Projeto Integrador 3  - Alexandre_Paloma_FINAL_v2.docx`

---

## Histórico de Trabalho Realizado

### 1. Dataset Sintético (`dataset_sintetico_laminopatias.csv`)

**Criado em maio/2026.** 600 pacientes simulados com `np.random.seed(42)`.

**Colunas:**

| Coluna | Tipo | Parâmetros de simulação |
|---|---|---|
| `id_paciente` | int | 1–600 |
| `sexo_masculino` | binária | prevalência 60% |
| `mutacao_nao_missense` | binária | prevalência 44% |
| `bloqueio_av` | binária | prevalência 43% |
| `tvns` | binária | prevalência 33% |
| `feve` | contínua | Normal(48, 11)%, truncada [15, 75] |
| `lge_presente` | binária | prevalência 55% |
| `lge_pct` | contínua | 0 se lge=0; Beta(2,6)×35 se lge=1 (média ≈10%) |
| `duracao_qrs` | contínua | Normal(115, 28) ms, truncada [80, 220], correlacionada com BAV |
| `tempo_seguimento` | contínua | até 5 anos (Weibull + 5% perda aleatória) |
| `evento` | categórica | 0=censurado, 1=LTVTA, 2=óbito competidor |

**Taxas de eventos:** ~12,8% LTVTA (evento=1), ~9,5% óbito competidor (evento=2), ~77,7% censurado.

**Calibração:** LAMBDA_LTVTA=0,001812 (calibrado via `scipy.optimize.brentq` para 18% LTVTA em 5 anos). LAMBDA_DEATH=0,0256.

**Coeficientes de simulação (log-SHR):**
- sexo_masculino: β = 0,888
- mutacao_nao_missense: β = 0,932
- bloqueio_av: β = 1,054
- tvns: β = 1,011
- feve (por 10%): β = −0,444
- lge_presente: β = 0,916
- duracao_qrs (por 10 ms): β = 0,182

---

### 2. Notebook de Análise (`analise_modelo_laminopatias.ipynb`)

**Criado em maio/2026.** Executa sem erros localmente e no Google Colab.

**Link Colab:** https://colab.research.google.com/drive/1VNMpUuOhFXHxijGW3hS_2do3I1Wfg67v?usp=sharing

**Seções:**
- Seção 0: Setup e imports (`numpy`, `pandas`, `matplotlib`, `seaborn`, `scipy`, `scikit-survival`, `lifelines`)
- Seção 1: Geração e exportação do dataset sintético
- Seção 2: EDA (distribuições, prevalências, correlações, incidência cumulativa) → gera fig1–fig3
- Seção 3: Modelo Wahbi original (5 variáveis) com `CoxPHSurvivalAnalysis`
- Seção 4: Modelo expandido (7 variáveis)
- Seção 5: Comparação (C-index, NRI, curvas por quartil) → gera fig4
- Seção 6: Análise de sensibilidade (variar HR_LGE e HR_QRS) → gera fig5–fig6
- Seção 7: Conclusões para o artigo

**Resultados obtidos:**
- C-index Wahbi (5 vars): **0,768** (ref. literatura: 0,776 ✓)
- C-index Expandido (7 vars): **0,794** (+0,026)
- HR LGE estimado: **2,26** (faixa hipotética 2,0–4,0 ✓)
- HR QRS/10ms estimado: **1,23** (faixa hipotética 1,10–1,30 ✓)
- C-index > 0,82 e NRI ≥ 10%: **não confirmadas** — interpretação: n=77 eventos dá poder limitado, mas melhora é consistente em toda análise de sensibilidade

> **Nota metodológica:** Fine-Gray exato requer `cmprsk` (R). O notebook usa Cox causa-específica (`scikit-survival`) para comparação relativa de C-index — metodologicamente válido para comparação entre modelos na mesma população.

---

### 3. Correções no Artigo Word

Todas aplicadas ao `_FINAL.docx` e mantidas no `_FINAL_v2.docx`:

| # | Correção | Detalhe |
|---|---|---|
| 1 | **Orientador na capa** | Adicionado parágrafo [003]: "Orientador: Prof. Argemiro Pentian Junior" (bold label + normal texto) |
| 2 | **Abstract em inglês** | Inserido após Palavras-Chave [009], com resultados da simulação (C-index 0,794 vs 0,768) |
| 3 | **Keywords em inglês** | Inserido após Abstract [010], em itálico |
| 4 | **Referência [13] corrigida** | Substituída de TRED-HF (Halliday, *Lancet* 2019) para estudo LATE correto: Halliday BP, Baksi AJ, Gulati A et al. *JACC Cardiovasc Imaging.* 2019;12(8):1645–1655 |
| 5 | **Duplicatas removidas** | [12]=Gulati 2013 (duplicata de [5]) e [18]=Shamim 1999 (duplicata de [6]) deletados; referências renumeradas [1]–[22] com remapeamento completo no corpo do texto |
| 6 | **Erro fisiológico do QRS (Seção 3.2)** | Corrigido: removido "quanto tempo leva para encher de sangue e esvaziar"; texto ficou: "O intervalo de tempo necessário para a despolarização elétrica dos ventrículos..." |
| 7 | **Coeficiente β mutação LMNA** | Corrigido na equação de 0,855 para **0,563** (ln(1,76) = 0,5653; 0,855 era o β do BAV 1º grau) |
| 8 | **Cabeçalhos vazios removidos** | 4 parágrafos Heading 1/2 em branco (artefatos de edição) excluídos |
| 9 | **Alinhamento Abstract/Keywords** | Corrigido para JUSTIFY (estava None) |

---

### 4. Seção 4.4 adicionada ao artigo (`_FINAL_v2.docx`)

Inserida após a Seção 4.3 (antes da Seção 5), como `Heading 2` com estilo `Ttulo2` (nome localizado em português do Word).

**Título:** 4.4. Verificação Computacional em Dataset Sintético

**Conteúdo:** 4 parágrafos:
1. Introdução do dataset sintético e do Colab
2. Hiperlink clicável: "Análise Computacional — Expansão do Modelo de Wahbi (Google Colab)" → URL do Colab (azul, sublinhado, relação externa no XML do docx)
3. Instruções de execução: Runtime → Run all, sem instalação local
4. Resultados: C-index 0,794 vs 0,768; HR LGE=2,26; HR QRS=1,23/10ms

---

### 5. Repositório GitHub

- **URL:** https://github.com/alefonsecabb/laminopatias-modelo-preditivo
- **Usuário:** alefonsecabb
- **Branch:** main
- **Credenciais:** armazenadas no Windows Credential Manager para `github.com`
- **Remote:** `https://github.com/alefonsecabb/laminopatias-modelo-preditivo.git`

**Commits publicados:**
1. `256667a` — Inicialização com todos os arquivos do projeto
2. `69a7ff9` — Adição do `_FINAL.docx` (com todas as correções)
3. `3657f1d` — Adição do `_FINAL_v2.docx` (com seção 4.4 + link Colab)

---

## Pendências e Pontos de Atenção

- O arquivo `_FINAL.docx` e o `_FINAL_v2.docx` coexistem. **O canônico é o `_v2`**. Em sessões futuras, consolidar em um único arquivo final se necessário.
- O arquivo `_BACKUP.docx` está excluído do git pelo `.gitignore` (não rastrear).
- A pasta `.claude/` (settings locais) também está excluída do git.
- As hipóteses de C-index > 0,82 e NRI ≥ 10% **não foram confirmadas** na simulação sintética — isso está documentado como limitação do poder amostral (n=77 eventos). Não alterar o texto das hipóteses na Seção 4.2.
- O estilo Heading 2 no docx usa o nome interno `Ttulo2` (localização PT-BR do Word), não `Heading2`. Usar sempre `Ttulo2` ao manipular via python-docx.
- Para editar o Word via python-docx com este caminho (contém `º`), copiar o arquivo para um diretório sem caracteres especiais, editar, e salvar de volta.

---

## Dependências Python

```bash
pip install numpy pandas matplotlib seaborn scipy scikit-survival lifelines python-docx
```

Para executar com SSL restrito (redes corporativas):
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org <pacote>
```
