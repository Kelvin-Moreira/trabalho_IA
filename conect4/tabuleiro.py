from defines import *

class Tabuleiro():
    def __init__(self, linhas, colunas, matriz=None):
        self.linhas = linhas
        self.colunas = colunas
        
        # Caso não seja passada uma matriz, cria uma preenchida com zeros
        if matriz is None:
            self.matriz = [[0 for _ in range(colunas)] for _ in range(linhas)]
        else:
            self.matriz = matriz

    def getMatriz(self):
        return self.matriz
        
    def getLinhas(self):
        return self.linhas
        
    def getColunas(self):
        return self.colunas

    def printMatrizCLI(self):
        for linha in self.matriz:
            # Troca os números por símbolos só para o visual no terminal
            linha_visual = []
            for peca in linha:
                if peca == 1: linha_visual.append("[ 1 ]") # Peça do Agente 1
                elif peca == 2: linha_visual.append("[ 2 ]") # Peça do Agente 2
                else: linha_visual.append("[   ]") # Vazio
            print("".join(linha_visual))
        print("-" * 35)

    # Primeira linha livre de baixo para cima na coluna. Caso nenhuma, retorna LINHA_INVALIDA
    def getPosicaoLivreColuna(self, coluna):
        for linha in range(self.linhas):
            linhaBaixoParaCima = self.linhas - 1 - linha
            if (self.matriz[linhaBaixoParaCima][coluna] == AGENTE_VAZIO):
                return linhaBaixoParaCima
            
        return LINHA_INVALIDA 
    
    # Retorna todas as colunas ainda válidas
    def getListaColunasLivres(self):
        colunasLivres = []
        for coluna in range(self.colunas):
            if (self.getPosicaoLivreColuna(coluna) != LINHA_INVALIDA):
                colunasLivres.append(coluna)
        return colunasLivres

    # Posiciona uma peça do agente no primeiro espaço livre
    def posiciona(self, coluna, IdAgente):
        linhaPosicionar = self.getPosicaoLivreColuna(coluna)

        if linhaPosicionar == LINHA_INVALIDA:
            return False 
        
        self.matriz[linhaPosicionar][coluna] = IdAgente
        return True

    # Verifica se alguém venceu ou deu empate
    def verificaEstado(self, agente):
        # Quatro peças na horizontal
        for linha in range(self.linhas):
            for coluna in range(self.colunas - 3):
                if (self.matriz[linha][coluna] == agente and self.matriz[linha][coluna + 1] == agente and self.matriz[linha][coluna + 2] == agente and self.matriz[linha][coluna + 3] == agente):
                    return VITORIA

        # Quatro peças na vertical
        for coluna in range(self.colunas):
            for linha in range(self.linhas - 3):
                if (self.matriz[linha][coluna] == agente and self.matriz[linha + 1][coluna] == agente and self.matriz[linha + 2][coluna] == agente and self.matriz[linha + 3][coluna] == agente):
                    return VITORIA
            
        # Quatro peças em uma diagonal
        for coluna in range(self.colunas - 3):
            for linha in range(self.linhas - 3):
                if (self.matriz[linha][coluna] == agente and self.matriz[linha + 1][coluna + 1] == agente and self.matriz[linha + 2][coluna + 2] == agente and self.matriz[linha + 3][coluna + 3] == agente):
                    return VITORIA
                elif (self.matriz[linha][coluna + 3] == agente and self.matriz[linha + 1][coluna + 2] == agente and self.matriz[linha + 2][coluna + 1] == agente and self.matriz[linha + 3][coluna] == agente):
                    return VITORIA

        if len(self.getListaColunasLivres()) == 0:
            return EMPATE
        
        return ANDAMENTO