import glob
import os
import matplotlib.pyplot as plt
import numpy as np


def ler_curvas_pasta_sa(caminho_pasta, iteracoes_por_ciclo):
    """Lê os arquivos .txt de uma pasta do SA, converte ciclos em avaliações

    e retorna a curva média interpolada em uma grade comum de orçamento.
    """
    arquivos = sorted(glob.glob(os.path.join(caminho_pasta, "*.txt")))

    if not arquivos:
        print(f"Aviso: Nenhum arquivo .txt encontrado em '{caminho_pasta}'")
        return np.array([]), np.array([])

    todas_as_curvas = []

    # Criamos uma grade comum do orçamento (de 0 até ~225.000 avaliações, de 500 em 500)
    grade_comum_avals = np.arange(0, 225000, 500)

    for caminho in arquivos:
        custos = []
        avals = []
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                if linha.startswith("Ciclo"):
                    partes = linha.split("|")
                    ciclo = int(partes[0].split()[1])
                    custo = float(partes[2].split(":")[1].strip())

                    avals.append(ciclo * iteracoes_por_ciclo)
                    custos.append(custo)

        if avals and custos:
            # Como a taxa rápida para cedo, repetimos o último custo (estagnação)
            # para preencher o resto do orçamento na interpolação
            curva_interpolada = np.interp(
                grade_comum_avals, avals, custos, right=custos[-1]
            )
            todas_as_curvas.append(curva_interpolada)

    if not todas_as_curvas:
        return np.array([]), np.array([])

    matriz_custos = np.array(todas_as_curvas)
    media_custos = np.mean(matriz_custos, axis=0)

    return grade_comum_avals, media_custos


def gerar_grafico_sensibilidade_sa(
    pasta_85, pasta_95, pasta_995, nome_saida="sensibilidade_SA_media_10_exec.png"
):
    plt.figure(figsize=(10, 6))

    # Configurações: (Pasta, Iterações por Ciclo, Rótulo, Cor)
    configuracoes = [
        (pasta_85, 122, "Resfriamento 0.85 (Rápido)", "#d62728"),  # Vermelho
        (pasta_95, 50, "Resfriamento 0.95 (Intermediário)", "#ff7f0e"),  # Laranja
        (pasta_995, 122, "Resfriamento 0.995 (Suave)", "#1f77b4"),  # Azul
    ]

    for pasta, iter_ciclo, rotulo, cor in configuracoes:
        avals, media = ler_curvas_pasta_sa(pasta, iter_ciclo)

        if len(media) > 0:
            # Ignora os primeiros pontos iniciais muito altos para não achatar o gráfico
            avals_plot = avals[1:]
            media_plot = media[1:]

            plt.plot(
                avals_plot,
                media_plot,
                color=cor,
                linewidth=2.5,
                label=f"{rotulo} (Média Final: {media_plot[-1]:.1f})",
            )
        else:
            print(f"Erro ao processar a pasta '{pasta}'.")

    # Linha do Ótimo Global
    plt.axhline(
        y=2020.0,
        color="black",
        linestyle="--",
        linewidth=1.5,
        label="Ótimo Global (2020.0)",
    )

    # Formatação Acadêmica
    plt.title(
        "Análise de Sensibilidade do SA — Média de 10 Execuções",
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
    print(f"\n[SUCESSO] Gráfico salvo em: {nome_saida}")


if __name__ == "__main__":
    PASTA_SA_85 = "teste_SA_85"
    PASTA_SA_95 = "teste_SA_95"
    PASTA_SA_995 = "teste_SA_995"

    gerar_grafico_sensibilidade_sa(PASTA_SA_85, PASTA_SA_95, PASTA_SA_995)