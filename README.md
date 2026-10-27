# Conceito, exemplo numérico e implementação em Python

## 1. Objetivo

Desenvolver um programa em Python capaz de carregar dados numéricos de um arquivo CSV, calcular medidas estatísticas, construir gráficos e avaliar se a variável selecionada apresenta comportamento aproximadamente compatível com uma distribuição normal.

A atividade deverá relacionar os conceitos teóricos da distribuição normal com uma análise prática de dados reais.

## 2. Base de dados sugerida

Utilize a base **Students Performance in Exams**, disponível no Kaggle.

**Arquivo:** `StudentsPerformance.csv`

A base possui 1.000 registros e oito colunas, contendo características dos estudantes e notas de matemática, leitura e escrita.

As principais variáveis quantitativas são:

- `math score`: nota de matemática;
- `reading score`: nota de leitura;
- `writing score`: nota de escrita.

Para a análise principal do trabalho, utilize a coluna **`math score`**.

## 3. Introdução teórica

A distribuição normal, também conhecida como **Curva de Gauss**, é uma distribuição contínua, simétrica e com formato de sino. Ela é determinada por dois parâmetros:

- **Média (μ):** determina o centro da distribuição;
- **Desvio-padrão (σ):** determina a dispersão dos valores.

A função densidade da distribuição normal é:

\[
f(x) = \frac{1}{\sigma\sqrt{2\pi}}
\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
\]

Para dados aproximadamente normais, espera-se que:

- aproximadamente **68%** dos valores estejam entre \(\mu-\sigma\) e \(\mu+\sigma\);
- aproximadamente **95%** estejam entre \(\mu-2\sigma\) e \(\mu+2\sigma\);
- aproximadamente **99{,}7%** estejam entre \(\mu-3\sigma\) e \(\mu+3\sigma\).

Essa propriedade é conhecida como **regra empírica 68–95–99,7**.

## 4. Atividades solicitadas

O programa deverá ser construído a partir dos dados brutos do arquivo CSV. Não serão aceitos programas que apresentem resultados inseridos manualmente.

### Parte A — Pesquisa teórica

Elabore uma introdução explicando:

- o conceito de distribuição normal;
- as características da Curva de Gauss;
- a função da média na distribuição;
- a função do desvio-padrão;
- o significado da regra 68–95–99,7;
- o conceito de escore padronizado \(z\).

O escore \(z\) deve ser apresentado pela fórmula:

\[
z = \frac{x-\mu}{\sigma}
\]

### Parte B — Leitura e organização dos dados

Desenvolva um programa que:

- leia o arquivo `StudentsPerformance.csv` utilizando o módulo `csv`;
- utilize `csv.DictReader` para acessar as colunas;
- converta os valores da coluna `math score` para números inteiros;
- armazene as notas em uma lista;
- informe a quantidade de registros carregados;
- verifique se existem valores ausentes ou inválidos.

### Parte C — Medidas estatísticas

Calcule, sem utilizar bibliotecas estatísticas:

- quantidade de dados;
- menor nota;
- maior nota;
- amplitude total;
- média aritmética;
- mediana;
- moda ou modas;
- variância amostral;
- desvio-padrão amostral;
- coeficiente de assimetria.

Utilize a fórmula do desvio-padrão amostral:

\[
s = \sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}}
\]

### Parte D — Regra 68–95–99,7

Determine a quantidade e o percentual de notas localizadas nos seguintes intervalos:

| Intervalo | Percentual esperado |
|---|---:|
| \(\bar{x}-s\) até \(\bar{x}+s\) | 68% |
| \(\bar{x}-2s\) até \(\bar{x}+2s\) | 95% |
| \(\bar{x}-3s\) até \(\bar{x}+3s\) | 99,7% |

### Parte E — Escores padronizados

Calcule o escore \(z\) para:

- a menor nota;
- a maior nota;
- uma nota igual a 50;
- uma nota igual a 75;
- uma nota igual a 90.

Classifique como possíveis valores atípicos aqueles que apresentarem:

\[
|z| > 3
\]

### Parte F — Representação gráfica

O programa deverá gerar:

- histograma das notas;
- curva normal teórica sobreposta ao histograma;
- linha vertical indicando a média;
- linhas indicando um desvio-padrão abaixo e acima da média;
- gráfico de caixa, opcionalmente.

### Parte G — Conclusão

Responda às seguintes perguntas:

1. O histograma apresenta aproximadamente o formato de sino?
2. Média e mediana apresentam valores próximos?
3. Os percentuais observados são próximos da regra 68–95–99,7?
4. A distribuição apresenta assimetria?
5. Existem valores atípicos?
6. É adequado afirmar que os dados seguem perfeitamente uma distribuição normal?
7. Qual seria uma conclusão mais cuidadosa sobre a distribuição das notas?

## 5. Arquivos para entrega

Cada dupla deverá entregar a seguinte estrutura:

```text
Trabalho_Distribuicao_Normal/
├── analise_distribuicao_normal.py
├── StudentsPerformance.csv
├── histograma_curva_normal.png
└── relatorio.pdf
```

A apresentação de 10 minutos deverá conter:

- fundamentação teórica;
- descrição da base de dados;
- fórmulas utilizadas;
- resultados encontrados;
- gráfico produzido;
- interpretação dos resultados;
- conclusão.

## 6. Restrições

Não deverão ser utilizadas bibliotecas estatísticas para realizar os cálculos.

**Não utilizar:**

- `statistics`;
- `scipy.stats`;
- `numpy.mean`;
- `numpy.std`;
- `pandas.mean`;
- `pandas.std`.

**Podem ser utilizados:**

- `csv`;
- `math`;
- `matplotlib`.

O `matplotlib` será usado somente para a geração dos gráficos.
