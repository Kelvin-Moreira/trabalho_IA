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

def plotar_curva(pasta, funcao_leitura, titulo, label_x, nome_arquivo):
    plt.figure(figsize=(10, 6))
    
    # Cores para diferenciar as 3 execuções
    cores = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    # Lê os 3 arquivos de log da pasta
    for i in range(1, 4):
        caminho_arquivo = os.path.join(pasta, f"log_execucao_0{i}.txt")
        
        if os.path.exists(caminho_arquivo):
            iteracoes, custos = funcao_leitura(caminho_arquivo)
            resultado_final = custos[-1]
            plt.plot(
                iteracoes,
                custos,
                marker='o',
                markersize=4,
                color=cores[i-1],
                linewidth=2,
                label=f'Execução {i} (Melhor: {resultado_final:.0f})'
            )
        else:
            print(f"Aviso: {caminho_arquivo} não encontrado.")

    # Adiciona a linha do Ótimo Global
    plt.axhline(y=2020.0, color='r', linestyle='--', linewidth=1.5, label='Ótimo Global (2020.0)')

    # Formatação do Gráfico
    plt.title(titulo, fontsize=14, fontweight='bold')
    plt.xlabel(label_x, fontsize=12)
    plt.ylabel('Custo da Rota', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(fontsize=10)
    plt.tight_layout()
    
    # Salva a imagem
    plt.savefig(nome_arquivo, dpi=300)
    print(f"Gráfico salvo com sucesso: {nome_arquivo}")
    plt.close()

if __name__ == "__main__":
    print("Gerando gráficos de convergência...")
    plotar_curva("teste_AG", ler_log_ag, 
                 "Curva de Convergência (3 Execuções) - Algoritmo Genético", 
                 "Gerações", "convergencia_AG.png")
                 
    plotar_curva("teste_SA", ler_log_sa, 
                 "Curva de Convergência (3 Execuções) - Simulated Annealing", 
                 "Ciclos Térmicos", "convergencia_SA.png")