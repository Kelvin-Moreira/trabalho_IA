import random
from utils import calcular_custo
from .operadores import torneio, order_crossover, inversion_mutation

def executar_ga(matriz_distancias, num_geracoes=1500, tam_populacao=150, taxa_mutacao=0.30, seed=None):

    if seed is not None:
        random.seed(seed)
    else:
        # Se nenhuma seed for passada, garante que o relógio do sistema cria uma nova
        random.seed() 
        
    num_cidades = len(matriz_distancias)


    num_cidades = len(matriz_distancias)
    
    # Inicialização Otimizada com Cache de Fitness
    cidades_base = list(range(num_cidades))
    populacao = []
    for _ in range(tam_populacao):
        rota = cidades_base.copy()
        random.shuffle(rota)
        custo = calcular_custo(rota, matriz_distancias)
        populacao.append((rota, custo)) # Guarda o tuplo (rota, custo)
        
    melhor_rota_global = None
    menor_custo_global = float('inf')
    historico_custos = []

    print("Iniciando GA (Orçamento: {} avaliações)...".format(num_geracoes * tam_populacao))
    
    for geracao in range(num_geracoes):
        nova_populacao = []
        
        # Elitismo: Já temos os custos pré-calculados
        melhor_da_geracao = min(populacao, key=lambda ind: ind[1])
        
        if melhor_da_geracao[1] < menor_custo_global:
            menor_custo_global = melhor_da_geracao[1]
            melhor_rota_global = melhor_da_geracao[0].copy()
            
        historico_custos.append(menor_custo_global)
        # Protege a elite passando uma cópia explícita
        nova_populacao.append((melhor_da_geracao[0].copy(), melhor_da_geracao[1]))
        
        while len(nova_populacao) < tam_populacao:
            # Seleciona os pais
            pai1 = torneio(populacao)
            pai2 = torneio(populacao)
            
            # Recombina (passando apenas os arrays de rota)
            filho_rota = order_crossover(pai1[0], pai2[0])
            
            # Muta
            if random.random() < taxa_mutacao:
                filho_rota = inversion_mutation(filho_rota)
                
            # Avalia a função objetivo (ÚNICA VEZ por indivíduo gerado)
            filho_custo = calcular_custo(filho_rota, matriz_distancias)
            nova_populacao.append((filho_rota, filho_custo))
            
        populacao = nova_populacao
        if geracao % 100 == 0:
            print(f"Geração {geracao:04d} | Melhor Custo: {menor_custo_global}")
        
    return melhor_rota_global, historico_custos