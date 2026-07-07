import math
import random
import time
from utils import calcular_custo

def gerar_vizinho_2opt(rota):
    """
    Operador de Vizinhança Estocástico (baseado no movimento 2-opt de Lin, 1965).
    Ao contrário de uma busca local exaustiva clássica de complexidade O(N^2), 
    este operador aplica uma única inversão de sub-segmento aleatório. 
    Esta perturbação geométrica atua desfazendo cruzamentos de arestas ("nós") no mapa,
    garantindo eficiência computacional (O(1) para gerar a vizinhança).
    """
    tamanho = len(rota)
    start, end = sorted(random.sample(range(tamanho), 2))
    
    # Slice e inversão in-place (preserva o vetor original na memória até a aceitação)
    nova_rota = rota.copy()
    nova_rota[start:end] = nova_rota[start:end][::-1]
    
    return nova_rota

def executar_sa(matriz_distancias, temp_inicial=10000, temp_final=1, taxa_resfriamento=0.995, iteracoes_por_temp=122, seed=None):
    """
    Motor do Simulated Annealing baseado na analogia do resfriamento termodinâmico (Kirkpatrick et al., 1983).
    
    Controla rigorosamente a transição entre a fase de "Exploração" (temperaturas altas) 
    e a fase de "Explotação/Refinamento" (temperaturas baixas).
    """
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

    num_cidades = len(matriz_distancias)
    
    # 1. Solução Inicial (Ponto de partida aleatório no espaço de busca)
    rota_atual = list(range(num_cidades))
    random.shuffle(rota_atual)
    custo_atual = calcular_custo(rota_atual, matriz_distancias)
    
    melhor_rota_global = rota_atual.copy()
    menor_custo_global = custo_atual

    inicio_tempo = time.time()

    
    temperatura = temp_inicial
    historico_custos = []
    
    ciclo = 0 # Contador para o feedback visual no console
    
    # 2. Ciclo Térmico (Equilíbrio por Temperatura)
    while temperatura > temp_final:
        for _ in range(iteracoes_por_temp):
            # Gera UMA única solução vizinha através da perturbação geométrica
            rota_vizinha = gerar_vizinho_2opt(rota_atual)
            custo_vizinho = calcular_custo(rota_vizinha, matriz_distancias)
            
            delta = custo_vizinho - custo_atual
            
            # 3. Critério de Aceitação de Metropolis
            # Se delta < 0: A solução é melhor, aceita incondicionalmente (Explotação).
            # Se delta >= 0: A solução é pior, aceita com base na Probabilidade de Boltzmann (Exploração).
            # A probabilidade de aceitar soluções piores cai exponencialmente conforme a T diminui.
            if delta < 0 or random.random() < math.exp(-delta / temperatura):
                rota_atual = rota_vizinha
                custo_atual = custo_vizinho
                
                # Atualiza a memória de longo prazo (Elitismo implícito do SA)
                if custo_atual < menor_custo_global:
                    menor_custo_global = custo_atual
                    melhor_rota_global = rota_atual.copy()
                    
        historico_custos.append(menor_custo_global)
        
        # Feedback visual a cada 100 ciclos (Não afeta o cronómetro significativo)
        if ciclo % 5 == 0:
            tempo_decorrido = time.time() - inicio_tempo
            print(f"Ciclo {ciclo:04d} | Temp: {temperatura:7.2f} | Melhor Custo: {menor_custo_global} | Tempo Decorrido: {tempo_decorrido:.4f}s")
            
        # 4. Decaimento Térmico (Esfriamento Geométrico)
        temperatura *= taxa_resfriamento
        ciclo += 1

    return melhor_rota_global, historico_custos