# Análise das notas de matemática

Este programa lê uma coluna de notas de um arquivo CSV, calcula estatísticas descritivas e compara a distribuição observada com a regra empírica da distribuição normal. Ao final, exibe um relatório no terminal e salva um histograma com a curva normal teórica.

## Requisitos

- Python 3.8 ou superior;
- `matplotlib` para gerar o gráfico.

Os cálculos estatísticos usam apenas recursos da biblioteca padrão do Python (`csv`, `math`, `collections` e `pathlib`). O `matplotlib` é usado somente para produzir a imagem.

### Instalar o matplotlib

Em um ambiente virtual chamado `.venv`:

```bash
.venv/bin/python -m pip install matplotlib
```

No Windows, use:

```powershell
.venv\Scripts\python.exe -m pip install matplotlib
```

## Arquivo de entrada

O arquivo precisa estar no formato CSV e conter uma coluna com o cabeçalho exato `math score`. Por padrão, o programa usa `StudentsPerformance.csv`, localizado na mesma pasta do script. A base incluída neste projeto contém 1.000 registros.

Valores vazios são contados como ausentes e ignorados. Valores que não podem ser convertidos para números inteiros são contados como inválidos e também ignorados. O programa informa essas quantidades no relatório. Se o cabeçalho não existir ou não houver nenhuma nota válida, a análise termina com uma mensagem de erro.

## Executar

Na raiz do projeto, usando o ambiente virtual:

```bash
.venv/bin/python analise_distribuicao_normal.py
```

Para analisar outro CSV, informe seu caminho como argumento:

```bash
.venv/bin/python analise_distribuicao_normal.py caminho/para/notas.csv
```

O caminho informado pode ser relativo ao diretório em que o comando foi executado ou absoluto. Para localizar o Python do ambiente virtual no Windows, use `.venv\Scripts\python.exe` no lugar de `.venv/bin/python`.

## Resultados calculados

O relatório apresentado no terminal inclui:

- quantidade de notas válidas, valores ausentes e inválidos;
- menor e maior nota e amplitude;
- média, mediana e moda(s);
- variância e desvio-padrão amostrais;
- coeficiente de assimetria amostral;
- quantidade e percentual de notas nos intervalos de um, dois e três desvios-padrão em torno da média, comparados com 68%, 95% e 99,7%;
- escores z da menor nota, da maior nota e dos valores de referência 50, 75 e 90. O programa sinaliza como possível valor atípico um escore com `|z| > 3`;
- uma conclusão descritiva baseada nas medidas calculadas.

As medidas são calculadas a partir dos dados do CSV em cada execução. A variância e o desvio-padrão usam a fórmula amostral (`n - 1`). A comparação com a regra empírica é uma avaliação aproximada: não é um teste formal de normalidade e não prova que os dados seguem uma distribuição normal.

## Gráfico gerado

O programa salva `histograma_curva_normal.png` na mesma pasta do arquivo CSV analisado. O gráfico contém:

- histograma das notas em escala de densidade;
- curva normal teórica calculada com a média e o desvio-padrão amostral;
- linha vertical da média;
- linhas verticais em um desvio-padrão abaixo e acima da média.

Se o `matplotlib` não puder ser importado pelo Python em uso, o programa informa como instalar a dependência. Erros de leitura do CSV ou de gravação do gráfico também são apresentados no terminal.

## Arquivos do projeto

```text
.
├── analise_distribuicao_normal.py
├── StudentsPerformance.csv
└── README.md
```

Após executar o programa, o gráfico `histograma_curva_normal.png` também estará disponível na pasta de saída.
