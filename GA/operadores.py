import random

def torneio(populacao, k=3):
    """
    Mecanismo de Pressão Seletiva.
    
    Seleciona 'k' indivíduos aleatórios e escolhe o de menor custo.
    A comparação é executada em O(1) pois o fitness (custo) já está em cache
    no tuplo (rota, custo), evitando recalcular rotas de tamanho O(N).
    """
    competidores = random.sample(populacao, k)
    melhor = min(competidores, key=lambda ind: ind[1])
    return melhor

def order_crossover(p1_rota, p2_rota):
    """
    Order Crossover (OX) - Proposto por Davis (1985).
    
    Projetado para domínios de alta epistasia (como o TSP). Transfere um segmento
    direto do Pai 1 para preservar a ordem e adjacência local, preenchendo o 
    restante com os genes do Pai 2 para evitar cidades duplicadas.
    
    Complexidade otimizada de O(N^2) para O(N) utilizando 
    Hash Maps (Sets) do Python, prevenindo colapso de CPU em mapas de grande escala.
    """
    tamanho = len(p1_rota)
    start, end = sorted(random.sample(range(tamanho), 2))
    filho = [-1] * tamanho
    
    # 1. Copia o segmento base do Pai 1
    filho[start:end] = p1_rota[start:end]
    
    # Busca O(1): Cria um set com as cidades já herdadas
    cidades_presentes = set(filho[start:end])
    
    pos_insercao = end
    pos_busca_p2 = end
    
    # 2. Preenche o restante preservando a ordem relativa do Pai 2
    while -1 in filho:
        cidade_candidata = p2_rota[pos_busca_p2 % tamanho]
        
        # A validação no Hash Map é O(1), eliminando iterações redundantes
        if cidade_candidata not in cidades_presentes:
            filho[pos_insercao % tamanho] = cidade_candidata
            cidades_presentes.add(cidade_candidata)
            pos_insercao += 1
            
        pos_busca_p2 += 1
        
    return filho

def inversion_mutation(rota):
    """
    Mutação por Inversão (Inversion Mutation) - Revisado por Larrañaga et al. (1999).
    
    Atua baseada no movimento geométrico do operador 2-opt, invertendo a ordem 
    de um sub-segmento aleatório. 
    
    Ao contrário de uma busca local, atua de forma estocástica e cega, servindo 
    exclusivamente como injeção de diversidade genética ("caos") para evitar 
    a convergência prematura da população.
    """
    tamanho = len(rota)
    start, end = sorted(random.sample(range(tamanho), 2))
    
    # Isola o indivíduo copiando o array antes da mutação in-place
    nova_rota = rota.copy()
    nova_rota[start:end] = nova_rota[start:end][::-1]
    
    return nova_rota