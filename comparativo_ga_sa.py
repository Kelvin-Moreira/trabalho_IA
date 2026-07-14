import os
import glob
import numpy as np
import matplotlib.pyplot as plt

def ler_pasta_e_calcular_media(pasta, tipo_log, iteracoes_ou_populacao):
    """
    Lê os 10 arquivos de uma pasta, converte as iterações/gerações para Avaliações
    da Função Objetivo e retorna a curva média interpolada.
    """
    arquivos = sorted(glob.glob(os.path.join(pasta, "*.txt")))
    if not arquivos:
        print(f"Erro: Nenhum arquivo .txt encontrado em '{pasta}'")
        return np.array([]), np.array([])

    todas_as_curvas = []
    # Nossa régua universal de 0 a 225.000 avaliações
    grade_comum_avals = np.arange(0, 225000, 500)

    for caminho in arquivos:
        avals = []
        custos = []
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                if tipo_log == "GA" and linha.startswith("Geração"):
                    partes = linha.split("|")
                    unidade = int(partes[0].split()[1]) # Geração
                    custo = float(partes[1].split(":")[1].strip())
                    
                    avals.append(unidade * iteracoes_ou_populacao)
                    custos.append(custo)
                    
                elif tipo_log == "SA" and linha.startswith("Ciclo"):
                    partes = linha.split("|")
                    unidade = int(partes[0].split()[1]) # Ciclo
                    custo = float(partes[2].split(":")[1].strip())
                    
                    avals.append(unidade * iteracoes_ou_populacao)
                    custos.append(custo)

        if avals and custos:
            # Estica a execução na régua universal. Se o algoritmo parou antes, 
            # repete o último custo (estagnação) até o fim das 225.000 avaliações.
            curva_interp = np.interp(grade_comum_avals, avals, custos, right=custos[-1])
            todas_as_curvas.append(curva_interp)

    # Faz o corte vertical somando e dividindo por 10 em cada marcação da régua
    media_custos = np.mean(todas_as_curvas, axis=0)
    
    return grade_comum_avals, media_custos

def gerar_grafico_batalha_medias(pasta_ga, pasta_sa, nome_saida="batalha_final_medias.png"):
    plt.figure(figsize=(10, 6))

    # 1. Processar a Média do Algoritmo Genético (População = 150)
    avals_ga, media_ga = ler_pasta_e_calcular_media(pasta_ga, tipo_log="GA", iteracoes_ou_populacao=150)
    if len(media_ga) > 0:
        # Pula a avaliação 0 para evitar achatamento inicial extremo
        plt.plot(avals_ga[1:], media_ga[1:], color='#d62728', linewidth=2.5, 
                 label=f'Algoritmo Genético - Mutação 30% (Média Final: {media_ga[-1]:.1f})')

    # 2. Processar a Média do Simulated Annealing (Iterações por temp = 122)
    avals_sa, media_sa = ler_pasta_e_calcular_media(pasta_sa, tipo_log="SA", iteracoes_ou_populacao=122)
    if len(media_sa) > 0:
        # Pula a avaliação 0 para evitar achatamento inicial extremo
        plt.plot(avals_sa[1:], media_sa[1:], color='#1f77b4', linewidth=2.5, 
                 label=f'Simulated Annealing - Taxa 0.995 (Média Final: {media_sa[-1]:.1f})')

    # 3. Linha do Ótimo Global
    plt.axhline(y=2020.0, color='black', linestyle='--', linewidth=1.5, label='Ótimo Global (2020.0)')

    # 4. Formatação Acadêmica
    plt.title('Batalha Final (Médias de 10 Execuções): GA vs SA', fontsize=14, fontweight='bold')
    plt.xlabel('Avaliações da Função Objetivo (Custo Computacional Equivalente)', fontsize=12)
    plt.ylabel('Custo Médio da Rota', fontsize=12)
    
    # Impede notação científica (ex: 2e5) no eixo X
    plt.ticklabel_format(style='plain', axis='x')
    
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(fontsize=11, loc='upper right')
    plt.tight_layout()

    plt.savefig(nome_saida, dpi=300)
    print(f"\n[SUCESSO] Gráfico da Batalha de Médias salvo em: {nome_saida}")

if __name__ == "__main__":
    # Coloque o nome correto das pastas onde estão guardadas as 10 rodadas campeãs
    PASTA_GA_CAMPEAO = "teste_AG_30" 
    PASTA_SA_CAMPEAO = "teste_SA_995"
    
    gerar_grafico_batalha_medias(PASTA_GA_CAMPEAO, PASTA_SA_CAMPEAO)