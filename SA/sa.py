import math
import random
from utils import calcular_custo

def gerar_vizinho_2opt(rota):
    """
    Operador 2-opt estocástico derivado da mecânica geométrica (Lin, 1965).
    Inverte um segmento aleatório para remover cruzamentos de arestas.
    """
    tamanho = len(rota)
    start, end = sorted(random.sample(range(tamanho), 2))
    
    # Slice e inversão in-place não devem alterar o pai até a aceitação
    nova_rota = rota.copy()
    nova_rota[start:end] = nova_rota[start:end][::-1]
    
    return nova_rota

def executar_sa(matriz_distancias, temp_inicial=10000, temp_final=1, taxa_resfriamento=0.995, iteracoes_por_temp=122, seed=None):
    """
    Motor do Simulated Annealing baseado em Kirkpatrick et al. (1983).
    """
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

    num_cidades = len(matriz_distancias)
    
    # 1. Solução Inicial
    rota_atual = list(range(num_cidades))
    random.shuffle(rota_atual)
    custo_atual = calcular_custo(rota_atual, matriz_distancias)
    
    melhor_rota_global = rota_atual.copy()
    menor_custo_global = custo_atual
    
    temperatura = temp_inicial
    historico_custos = []
    
    ciclo = 0 # Contador para o feedback visual
    
    # 2. Ciclo de Resfriamento
    while temperatura > temp_final:
        for _ in range(iteracoes_por_temp):
            # Gera vizinho com 2-opt
            rota_vizinha = gerar_vizinho_2opt(rota_atual)
            custo_vizinho = calcular_custo(rota_vizinha, matriz_distancias)
            
            delta = custo_vizinho - custo_atual
            
            # 3. Critério de Aceitação de Metropolis (Kirkpatrick, 1983)
            if delta < 0 or random.random() < math.exp(-delta / temperatura):
                rota_atual = rota_vizinha
                custo_atual = custo_vizinho
                
                # Registo do melhor encontrado até ao momento
                if custo_atual < menor_custo_global:
                    menor_custo_global = custo_atual
                    melhor_rota_global = rota_atual.copy()
                    
        historico_custos.append(menor_custo_global)
        
        # Feedback visual a cada 100 ciclos
        if ciclo % 100 == 0:
            print(f"Ciclo {ciclo:04d} | Temp: {temperatura:7.2f} | Melhor Custo: {menor_custo_global}")
            
        # Diminui a temperatura
        temperatura *= taxa_resfriamento
        ciclo += 1

    return melhor_rota_global, historico_custos