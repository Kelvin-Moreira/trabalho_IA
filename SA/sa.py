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

def executar_sa(
    matriz_distancias,
    temp_inicial=10000,
    orcamento_maximo=225000,
    taxa_resfriamento=0.995,
    iteracoes_por_temp=122,
    seed=None,
):
    """Motor do Simulated Annealing baseado na analogia do resfriamento termodinâmico (Kirkpatrick et al., 1983)."""
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

    ciclo = 0
    avaliacoes = 1  # Já gastamos 1 avaliação ao calcular a solução inicial!

    # 2. Ciclo Térmico controlado rigorosamente pelo orçamento de avaliações
    while avaliacoes < orcamento_maximo:
        for _ in range(iteracoes_por_temp):
            if avaliacoes >= orcamento_maximo:
                break  # Trava de segurança absoluta

            # 1. Gera vizinho 2-opt
            rota_vizinha = gerar_vizinho_2opt(rota_atual)

            # 2. Avalia o custo (GASTA 1 AVALIAÇÃO DO ORÇAMENTO)
            custo_vizinho = calcular_custo(rota_vizinha, matriz_distancias)
            avaliacoes += 1

            # 3. Critério de Metropolis blindado contra divisão por zero
            delta = custo_vizinho - custo_atual
            aceitar_pior = False

            if delta >= 0 and temperatura > 1e-10:
                try:
                    if random.random() < math.exp(-delta / temperatura):
                        aceitar_pior = True
                except OverflowError:
                    aceitar_pior = False

            if delta < 0 or aceitar_pior:
                rota_atual = rota_vizinha
                custo_atual = custo_vizinho

                # === ADIÇÃO CRÍTICA: Atualização do Elitismo Global ===
                if custo_atual < menor_custo_global:
                    menor_custo_global = custo_atual
                    melhor_rota_global = rota_atual.copy()

        # === ADIÇÃO CRÍTICA: Registro da Curva de Convergência ===
        historico_custos.append(menor_custo_global)

        # Feedback visual a cada ciclo
        if ciclo % 1 == 0:
            tempo_decorrido = time.time() - inicio_tempo
            print(
                f"Ciclo {ciclo:04d} | Temp: {temperatura:7.2f} | Melhor Custo: {menor_custo_global} | Tempo Decorrido: {tempo_decorrido:.4f}s"
            )

        # 4. Decaimento Térmico
        temperatura *= taxa_resfriamento
        ciclo += 1

    return melhor_rota_global, historico_custos