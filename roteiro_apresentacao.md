# Roteiro da Apresentação — 15 minutos
**Expansão do Modelo Preditivo para Taquiarritmias Ventriculares em Laminopatias**

---

## Slide 1 — Capa `[0:00 – 0:30]`

> "Bom dia/Boa tarde a todos. Meu nome é Alexandre, e hoje vou apresentar o trabalho que desenvolvemos junto à Paloma no Projeto Integrador III, mas sob a ótica de Aprendizado de Máquina.
> O título é um pouco técnico, então vou começar explicando o problema clínico por trás disso."

---

## Slide 2 — O que são Laminopatias? `[0:30 – 2:00]`

> "Laminopatias são doenças genéticas causadas por mutações no gene LMNA. Esse gene codifica proteínas estruturais do núcleo celular, e quando ele está alterado, o coração é um dos órgãos mais afetados.
>
> O principal risco nessas pessoas é desenvolver uma arritmia ventricular grave — chamamos de LTVTA, ou Taquiarritmia Ventricular Ameaçadora à Vida. Isso inclui taquicardia ventricular sustentada, fibrilação ventricular, ou morte súbita.
>
> A incidência acumulada em 5 anos chega a 18% nos portadores de mutação LMNA — ou seja, quase 1 em cada 5 pacientes.
>
> A principal forma de prevenção é o cardiodesfibrilador implantável, o CDI. Mas ele é caro, invasivo, e nem todo paciente precisa. Por isso, precisamos de modelos que identifiquem quem realmente tem alto risco."

---

## Slide 3 — Modelo de Wahbi et al. `[2:00 – 3:30]`

> "Em 2019, Wahbi e colaboradores publicaram o primeiro modelo de estratificação de risco específico para laminopatias. É um modelo de regressão de riscos competidores — chamado de Fine-Gray — que compete dois desfechos: o evento de interesse, que é a LTVTA, e o óbito por outra causa.
>
> O modelo usa 5 variáveis: sexo masculino, tipo de mutação, bloqueio atrioventricular, taquicardia ventricular não-sustentada e fração de ejeção do ventrículo esquerdo.
>
> O desempenho é bom — C-index de 0,776 na derivação e 0,800 na validação externa. C-index é como uma AUC para dados de sobrevivência: 1,0 é perfeito, 0,5 é aleatório.
>
> Mas existe uma lacuna: duas variáveis importantes clinicamente não estão no modelo. É aí que entra nossa proposta."

---

## Slide 4 — Nossa Proposta `[3:30 – 5:00]`

> "Propomos adicionar duas variáveis ao modelo de Wahbi.
>
> A primeira é o LGE — Late Gadolinium Enhancement — detectado por Ressonância Magnética Cardíaca. O LGE indica fibrose miocárdica, que é justamente o substrato para reentrada elétrica e arritmias. Nossa hipótese é que a presença de LGE multiplica o risco entre 2 e 4 vezes.
>
> A segunda é a duração do QRS no ECG de superfície. O QRS representa o tempo de despolarização elétrica dos ventrículos — quando ele está alargado, indica distúrbio de condução que se associa a disfunção elétrica e mecânica. Nossa hipótese é que cada 10 milissegundos a mais de QRS aumenta o risco entre 10 e 30%.
>
> Para testar essa hipótese sem acesso a dados clínicos reais, usamos dados sintéticos parametrizados."

---

## Slide 5 — Dataset Sintético `[5:00 – 6:30]`

> "Geramos 600 pacientes simulados com NumPy, usando seed fixo para reprodutibilidade.
>
> Os parâmetros foram calibrados diretamente da coorte de Wahbi — prevalências das variáveis, médias e desvios padrão das contínuas, e as taxas de eventos. Usamos a distribuição de Weibull para simular o tempo até o evento, com dois riscos competidores.
>
> Calibramos automaticamente a taxa base usando otimização numérica — a função brentq do SciPy — para que a incidência acumulada em 5 anos de LTVTA ficasse em 18%, tal qual na coorte original.
>
> O resultado foi 77 eventos de LTVTA em 600 pacientes — 12,8% — com tempo médio de seguimento de 4,3 anos.
>
> Todos os coeficientes de simulação foram derivados dos logaritmos dos Hazard Ratios da literatura."

