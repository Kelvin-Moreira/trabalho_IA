import random
from utils import calcular_custo

def torneio(populacao, matriz_distancias, k=3):
    """Seleciona as k rotas aleatórias e retorna a de menor custo."""
    competidores = random.sample(populacao, k)
    melhor = min(competidores, key=lambda rota: calcular_custo(rota, matriz_distancias))
    return melhor

def order_crossover(p1, p2):
    """Cruzamento OX com indexação circular."""
    tamanho = len(p1)
    start, end = sorted(random.sample(range(tamanho), 2))
    filho = [-1] * tamanho
    
    # Passo 1: Copia o segmento interno do Pai 1
    filho[start:end] = p1[start:end]
    
    pos_insercao = end
    pos_busca_p2 = end
    
    # Passo 2 e 3: Preenche com o Pai 2 (wrap-around com %)
    while -1 in filho:
        cidade_candidata = p2[pos_busca_p2 % tamanho]
        if cidade_candidata not in filho:
            filho[pos_insercao % tamanho] = cidade_candidata
            pos_insercao += 1
        pos_busca_p2 += 1
        
    return filho

def inversion_mutation(rota):
    """Inverte um sub-caminho da rota para gerar diversidade."""
    tamanho = len(rota)
    start, end = sorted(random.sample(range(tamanho), 2))
    rota[start:end] = rota[start:end][::-1]
    return rota