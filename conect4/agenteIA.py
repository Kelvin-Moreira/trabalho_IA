from defines import *
from agente import Agente
from tabuleiro import Tabuleiro
import random

class AgenteIA(Agente):

    def calculaHeuristicaGrupo(self, grupo, idAgente):
        """ 
        Avalia um grupo isolado de 4 espaços.
        Retorna: (Pontuacao_do_Grupo, Ameaça_IA, Ameaça_Oponente)
        """
        idAdversario = AGENTE_2 if idAgente == AGENTE_1 else AGENTE_1
        pontuacao = 0
        ameaca_ia = 0
        ameaca_oponente = 0

        # --- MODO ATAQUE ---
        if grupo.count(idAgente) == 4:
            pontuacao += 1000
        elif grupo.count(idAgente) == 3 and grupo.count(AGENTE_VAZIO) == 1:
            pontuacao += 100
            ameaca_ia = 1  # Registra que encontrou uma ameaça a favor da IA
        elif grupo.count(idAgente) == 2 and grupo.count(AGENTE_VAZIO) == 2:
            pontuacao += 10

        # --- MODO DEFESA ---
        if grupo.count(idAdversario) == 3 and grupo.count(AGENTE_VAZIO) == 1:
            pontuacao -= 500  
            ameaca_oponente = 1 # Registra que o inimigo tem uma ameaça perigosa
        elif grupo.count(idAdversario) == 2 and grupo.count(AGENTE_VAZIO) == 2:
            pontuacao -= 50   

        return pontuacao, ameaca_ia, ameaca_oponente

    def calculaHeuristicaTabuleiro(self, tabuleiro, idAgente):
        """ Varre o tabuleiro inteiro e aplica a Tabela de Pesos, avaliação de grupos e Bônus de Trio Duplo """
        matriz = tabuleiro.getMatriz()
        linhas = tabuleiro.getLinhas()
        colunas = tabuleiro.getColunas()
        pontuacao_total = 0
        
        total_ameacas_ia = 0
        total_ameacas_oponente = 0
        
        idAdversario = AGENTE_2 if idAgente == AGENTE_1 else AGENTE_1

        # Tabela de pesos do tabuleiro 
        tabela_pesos = [
            [3, 4, 5, 7, 5, 4, 3],
            [4, 6, 8, 10, 8, 6, 4],
            [5, 8, 11, 20, 11, 8, 5],
            [5, 8, 11, 20, 11, 8, 5],
            [4, 6, 8, 10, 8, 6, 4],
            [3, 4, 5, 7, 5, 4, 3]
        ]

        for l in range(linhas):
            for c in range(colunas):
                if matriz[l][c] == idAgente:
                    pontuacao_total += tabela_pesos[l][c]
                elif matriz[l][c] == idAdversario:
                    pontuacao_total -= tabela_pesos[l][c]

        # AVALIAÇÃO DE GRUPOS
        
        # Avalia Linhas Horizontais
        for l in range(linhas):
            linha_atual = matriz[l]
            for c in range(colunas - 3):
                grupo = linha_atual[c:c+4]
                pts, am_ia, am_op = self.calculaHeuristicaGrupo(grupo, idAgente)
                pontuacao_total += pts
                total_ameacas_ia += am_ia
                total_ameacas_oponente += am_op

        # Avalia Colunas Verticais
        for c in range(colunas):
            coluna_atual = [matriz[l][c] for l in range(linhas)]
            for l in range(linhas - 3):
                grupo = coluna_atual[l:l+4]
                pts, am_ia, am_op = self.calculaHeuristicaGrupo(grupo, idAgente)
                pontuacao_total += pts
                total_ameacas_ia += am_ia
                total_ameacas_oponente += am_op

        # Avalia Diagonais Positivas (/)
        for l in range(linhas - 3):
            for c in range(colunas - 3):
                grupo = [matriz[l][c], matriz[l+1][c+1], matriz[l+2][c+2], matriz[l+3][c+3]]
                pts, am_ia, am_op = self.calculaHeuristicaGrupo(grupo, idAgente)
                pontuacao_total += pts
                total_ameacas_ia += am_ia
                total_ameacas_oponente += am_op

        # Avalia Diagonais Negativas (\)
        for l in range(linhas - 3):
            for c in range(colunas - 3):
                grupo = [matriz[l+3][c], matriz[l+2][c+1], matriz[l+1][c+2], matriz[l][c+3]]
                pts, am_ia, am_op = self.calculaHeuristicaGrupo(grupo, idAgente)
                pontuacao_total += pts
                total_ameacas_ia += am_ia
                total_ameacas_oponente += am_op

        # Estrategia do trio duplo
        
        # Se a IA formou 2 ou mais ameaças de vitória simultâneas
        if total_ameacas_ia >= 2:
            pontuacao_total += 200
            
        # Se o oponente formou 2 ou mais ameaças de vitória simultâneas
        if total_ameacas_oponente >= 2:
            pontuacao_total -= 500

        return pontuacao_total

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