---

## Slide 6 — Análise Exploratória `[6:30 – 7:30]`

> "Antes de ajustar os modelos, validamos se o dataset sintético reproduz as características da coorte de Wahbi.
>
> Neste gráfico vocês veem as prevalências das variáveis binárias comparadas com as faixas de referência da literatura — representadas pelas barras de erro. Todas as variáveis ficaram dentro das faixas esperadas, o que valida que nosso dataset é uma representação plausível da população real.
>
> Fizemos o mesmo para as variáveis contínuas — FEVE, percentual de fibrose e duração do QRS — com distribuições calibradas e verificadas."

---

## Slide 7 — Modelo de ML `[7:30 – 9:00]`

> "Para a modelagem, usamos regressão de Cox causa-específica, implementada com a biblioteca scikit-survival do Python — especificamente a classe CoxPHSurvivalAnalysis.
>
> Por que não o modelo Fine-Gray exato como Wahbi? O Fine-Gray exato requer o pacote cmprsk do R. A Cox causa-específica é metodologicamente válida para comparação relativa de C-index dentro da mesma população — e esse é nosso objetivo: comparar os dois modelos na mesma coorte, não estimar probabilidades absolutas para um novo paciente.
>
> Para avaliação, usamos o C-index de Harrell — que mede a capacidade do modelo de ordenar pacientes do menor para o maior risco. E o NRI, ou Net Reclassification Index, que mede quantos pacientes foram classificados corretamente para uma categoria de risco diferente ao adicionar as novas variáveis.
>
> Para garantir robustez, também fizemos análise de sensibilidade variando os coeficientes das novas variáveis dentro das faixas hipotéticas."

---

## Slide 8 — Fine-Gray vs. Cox Causa-Específica `[9:00 – 10:30]`

> "Antes de mostrar os resultados, quero dedicar um minuto para explicar uma escolha metodológica importante — a diferença entre os dois modelos de sobrevivência que existem para riscos competidores.
>
> O modelo de Wahbi usa o Fine-Gray, que modela diretamente a probabilidade acumulada de LTVTA — tecnicamente chamada de Função de Incidência Cumulativa. O truque do Fine-Gray é que pacientes que morreram por outra causa continuam no conjunto de risco matematicamente, com peso decrescendo a zero. Isso parece estranho, mas garante que a probabilidade estimada reflita o risco real na população.
>
> Já na Cox causa-específica, que é o que usamos, quando um paciente morre de outra causa ele simplesmente sai do conjunto de risco — é tratado como uma censura. A pergunta que esse modelo responde é: quais fatores aumentam a taxa de LTVTA entre os que ainda estão vivos?
>
> A diferença prática: Fine-Gray é superior para prever risco absoluto — 'qual a chance deste paciente ter LTVTA em 5 anos?'. Cox causa-específica é melhor para entender etiologia — 'quais variáveis aumentam a taxa do evento?'.
>
> E por que usamos Cox aqui? Porque nosso objetivo é comparar dois modelos na mesma coorte, não estimar probabilidade absoluta. O C-index mede apenas a capacidade de ordenar pacientes do menor para o maior risco — e essa ordenação é praticamente equivalente entre os dois métodos na mesma população. Fine-Gray exato exigiria o pacote cmprsk do R, que não tem equivalente direto em Python."

---

## Slide 9 — Resultados: Hazard Ratios `[10:30 – 12:00]`

> "Aqui estão os Hazard Ratios estimados pelos modelos. Nas três primeiras colunas, vemos os HRs do modelo de referência Wahbi, do nosso modelo original replicado e do modelo expandido com as duas novas variáveis.
>
> Os HRs das variáveis originais ficaram em faixas muito próximas às do Wahbi — o que valida a calibração do dataset.
>
> E as novas variáveis: LGE presente estimou HR de 2,26 — dentro da nossa hipótese de 2 a 4. E QRS estimou HR de 1,23 por 10 milissegundos — dentro da hipótese de 1,10 a 1,30.
>
> No gráfico tornado à direita, vocês veem a importância relativa de cada variável no modelo expandido — as barras em vermelho são as novas. LGE tem contribuição comparável ao BAV e à TVNS."

