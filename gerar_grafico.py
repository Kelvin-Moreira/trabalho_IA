import os
import matplotlib.pyplot as plt

def ler_log_ag(caminho):
    iteracoes, custos = [], []
    with open(caminho, 'r', encoding='utf-8') as f:
        for linha in f:
            if linha.startswith("Geração"):
                partes = linha.split('|')
                # Extrai a Geração: "Geração 0100 " -> 100
                geracao = int(partes[0].split()[1])
                # Extrai o Custo: " Melhor Custo: 2270.0 " -> 2270.0
                custo = float(partes[1].split(':')[1].strip())
                iteracoes.append(geracao)
                custos.append(custo)
    return iteracoes, custos

def ler_log_sa(caminho):
    iteracoes, custos = [], []
    with open(caminho, 'r', encoding='utf-8') as f:
        for linha in f:
            if linha.startswith("Ciclo"):
                partes = linha.split('|')
                # Extrai o Ciclo: "Ciclo 0100 " -> 100
                ciclo = int(partes[0].split()[1])
                # Extrai o Custo (no SA o custo é a 3ª parte da string dividida por '|')
                custo = float(partes[2].split(':')[1].strip())
                iteracoes.append(ciclo)
                custos.append(custo)
    return iteracoes, custos

def plotar_comparacao(arquivos_labels, funcao_leitura, titulo, label_x, nome_arquivo):
    plt.figure(figsize=(10, 6))
    
    # Cores contrastantes para diferenciar claramente as configurações
    cores = ['#d62728', '#ff7f0e', '#1f77b4'] 
    
    for idx, (caminho_arquivo, label_legenda) in enumerate(arquivos_labels):
        if os.path.exists(caminho_arquivo):
            iteracoes, custos = funcao_leitura(caminho_arquivo)
            
            # TRUQUE DO ZOOM: Cortamos o ponto inicial (Geração/Ciclo 0)
            # Isso impede que o custo inicial de ~5000 achate as linhas no gráfico
            if len(iteracoes) > 1:
                iteracoes = iteracoes[1:]
                custos = custos[1:]
                
            resultado_final = custos[-1] if custos else 0
            
            plt.plot(
                iteracoes,
                custos,
                marker='o',
                markersize=5,
                color=cores[idx],
                linewidth=2.5,
                label=f'{label_legenda} (Melhor: {resultado_final:.0f})'
            )
        else:
            print(f"Aviso Crítico: O ficheiro {caminho_arquivo} não foi encontrado na pasta raiz.")

    # Adiciona a linha do Ótimo Global
    plt.axhline(y=2020.0, color='black', linestyle='--', linewidth=1.5, label='Ótimo Global (2020.0)')

    # Formatação do Gráfico para padrão de Relatório/Artigo
    plt.title(titulo, fontsize=14, fontweight='bold')
    plt.xlabel(label_x, fontsize=12)
    plt.ylabel('Custo da Rota', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(fontsize=11, loc='upper right')
    plt.tight_layout()
    
    # Salva a imagem em alta resolução
    plt.savefig(nome_arquivo, dpi=300)
    print(f"Gráfico salvo com sucesso: {nome_arquivo}")
    plt.close()

if __name__ == "__main__":
    print("Gerando gráficos de Análise de Sensibilidade...\n")
    
    # 1. Configuração do Algoritmo Genético
    # Estrutura: ("nome_do_arquivo.txt", "Rótulo que vai aparecer na Legenda")
    arquivos_ag = [
        ("teste_AG\log_execucao_mut_10.txt", "Mutação 10%"),
        ("teste_AG\log_execucao_mut_20.txt", "Mutação 20%"),
        ("teste_AG\log_execucao_mut_30.txt", "Mutação 30%")
    ]
    
    plotar_comparacao(
        arquivos_labels=arquivos_ag, 
        funcao_leitura=ler_log_ag, 
        titulo="Análise de Sensibilidade: Taxa de Mutação (GA)", 
        label_x="Iterações", 
        nome_arquivo="analise_sensibilidade_AG.png"
    )
                     
    # 2. Configuração do Simulated Annealing
    arquivos_sa = [
        ("teste_SA\log_execucao_taxa_85.txt", "Resfriamento 0.85"),
        ("teste_SA\log_execucao_taxa_95.txt", "Resfriamento 0.95"),
        ("teste_SA\log_execucao_taxa_995.txt", "Resfriamento 0.995")
    ]
    
    plotar_comparacao(
        arquivos_labels=arquivos_sa, 
        funcao_leitura=ler_log_sa, 
        titulo="Análise de Sensibilidade: Curva de Resfriamento (SA)", 
        label_x="Ciclos Térmicos", 
        nome_arquivo="analise_sensibilidade_SA.png"
    )