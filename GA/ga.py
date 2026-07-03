import random
from utils import calcular_custo
from operadores import torneio, order_crossover, inversion_mutation

def executar_ga(matriz_distancias, num_geracoes=1000, tam_populacao=100, taxa_mutacao=0.05):
    num_cidades = len(matriz_distancias)
    
    # Criar população inicial com rotas aleatórias
    cidades_base = list(range(num_cidades))
    populacao = []
    for _ in range(tam_populacao):
        rota_aleatoria = cidades_base.copy()
        random.shuffle(rota_aleatoria)
        populacao.append(rota_aleatoria)
        
    melhor_rota_global = None
    menor_custo_global = float('inf')
    historico_custos = []

    print("Iniciando a Evolução (Algoritmo Genético)...")
    
    for geracao in range(num_geracoes):
        nova_populacao = []
        
        # Avaliar e salvar o melhor da geração atual (Elitismo)
        melhor_da_geracao = min(populacao, key=lambda r: calcular_custo(r, matriz_distancias))
        custo_atual = calcular_custo(melhor_da_geracao, matriz_distancias)
        
        if custo_atual < menor_custo_global:
            menor_custo_global = custo_atual
            melhor_rota_global = melhor_da_geracao.copy()
            
        historico_custos.append(menor_custo_global)
        nova_populacao.append(melhor_da_geracao) # Passa o melhor intacto
        
        # Preencher o restante da nova população
        while len(nova_populacao) < tam_populacao:
            pai1 = torneio(populacao, matriz_distancias)
            pai2 = torneio(populacao, matriz_distancias)
            
            filho = order_crossover(pai1, pai2)
            
            if random.random() < taxa_mutacao:
                filho = inversion_mutation(filho)
                
            nova_populacao.append(filho)
            
        populacao = nova_populacao
        
        if geracao % 100 == 0:
            print(f"Geração {geracao:04d} | Melhor Custo: {menor_custo_global}")

    print("\nEvolução Concluída!")
    return melhor_rota_global, historico_custos