---

## Slide 10 — Resultados: Desempenho `[11:30 – 13:00]`

> "Em termos de desempenho discriminativo, o modelo expandido atingiu C-index de 0,794 contra 0,768 do modelo original — ganho de 0,026 pontos.
>
> O NRI total foi de positivo 2,6%, com melhora na reclassificação de não-eventos — pacientes de baixo risco foram corretamente reclassificados para baixo risco pelo modelo expandido.
>
> Nos gráficos, vocês veem as curvas de incidência cumulativa estratificadas por quartil de pontuação de risco. O modelo expandido mostra separação mais clara entre os quartis Q1 e Q4 — pacientes de baixo e alto risco."

---

## Slide 11 — Análise de Sensibilidade `[13:00 – 14:00]`

> "Para verificar robustez, variamos o HR do LGE de 2,0 a 4,0, e o HR do QRS de 1,10 a 1,30 por 10 milissegundos. Para cada combinação, recalculamos o C-index.
>
> O resultado é claro: em todos os 100% dos cenários testados, o modelo expandido superou o modelo original. Isso significa que a melhora não depende de um coeficiente específico — é estrutural, com a adição dessas variáveis.
>
> O LGE teve impacto maior que o QRS nos C-indexes — confirmando que a fibrose miocárdica é o preditor mais informativo das duas novas variáveis."

---

## Slide 12 — Limitações `[14:00 – 14:45]`

> "É importante ser transparente sobre as limitações.
>
> Primeiro: são dados sintéticos. Eles replicam parâmetros da literatura, mas não substituem uma coorte clínica real. As hipóteses precisam ser testadas com dados de pacientes.
>
> Segundo: com 77 eventos, o poder amostral é limitado. Por isso, as hipóteses de C-index acima de 0,82 e NRI acima de 10% não foram atingidas — e isso está explicitamente documentado no artigo como limitação, não como falha.
>
> Terceiro: usamos Cox causa-específica em vez de Fine-Gray exato. A diferença metodológica é reconhecida, mas a comparação relativa entre modelos na mesma população é válida."

---

## Slide 13 — Conclusões `[14:45 – 15:30]`

> "Para concluir: as simulações computacionais confirmam que LGE e duração do QRS são candidatos relevantes para melhorar o modelo preditivo de Wahbi.
>
> Os Hazard Ratios estimados ficaram dentro das faixas hipotéticas — HR 2,26 para LGE e 1,23 por 10 ms para QRS. O C-index melhorou de 0,768 para 0,794, e essa melhora é consistente em toda a análise de sensibilidade.
>
> A implicação clínica direta é que a RMC deveria ser considerada nos protocolos de estratificação de risco para portadores de mutação LMNA — e o QRS, que já é medido em todo ECG, é um marcador incremental de baixo custo.
>
> Toda a análise está disponível no Google Colab — reprodutível, sem dados de pacientes reais, seed fixo 42.
>
> Obrigado. Fico à disposição para perguntas."

---

## Dicas de apresentação

- **Slide 3 e 7**: não precisa entrar em detalhes matemáticos do Fine-Gray — se perguntarem, diga que é regressão de sobrevivência com dois desfechos concorrentes.
- **Slide 6**: aponte visualmente para as barras de erro e diga "cada barra representa a faixa reportada na literatura".
- **Slide 9**: mencione que C-index é análogo à AUC — se a audiência for de ML, isso já comunica bem.
- **Slide 11**: fale as limitações com confiança, não como desculpa — faz parte do rigor científico reconhecê-las.
- **Tempo de fala**: pratique 1–2 vezes cronometrando. O roteiro foi escrito para ~14 min 30 s, deixando 30 s de folga.
