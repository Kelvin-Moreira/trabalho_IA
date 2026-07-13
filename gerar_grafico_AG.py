import glob
import os
import matplotlib.pyplot as plt
import numpy as np


def ler_curvas_pasta(caminho_pasta, tam_populacao=150):
    """Lê todos os arquivos .txt de uma pasta e calcula a matriz de custos (Execuções x Avaliações)."""
    arquivos = sorted(glob.glob(os.path.join(caminho_pasta, "*.txt")))

    if not arquivos:
        print(f"Aviso: Nenhum arquivo .txt encontrado na pasta '{caminho_pasta}'")
        return np.array([]), np.array([])

    todas_as_curvas = []
    eixo_x = []

    for caminho in arquivos:
        custos = []
        avals = []
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                if linha.startswith("Geração"):
                    partes = linha.split("|")
                    geracao = int(partes[0].split()[1])
                    custo = float(partes[1].split(":")[1].strip())

                    avals.append(geracao * tam_populacao)
                    custos.append(custo)

        if not eixo_x and avals:
            eixo_x = avals

        if custos:
            todas_as_curvas.append(custos)

    return np.array(eixo_x), np.array(todas_as_curvas)


def gerar_grafico_sensibilidade_media(
    pasta_10, pasta_20, pasta_30, nome_saida="sensibilidade_AG_media_10_exec.png"
):
    plt.figure(figsize=(10, 6))

    configuracoes = [
        (pasta_10, "Mutação 10%", "#d62728"),  # Vermelho
        (pasta_20, "Mutação 20%", "#ff7f0e"),  # Laranja
        (pasta_30, "Mutação 30%", "#1f77b4"),  # Azul
    ]

    for pasta, rotulo, cor in configuracoes:
        avals, matriz_custos = ler_curvas_pasta(pasta)

        if len(matriz_custos) > 0:
            # Ignora a Geração 0 para o custo inicial não achatar a escala do gráfico
            avals = avals[1:]
            matriz_custos = matriz_custos[:, 1:]

            # Calcula apenas a média de cada coluna (avaliação) entre as 10 execuções
            media = np.mean(matriz_custos, axis=0)

            # Desenha a linha limpa da média
            plt.plot(
                avals,
                media,
                marker="o",
                markersize=4,
                color=cor,
                linewidth=2.5,
                label=f"{rotulo} (Média Final: {media[-1]:.1f})",
            )
        else:
            print(f"Erro: Não foi possível processar os dados de '{pasta}'.")

    # Linha do Ótimo Global
    plt.axhline(
        y=2020.0,
        color="black",
        linestyle="--",
        linewidth=1.5,
        label="Ótimo Global (2020.0)",
    )

    # Formatação Acadêmica do Gráfico
    plt.title(
        "Análise do AG — Média de 10 Execuções",
        fontsize=13,
        fontweight="bold",
    )
    plt.xlabel("Avaliações da Função Objetivo", fontsize=12)
    plt.ylabel("Custo Médio da Rota", fontsize=12)
    plt.ticklabel_format(style="plain", axis="x")
    plt.grid(True, linestyle=":", alpha=0.7)
    plt.legend(fontsize=11, loc="upper right")
    plt.tight_layout()

    plt.savefig(nome_saida, dpi=300)
    print(f"\n[SUCESSO] Gráfico gerado com sucesso: {nome_saida}")


if __name__ == "__main__":
    PASTA_MUT_10 = "teste_AG_10"
    PASTA_MUT_20 = "teste_AG_20"
    PASTA_MUT_30 = "teste_AG_30"

    gerar_grafico_sensibilidade_media(PASTA_MUT_10, PASTA_MUT_20, PASTA_MUT_30)