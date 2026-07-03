import random

def torneio(populacao, k=3):
    """
    População agora recebe tuplos: (rota, custo)
    O Torneio compara diretamente o custo em cache, sem recalcular O(N).
    """
    competidores = random.sample(populacao, k)
    # Retorna o indivíduo completo (rota, custo) com o menor custo
    melhor = min(competidores, key=lambda ind: ind[1])
    return melhor

def order_crossover(p1_rota, p2_rota):
    """OX com complexidade O(N) através da utilização de Sets (Hash Maps)."""
    tamanho = len(p1_rota)
    start, end = sorted(random.sample(range(tamanho), 2))
    filho = [-1] * tamanho
    
    # 1. Copia o segmento
    filho[start:end] = p1_rota[start:end]
    
    # Busca O(1): Cria um set com as cidades já presentes no filho
    cidades_presentes = set(filho[start:end])
    
    pos_insercao = end
    pos_busca_p2 = end
    
    # 2. Preenche o restante iterando o Pai 2
    while -1 in filho:
        cidade_candidata = p2_rota[pos_busca_p2 % tamanho]
        
        # A busca num set é O(1), eliminando a ineficiência estrutural
        if cidade_candidata not in cidades_presentes:
            filho[pos_insercao % tamanho] = cidade_candidata
            cidades_presentes.add(cidade_candidata)
            pos_insercao += 1
            
        pos_busca_p2 += 1
        
    return filho

def inversion_mutation(rota):
    tamanho = len(rota)
    start, end = sorted(random.sample(range(tamanho), 2))
    # Copia a rota antes de mutar para não alterar referências indesejadas
    nova_rota = rota.copy()
    nova_rota[start:end] = nova_rota[start:end][::-1]
    return nova_rota