from defines import *
from agente import Agente
from tabuleiro import Tabuleiro
import random

class AgenteIA(Agente):

    def calculaHeuristicaTabuleiro(self, tabuleiro, idAgente):
        """
        =========================================================
        AQUI ENTRA A SUA HEURÍSTICA
        =========================================================
        """
        matriz = tabuleiro.getMatriz()
        valorHeuristica = 0
        
        # TODO: Implemente a lógica de avaliação aqui
        
        return valorHeuristica       

    def buscaColunaMiniMax(self, tabuleiro, profundidade, alpha, beta, maximizar):
        colunasLivres = tabuleiro.getListaColunasLivres()
        
        # Identifica dinamicamente quem é a IA e quem é o Oponente
        id_ia = self.getId()
        id_oponente = AGENTE_2 if id_ia == AGENTE_1 else AGENTE_1
        
        vitoria_ia = tabuleiro.verificaEstado(id_ia) == VITORIA
        vitoria_oponente = tabuleiro.verificaEstado(id_oponente) == VITORIA

        posicaoTerminal = len(colunasLivres) == 0 or vitoria_ia or vitoria_oponente

        if (profundidade == 0 or posicaoTerminal):
            if posicaoTerminal:
                if vitoria_ia:
                    return (None, INFINITO_POSITIVO)
                elif vitoria_oponente:
                    return (None, INFINITO_NEGATIVO)
                else:
                    return (None, 0) # Empate
            else: 
                return (None, self.calculaHeuristicaTabuleiro(tabuleiro, id_ia))
            
        if maximizar:
            valorHeuristica = INFINITO_NEGATIVO
            colunaRet = random.choice(colunasLivres)

            for coluna in colunasLivres:
                matriz_copia = [linha[:] for linha in tabuleiro.getMatriz()]
                tabuleiroAux = Tabuleiro(tabuleiro.getLinhas(), tabuleiro.getColunas(), matriz_copia)
                # IA faz a jogada nas simulações dela
                tabuleiroAux.posiciona(coluna, id_ia)

                heuristicaFilho = self.buscaColunaMiniMax(tabuleiroAux, profundidade - 1, alpha, beta, False)[1]
                if heuristicaFilho > valorHeuristica:
                    valorHeuristica = heuristicaFilho
                    colunaRet = coluna

                alpha = max(alpha, valorHeuristica)
                if beta <= alpha:
                    break

            return colunaRet, valorHeuristica

        else:
            valorHeuristica = INFINITO_POSITIVO
            colunaRet = random.choice(colunasLivres)

            for coluna in colunasLivres:
                matriz_copia = [linha[:] for linha in tabuleiro.getMatriz()]
                tabuleiroAux = Tabuleiro(tabuleiro.getLinhas(), tabuleiro.getColunas(), matriz_copia)
                # Oponente faz a jogada nas simulações da IA
                tabuleiroAux.posiciona(coluna, id_oponente)

                heuristicaFilho = self.buscaColunaMiniMax(tabuleiroAux, profundidade - 1, alpha, beta, True)[1]
                if heuristicaFilho < valorHeuristica:
                    valorHeuristica = heuristicaFilho
                    colunaRet = coluna

                beta = min(beta, valorHeuristica)
                if beta <= alpha:
                    break

            return colunaRet, valorHeuristica
        
    def jogar(self, tabuleiro):
        profundidade = tabuleiro.getLinhas() - 1
        coluna, valorMiniMax = self.buscaColunaMiniMax(tabuleiro, profundidade, INFINITO_NEGATIVO, INFINITO_POSITIVO, True)

        if coluna is not None:
            tabuleiro.posiciona(coluna, self.getId())
            print(f"\n[JOGADA REALIZADA] A IA (Agente {self.getId()}) inseriu uma peça na Coluna {coluna}")
        else:
            print("\nNão há mais jogadas válidas.")