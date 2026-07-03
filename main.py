import os
from utils import carregar_matriz
import GA.ga

def main():
    # 1. Carregar os dados (Certifique-se de que o ficheiro txt está na mesma pasta)
    caminho_arquivo = r'tsp\Bays29.txt' 
    print(f"Lendo a matriz de distâncias de: {caminho_arquivo}")
    
    try:
        matriz = carregar_matriz(caminho_arquivo)
        print(f"Mapa carregado com sucesso: {len(matriz)} cidades detectadas.\n")
    except Exception as e:
        print(f"Erro ao abrir ou ler o ficheiro: {e}")
        return

    # 2. Configurar o sistema de Logs
    pasta_logs = "teste_GA"
    # Cria a pasta automaticamente se ela não existir
    os.makedirs(pasta_logs, exist_ok=True) 
    caminho_log = os.path.join(pasta_logs, "log_resultados.txt")

    num_testes = 10
    resultados_custos = []

    print(f"Iniciando a bateria de {num_testes} testes. Por favor, aguarde...\n")

    # Abre o ficheiro de log em modo de escrita ('w')
    with open(caminho_log, "w", encoding="utf-8") as arquivo_log:
        arquivo_log.write("="*50 + "\n")
        arquivo_log.write("        LOG DE RESULTADOS - ALGORITMO GENÉTICO\n")
        arquivo_log.write("="*50 + "\n\n")

        # 3. Executar o Algoritmo Genético 10 vezes
        for i in range(1, num_testes + 1):
            # Print para o terminal não parecer "congelado"
            print(f"A executar teste {i}/{num_testes}...") 
            
            melhor_rota, historico = GA.ga.executar_ga(
                matriz_distancias=matriz, 
                num_geracoes=1500, 
                tam_populacao=150, 
                taxa_mutacao=0.30,  
                seed=None # Mantemos None para testar a robustez em diferentes inicializações
            )

            custo_final = historico[-1]
            resultados_custos.append(custo_final)

            # Escreve o resultado individual no ficheiro de log
            arquivo_log.write(f"--- Teste {i} ---\n")
            arquivo_log.write(f"Custo Final: {custo_final}\n")
            arquivo_log.write(f"Melhor Rota: {melhor_rota}\n\n")

        # 4. Calcular e escrever as estatísticas finais no log
        media = sum(resultados_custos) / num_testes
        melhor_absoluto = min(resultados_custos)
        pior_absoluto = max(resultados_custos)

        arquivo_log.write("="*50 + "\n")
        arquivo_log.write("               ESTATÍSTICAS FINAIS\n")
        arquivo_log.write("="*50 + "\n")
        arquivo_log.write(f"Número de execuções: {num_testes}\n")
        arquivo_log.write(f"Melhor custo encontrado: {melhor_absoluto}\n")
        arquivo_log.write(f"Pior custo encontrado: {pior_absoluto}\n")
        arquivo_log.write(f"Custo Médio: {media:.2f}\n")

    # 5. Imprimir o Veredito no terminal
    print("\n" + "="*40)
    print("           BATERIA CONCLUÍDA")
    print("="*40)
    print(f"Os resultados foram salvos com sucesso em: {caminho_log}")
    print(f"Custo Médio em {num_testes} execuções: {media:.2f}")
    print(f"Melhor Custo Absoluto Encontrado: {melhor_absoluto}")

if __name__ == "__main__":
    main()