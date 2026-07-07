import os
import time 
import math
import sys # ADIÇÃO: Necessário para capturar o log do terminal
from utils import carregar_matriz

try:
    import GA.ga as ga
except ImportError:
    import ga
    
import SA.sa

# ADIÇÃO: Classe para espelhar o print do terminal para um arquivo de texto
class CapturarSaida:
    def __init__(self, caminho_arquivo):
        self.terminal = sys.stdout
        self.log = open(caminho_arquivo, "w", encoding="utf-8")

    def write(self, mensagem):
        self.terminal.write(mensagem) # Imprime na tela normalmente
        self.log.write(mensagem)      # Salva no arquivo ao mesmo tempo

    def flush(self):
        self.terminal.flush()
        self.log.flush()

    def fechar(self):
        self.log.close()
        sys.stdout = self.terminal # Devolve o controle normal ao Python

def main():
    # 1. Carregar os dados
    caminho_arquivo = r'tsp\Bays29.txt' 
    print(f"Lendo a matriz de distâncias de: {caminho_arquivo}")
    
    try:
        matriz = carregar_matriz(caminho_arquivo)
        print(f"Mapa carregado com sucesso: {len(matriz)} cidades detectadas.\n")
    except Exception as e:
        print(f"Erro ao abrir ou ler o ficheiro: {e}")
        return

    # 2. Configurar o sistema de Logs Unificado e Pastas Individuais
    pasta_logs = "teste_comparativo"
    pasta_ag = "teste_AG" # ADIÇÃO: Pasta para os logs do GA
    pasta_sa = "teste_SA" # ADIÇÃO: Pasta para os logs do SA
    
    os.makedirs(pasta_logs, exist_ok=True) 
    os.makedirs(pasta_ag, exist_ok=True) # Cria a pasta se não existir
    os.makedirs(pasta_sa, exist_ok=True) # Cria a pasta se não existir
    
    caminho_log = os.path.join(pasta_logs, "log_batalha_1.txt")
    num_testes = 10

    print(f"Iniciando a bateria de {num_testes} testes para cada algoritmo. Por favor, aguarde...\n")

    with open(caminho_log, "w", encoding="utf-8") as arquivo_log:
        arquivo_log.write("="*90 + "\n")
        arquivo_log.write("                 RELATÓRIO OFICIAL DE BENCHMARKING: GA vs SA\n")
        arquivo_log.write("="*90 + "\n\n")

        # ==========================================
        # FASE 1: ALGORITMO GENÉTICO (GA)
        # ==========================================
        print("-> A executar Bateria do Algoritmo Genético (GA)...")
        arquivo_log.write("--- FASE 1: ALGORITMO GENÉTICO (GA) ---\n")
        arquivo_log.write("Parâmetros: 1500 Gerações | População: 150 Indivíduos | Taxa de Mutação: 30%\n")
        arquivo_log.write("-" * 90 + "\n")
        
        resultados_ga = []
        tempos_ga = [] 
        melhor_rota_absoluta_ga = None
        menor_custo_ga = float('inf')
        
        for i in range(1, num_testes + 1):
            inicio_tempo = time.time() 
            
            # ADIÇÃO: Inicia a captura do terminal para o arquivo iterativo do AG
            arquivo_iterativo = os.path.join(pasta_ag, f"log_execucao_{i:02d}.txt")
            logger = CapturarSaida(arquivo_iterativo)
            sys.stdout = logger
            
            melhor_rota, historico = ga.executar_ga(
                matriz_distancias=matriz, 
                num_geracoes=1500, 
                tam_populacao=150, 
                taxa_mutacao=0.10,  
                seed=None
            )
            
            # ADIÇÃO: Encerra a captura e volta ao normal
            logger.fechar()
            
            fim_tempo = time.time() 
            tempo_execucao = fim_tempo - inicio_tempo 
            
            custo_final = historico[-1]
            resultados_ga.append(custo_final)
            tempos_ga.append(tempo_execucao)
            
            arquivo_log.write(f"Teste {i:02d} | Custo: {custo_final} | Tempo: {tempo_execucao:.4f}s | Rota: {melhor_rota}\n")
            
            if custo_final < menor_custo_ga:
                menor_custo_ga = custo_final
                melhor_rota_absoluta_ga = melhor_rota.copy()
            
        media_ga = sum(resultados_ga) / num_testes
        media_tempo_ga = sum(tempos_ga) / num_testes
        pior_ga = max(resultados_ga)
        desvio_ga = math.sqrt(sum((x - media_ga) ** 2 for x in resultados_ga) / (num_testes - 1) if num_testes > 1 else 0)
        
        arquivo_log.write(f"\n[GA] ESTATÍSTICAS:\n")
        arquivo_log.write(f"Custo Médio: {media_ga:.2f}\n")
        arquivo_log.write(f"Tempo Médio de Execução: {media_tempo_ga:.4f} segundos\n")
        arquivo_log.write(f"Melhor Custo Absoluto: {menor_custo_ga}\n")
        arquivo_log.write(f"Melhor Rota Absoluta: {melhor_rota_absoluta_ga}\n")
        arquivo_log.write(f"Pior Absoluto: {pior_ga}\n")
        arquivo_log.write(f"Desvio Padrão: {desvio_ga:.2f}\n\n\n")

        # ==========================================
        # FASE 2: SIMULATED ANNEALING (SA)
        # ==========================================
        print("-> A executar Bateria do Simulated Annealing (SA)...")
        arquivo_log.write("--- FASE 2: SIMULATED ANNEALING (SA) ---\n")
        arquivo_log.write("Parâmetros: Temp Inicial: 10000 | Temp Final: 1 | Resfriamento: 0.995 | Ciclos/Temp: 122\n")
        arquivo_log.write("-" * 90 + "\n")
        
        resultados_sa = []
        tempos_sa = [] 
        melhor_rota_absoluta_sa = None
        menor_custo_sa = float('inf')
        
        for i in range(1, num_testes + 1):
            inicio_tempo = time.time() 
            
            # ADIÇÃO: Inicia a captura do terminal para o arquivo iterativo do SA
            arquivo_iterativo = os.path.join(pasta_sa, f"log_execucao_{i:02d}.txt")
            logger = CapturarSaida(arquivo_iterativo)
            sys.stdout = logger
            
            melhor_rota, historico = SA.sa.executar_sa(
               matriz_distancias=matriz, 
                temp_inicial=2000,      
                temp_final=1, 
                taxa_resfriamento=0.95, 
                iteracoes_por_temp=50,  
                seed=None
            )
            
            # ADIÇÃO: Encerra a captura e volta ao normal
            logger.fechar()
            
            fim_tempo = time.time() 
            tempo_execucao = fim_tempo - inicio_tempo 
            
            custo_final = historico[-1]
            resultados_sa.append(custo_final)
            tempos_sa.append(tempo_execucao)
            
            arquivo_log.write(f"Teste {i:02d} | Custo: {custo_final} | Tempo: {tempo_execucao:.4f}s | Rota: {melhor_rota}\n")
            
            if custo_final < menor_custo_sa:
                menor_custo_sa = custo_final
                melhor_rota_absoluta_sa = melhor_rota.copy()
            
        media_sa = sum(resultados_sa) / num_testes
        media_tempo_sa = sum(tempos_sa) / num_testes
        pior_sa = max(resultados_sa)
        desvio_sa = math.sqrt(sum((x - media_sa) ** 2 for x in resultados_sa) / (num_testes - 1) if num_testes > 1 else 0)
        
        arquivo_log.write(f"\n[SA] ESTATÍSTICAS:\n")
        arquivo_log.write(f"Custo Médio: {media_sa:.2f}\n")
        arquivo_log.write(f"Tempo Médio de Execução: {media_tempo_sa:.4f} segundos\n")
        arquivo_log.write(f"Melhor Custo Absoluto: {menor_custo_sa}\n")
        arquivo_log.write(f"Melhor Rota Absoluta: {melhor_rota_absoluta_sa}\n")
        arquivo_log.write(f"Pior Absoluto: {pior_sa}\n")
        arquivo_log.write(f"Desvio Padrão: {desvio_sa:.2f}\n\n\n")

        # ==========================================
        # FASE 3: VEREDICTO FINAL
        # ==========================================
        arquivo_log.write("="*90 + "\n")
        arquivo_log.write("                               VEREDICTO FINAL\n")
        arquivo_log.write("="*90 + "\n")
        
        otimo_conhecido = 2020.0
        
        arquivo_log.write(f"Ótimo global do problema bays29: {otimo_conhecido}\n\n")
        
        arquivo_log.write(f"Desempenho Algoritmo Genético (GA):\n")
        arquivo_log.write(f" - Custo Médio: {media_ga:.2f} (Erro: {((media_ga - otimo_conhecido)/otimo_conhecido)*100:.2f}%)\n")
        arquivo_log.write(f" - Tempo Médio: {media_tempo_ga:.4f}s\n")
        
        arquivo_log.write(f"\nDesempenho Simulated Annealing (SA):\n")
        arquivo_log.write(f" - Custo Médio: {media_sa:.2f} (Erro: {((media_sa - otimo_conhecido)/otimo_conhecido)*100:.2f}%)\n")
        arquivo_log.write(f" - Tempo Médio: {media_tempo_sa:.4f}s\n")

        if media_ga < media_sa:
            vencedor = "ALGORITMO GENÉTICO (GA)"
        elif media_sa < media_ga:
            vencedor = "SIMULATED ANNEALING (SA)"
        else:
            vencedor = "EMPATE TÉCNICO"
            
        arquivo_log.write(f"\n>> ALGORITMO VENCEDOR NA MÉDIA (CUSTO): {vencedor} <<\n")

    print("\n" + "="*50)
    print("      BATERIA CONCLUÍDA: VEREDICTO FINAL")
    print("="*50)
    print(f"Média do GA: {media_ga:.2f} | Tempo Médio: {media_tempo_ga:.4f}s")
    print(f"Média do SA: {media_sa:.2f} | Tempo Médio: {media_tempo_sa:.4f}s")
    print(f"Vencedor no Custo: {vencedor}")
    print(f"\nRelatório completo guardado em: {caminho_log}")
    print("Os logs iterativos (curva de convergência) foram guardados nas pastas 'teste_AG' e 'teste_SA'.")

if __name__ == "__main__":
    main()