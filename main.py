from utils import carregar_matriz
from ga import executar_ga

def main():
    # 1. Carregar os dados (Certifique-se de que o ficheiro txt está na mesma pasta)
    caminho_arquivo = 'bays29.txt' 
    print(f"Lendo a matriz de distâncias de: {caminho_arquivo}")
    
    try:
        matriz = carregar_matriz(caminho_arquivo)
        print(f"Mapa carregado com sucesso: {len(matriz)} cidades detectadas.\n")
    except Exception as e:
        print(f"Erro ao abrir ou ler o ficheiro: {e}")
        return

    # 2. Executar o Algoritmo Genético
    # Pode ajustar estes hiperparâmetros depois para comparar performance
    melhor_rota, historico = executar_ga(
        matriz_distancias=matriz, 
        num_geracoes=1500, 
        tam_populacao=150, 
        taxa_mutacao=0.10
    )

    # 3. Imprimir o Veredito
    print("\n" + "="*40)
    print("           RESULTADO FINAL")
    print("="*40)
    print(f"Melhor Rota Encontrada: \n{melhor_rota}")
    print(f"\nCusto Final da Viagem: {historico[-1]}")

if __name__ == "__main__":
    main()