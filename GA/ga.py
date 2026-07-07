import random
import time
from utils import calcular_custo
from .operadores import torneio, order_crossover, inversion_mutation

def executar_ga(matriz_distancias, num_geracoes=1500, tam_populacao=150, taxa_mutacao=0.30, seed=None):
    """
    Motor da Meta-heurística Populacional (Algoritmo Genético) baseado em Goldberg (1989).
    
    Projetado para macro-exploração do espaço de busca. Utiliza representação 
    permutacional estrita para garantir a validade das rotas do Caixeiro Viajante.
    """
    if seed is not None:
        random.seed(seed)
    else:
        # Garante entropia através do relógio do sistema para testes independentes
        random.seed() 
        
    num_cidades = len(matriz_distancias)
    
    # 1. Inicialização Otimizada com Cache de Fitness
    # Evita o recálculo redundante da função objetivo guardando o estado (rota, custo)
    cidades_base = list(range(num_cidades))
    populacao = []
    for _ in range(tam_populacao):
        rota = cidades_base.copy()
        random.shuffle(rota)
        custo = calcular_custo(rota, matriz_distancias)
        populacao.append((rota, custo)) 
        
    melhor_rota_global = None
    menor_custo_global = float('inf')
    historico_custos = []

    print("Iniciando GA (Orçamento: {} avaliações)...".format(num_geracoes * tam_populacao))
    inicio_tempo = time.time()
    # 2. Ciclo Evolutivo
    for geracao in range(num_geracoes):
        nova_populacao = []
        
        # 3. Elitismo 
        # Garante convergência monotónica: a melhor solução nunca é perdida para a mutação
        melhor_da_geracao = min(populacao, key=lambda ind: ind[1])
        
        if melhor_da_geracao[1] < menor_custo_global:
            menor_custo_global = melhor_da_geracao[1]
            melhor_rota_global = melhor_da_geracao[0].copy()
            
        historico_custos.append(menor_custo_global)
        
        # Protege a elite passando uma cópia explícita para a nova geração
        nova_populacao.append((melhor_da_geracao[0].copy(), melhor_da_geracao[1]))
        
        # 4. Substituição Populacional 
        while len(nova_populacao) < tam_populacao:
            # Seleção guiada por pressão seletiva
            pai1 = torneio(populacao)
            pai2 = torneio(populacao)
            
            # Recombinação de características herdadas 
            filho_rota = order_crossover(pai1[0], pai2[0])
            
            # Perturbação Estocástica para manutenção da diversidade
            if random.random() < taxa_mutacao:
                filho_rota = inversion_mutation(filho_rota)
                
            # 5. Avaliação (
            # A função objetivo é chamada uma ÚNICA VEZ por indivíduo gerado
            filho_custo = calcular_custo(filho_rota, matriz_distancias)
            nova_populacao.append((filho_rota, filho_custo))
            
        populacao = nova_populacao
        
        if geracao % 100 == 0:
            tempo_decorrido = time.time() - inicio_tempo
            print(f"Geração {geracao:04d} | Melhor Custo: {menor_custo_global} | Tempo Decorrido: {tempo_decorrido:.2f}s")
        
    return melhor_rota_global, historico_custos