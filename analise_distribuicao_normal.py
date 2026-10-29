#!/usr/bin/env python3
"""Analisa as notas de matemática e compara sua distribuição com a normal.

Uso: python analise_distribuicao_normal.py [caminho/StudentsPerformance.csv]

Os cálculos estatísticos são implementados neste arquivo sem bibliotecas
estatísticas. O matplotlib é usado exclusivamente para gerar os gráficos.
"""

import csv
import math
import sys
from collections import Counter
from pathlib import Path


COLUNA_NOTAS = "math score"
ARQUIVO_PADRAO = "StudentsPerformance.csv"
ARQUIVO_GRAFICO = "histograma_curva_normal.png"


def carregar_notas(caminho):
    """Lê a coluna de notas e retorna (notas, inválidos, ausentes)."""
    notas = []
    invalidos = []
    ausentes = 0

    with caminho.open("r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        if leitor.fieldnames is None or COLUNA_NOTAS not in leitor.fieldnames:
            colunas = ", ".join(leitor.fieldnames or []) or "nenhuma"
            raise ValueError(
                f"A coluna obrigatória {COLUNA_NOTAS!r} não foi encontrada. "
                f"Colunas disponíveis: {colunas}."
            )

        for numero_linha, registro in enumerate(leitor, start=2):
            valor = registro.get(COLUNA_NOTAS)
            if valor is None or not valor.strip():
                ausentes += 1
                continue
            try:
                nota = int(valor.strip())
            except (TypeError, ValueError):
                invalidos.append((numero_linha, valor))
                continue
            notas.append(nota)

    if not notas:
        raise ValueError("Nenhuma nota válida foi encontrada no arquivo.")
    return notas, invalidos, ausentes


def calcular_medidas(dados):
    """Calcula medidas descritivas usando apenas operações aritméticas."""
    ordenados = sorted(dados)
    n = len(ordenados)
    media = sum(ordenados) / n
    meio = n // 2
    if n % 2:
        mediana = float(ordenados[meio])
    else:
        mediana = (ordenados[meio - 1] + ordenados[meio]) / 2

    frequencias = Counter(ordenados)
    frequencia_maxima = max(frequencias.values())
    modas = sorted(valor for valor, frequencia in frequencias.items()
                   if frequencia == frequencia_maxima)
    soma_quadrados = sum((valor - media) ** 2 for valor in ordenados)
    variancia = soma_quadrados / (n - 1) if n > 1 else 0.0
    desvio = math.sqrt(variancia)
    if n > 2 and desvio > 0:
        assimetria = (n / ((n - 1) * (n - 2))) * sum(
            ((valor - media) / desvio) ** 3 for valor in ordenados
        )
    else:
        assimetria = 0.0

    return {
        "quantidade": n,
        "menor": ordenados[0],
        "maior": ordenados[-1],
        "amplitude": ordenados[-1] - ordenados[0],
        "media": media,
        "mediana": mediana,
        "modas": modas,
        "frequencia_moda": frequencia_maxima,
        "variancia": variancia,
        "desvio": desvio,
        "assimetria": assimetria,
    }


def proporcoes_regra_empirica(dados, media, desvio):
    resultados = []
    for multiplos, esperado in ((1, 68.0), (2, 95.0), (3, 99.7)):
        inferior = media - multiplos * desvio
        superior = media + multiplos * desvio
        quantidade = sum(inferior <= valor <= superior for valor in dados)
        percentual = 100 * quantidade / len(dados)
        resultados.append((multiplos, inferior, superior, quantidade,
                           percentual, esperado))
    return resultados


def gerar_grafico(dados, media, desvio, destino):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as erro:
        raise RuntimeError(
            "Para gerar o gráfico, instale matplotlib (python -m pip install matplotlib)."
        ) from erro

    minimo, maximo = min(dados), max(dados)
    amplitude = maximo - minimo
    largura = amplitude / 30 if amplitude else 1
    bins = max(1, min(30, math.ceil(amplitude / largura)))
    figura, eixo = plt.subplots(figsize=(10, 6))
    eixo.hist(dados, bins=bins, density=True, color="#78a9d1", alpha=0.72,
              edgecolor="white", label="Notas observadas")

    if desvio > 0:
        passo = (maximo - minimo) / 400 if maximo > minimo else desvio / 100
        inicio = min(minimo, media - 4 * desvio)
        fim = max(maximo, media + 4 * desvio)
        xs = [inicio + i * (fim - inicio) / 500 for i in range(501)]
        densidades = [math.exp(-0.5 * ((x - media) / desvio) ** 2) /
                      (desvio * math.sqrt(2 * math.pi)) for x in xs]
        eixo.plot(xs, densidades, color="#c43c39", linewidth=2,
                  label="Curva normal teórica (μ e s da amostra)")
        eixo.axvline(media - desvio, color="#4d7c0f", linestyle="--",
                     label="Média − 1 desvio-padrão")
        eixo.axvline(media + desvio, color="#4d7c0f", linestyle="--",
                     label="Média + 1 desvio-padrão")
    eixo.axvline(media, color="#222222", linewidth=1.8, label=f"Média = {media:.2f}")
    eixo.set(title="Distribuição das notas de matemática",
             xlabel="Nota de matemática", ylabel="Densidade")
    eixo.grid(axis="y", alpha=0.2)
    eixo.legend()
    figura.tight_layout()
    figura.savefig(destino, dpi=160)
    plt.close(figura)


def exibir_relatorio(caminho, dados, medidas, invalidos, ausentes, faixas,
                     z_valores, caminho_grafico):
    print("INTRODUÇÃO TEÓRICA")
    print("A distribuição normal (Curva de Gauss) é contínua, simétrica e tem "
          "forma de sino. Sua média (μ) determina o centro e seu desvio-padrão "
          "(σ) descreve a dispersão. Na regra empírica, cerca de 68%, 95% e "
          "99,7% dos valores ficam, respectivamente, a até 1, 2 e 3 desvios "
          "da média. O escore padronizado z = (x − μ) / σ indica quantos "
          "desvios uma observação está do centro.")
    print(f"\nARQUIVO: {caminho}")
    print(f"Registros válidos carregados: {len(dados)}")
    print(f"Valores ausentes: {ausentes}; valores inválidos: {len(invalidos)}")
    if invalidos:
        print("Linhas inválidas (até 10): " + ", ".join(
            f"{linha}={valor!r}" for linha, valor in invalidos[:10]))

    print("\nMEDIDAS ESTATÍSTICAS")
    print(f"Quantidade: {medidas['quantidade']}")
    print(f"Menor nota: {medidas['menor']}; maior nota: {medidas['maior']}; "
          f"amplitude: {medidas['amplitude']}")
    print(f"Média: {medidas['media']:.4f}; mediana: {medidas['mediana']:.4f}")
    print(f"Moda(s): {', '.join(map(str, medidas['modas']))} "
          f"(frequência: {medidas['frequencia_moda']})")
    print(f"Variância amostral: {medidas['variancia']:.4f}")
    print(f"Desvio-padrão amostral: {medidas['desvio']:.4f}")
    print(f"Assimetria amostral: {medidas['assimetria']:.4f}")

    print("\nREGRA 68–95–99,7")
    for multiplos, inferior, superior, quantidade, percentual, esperado in faixas:
        print(f"±{multiplos}s ({inferior:.2f} a {superior:.2f}): "
              f"{quantidade} notas ({percentual:.2f}%; esperado ≈ {esperado:.1f}%)")

    print("\nESCORES Z (usando média e desvio-padrão amostral)")
    for rotulo, valor, z in z_valores:
        classificacao = "possível valor atípico" if abs(z) > 3 else "|z| ≤ 3"
        print(f"{rotulo} ({valor}): z = {z:.4f} — {classificacao}")

    assimetria = medidas["assimetria"]
    if abs(assimetria) < 0.1:
        descricao_assimetria = "pequena (próxima da simetria)"
    elif assimetria > 0:
        descricao_assimetria = "positiva (cauda à direita)"
    else:
        descricao_assimetria = "negativa (cauda à esquerda)"
    valores_atipicos = [rotulo for rotulo, _, z in z_valores if abs(z) > 3]
    proximas = all(abs(item[4] - item[5]) <= 5 for item in faixas)
    print("\nCONCLUSÃO")
    print("1. O formato de sino deve ser avaliado visualmente no histograma; "
          "a sobreposição mostra a referência normal teórica.")
    print(f"2. Média e mediana {'são' if abs(medidas['media'] - medidas['mediana']) <= 2 else 'não são'} "
          "próximas (diferença: "
          f"{abs(medidas['media'] - medidas['mediana']):.2f} pontos).")
    print(f"3. Os percentuais observados {'são' if proximas else 'não são'} "
          "próximos dos valores empíricos (tolerância descritiva de 5 pontos percentuais).")
    print(f"4. Assimetria: {descricao_assimetria} (coeficiente {assimetria:.4f}).")
    print("5. Entre os valores avaliados, " +
          ("há possíveis atípicos: " + ", ".join(valores_atipicos) + "."
           if valores_atipicos else "não há possíveis atípicos pelo critério |z| > 3."))
    print("6. Não é adequado afirmar que os dados seguem perfeitamente uma "
          "normal: os resultados e o gráfico permitem apenas uma avaliação aproximada.")
    print("7. Conclusão cuidadosa: descreva a distribuição como mais ou menos "
          "compatível com o padrão normal conforme o histograma, a assimetria e "
          "as proporções observadas; isso não prova normalidade perfeita.")
    print(f"\nGráfico salvo em: {caminho_grafico}")


def main():
    base = Path(__file__).resolve().parent
    caminho = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else base / ARQUIVO_PADRAO
    if not caminho.is_absolute():
        caminho = Path.cwd() / caminho
    caminho = caminho.resolve()
    if not caminho.is_file():
        print(f"Erro: arquivo CSV não encontrado: {caminho}", file=sys.stderr)
        print(f"Uso: python {Path(__file__).name} [caminho/{ARQUIVO_PADRAO}]", file=sys.stderr)
        return 1

    try:
        dados, invalidos, ausentes = carregar_notas(caminho)
        medidas = calcular_medidas(dados)
        faixas = proporcoes_regra_empirica(dados, medidas["media"], medidas["desvio"])
        valores_consultados = [
            ("Menor nota", medidas["menor"]), ("Maior nota", medidas["maior"]),
            ("Nota de referência", 50), ("Nota de referência", 75),
            ("Nota de referência", 90),
        ]
        z_valores = [(rotulo, valor,
                      (valor - medidas["media"]) / medidas["desvio"]
                      if medidas["desvio"] else 0.0)
                     for rotulo, valor in valores_consultados]
        destino = caminho.parent / ARQUIVO_GRAFICO
        gerar_grafico(dados, medidas["media"], medidas["desvio"], destino)
        exibir_relatorio(caminho, dados, medidas, invalidos, ausentes, faixas,
                         z_valores, destino)
    except (OSError, ValueError, RuntimeError) as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
