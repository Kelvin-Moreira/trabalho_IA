import math

def carregar_matriz(caminho_arquivo):
    """
    Lê o ficheiro txt e constrói a matriz de distâncias N x N.
    Equivalente otimizado ao ExtratorProblemaTSP que vimos em Java.
    """
    numeros = []
    with open(caminho_arquivo, 'r') as f:
        for linha in f:
            # Lê todos os números separados por espaços
            numeros.extend([float(x) for x in linha.split()])
            
    # Deduz o tamanho da matriz (N cidades)
    num_cidades = int(math.sqrt(len(numeros)))
    matriz = []
    
    indice = 0
    for _ in range(num_cidades):
        linha_matriz = []
        for _ in range(num_cidades):
            linha_matriz.append(numeros[indice])
            indice += 1
        matriz.append(linha_matriz)
        
    return matriz

def calcular_custo(rota, matriz_distancias):
    """Calcula a distância total da rota, fechando o ciclo na origem."""
    custo = 0
    tamanho = len(rota)
    for i in range(tamanho):
        origem = rota[i]
        destino = rota[(i + 1) % tamanho]
        custo += matriz_distancias[origem][destino]
    return custo