import os
import ast
from defines import *
from tabuleiro import Tabuleiro
from agenteIA import AgenteIA

# ==========================================
# CONFIGURAÇÃO DA IA
# Defina aqui se a ia desse codigo será o Agente 1 ou 2
# ==========================================
MEU_AGENTE = AGENTE_2  # Mude para AGENTE_1 se a IA desse codigo for a primeira a jogar se nao mude para AGENTE_2 

if __name__ == "__main__":
    print("=== Batalha de IAs - Iniciando Partida ===")
    print("O terminal ficará aberto até o fim do jogo.")
    agente_ia = AgenteIA(MEU_AGENTE)
    nome_arquivo = "saida_tabuleiro.txt"
    oponente = AGENTE_1 if MEU_AGENTE == AGENTE_2 else AGENTE_2

    matriz_entrada = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
    ]
    tabuleiro = Tabuleiro(LINHAS, COLUNAS, matriz_entrada)
    print("--- TABULEIRO INICIAL ---")
    tabuleiro.printMatrizCLI()

    if MEU_AGENTE == AGENTE_1:
        print("\nSua IA joga primeiro. Calculando...")
        agente_ia.jogar(tabuleiro)
        diretorio_script = os.path.dirname(os.path.abspath(__file__))
        caminho_arquivo = os.path.join(diretorio_script, "saida_tabuleiro.txt")
        with open(caminho_arquivo, "w") as arquivo:
            arquivo.write(str(tabuleiro.getMatriz()))
        print("--- VISUALIZAÇÃO DO TABULEIRO PÓS-JOGADA ---")
        tabuleiro.printMatrizCLI()

    while True:
        try:
            print("\n" + "="*50)
            entrada = input(f"Digite a coluna (0 a {COLUNAS - 1}) da jogada do oponente (ou 'sair'):\n> ").strip()
            if entrada.lower() == 'sair':
                print("Encerrando o jogo prematuramente...")
                break
            if not entrada:
                continue
            coluna_oponente = int(entrada)
            if coluna_oponente < 0 or coluna_oponente >= COLUNAS:
                print(f"[ERRO] A coluna deve ser um número entre 0 e {COLUNAS - 1}.")
                continue
            jogada_valida = tabuleiro.posiciona(coluna_oponente, oponente)
            if not jogada_valida:
                print("[ERRO] Essa coluna já está cheia! O oponente precisa escolher outra.")
                continue
            if tabuleiro.verificaEstado(oponente) == VITORIA:
                print("\n💀 FIM DE JOGO: O oponente venceu!")
                tabuleiro.printMatrizCLI()
                break
            elif tabuleiro.verificaEstado(oponente) == EMPATE:
                print("\n🤝 FIM DE JOGO: Empate! O tabuleiro encheu.")
                tabuleiro.printMatrizCLI()
                break
            print("\nSua IA está calculando a jogada...")
            agente_ia.jogar(tabuleiro)
            nova_matriz = tabuleiro.getMatriz()
            diretorio_script = os.path.dirname(os.path.abspath(__file__))
            caminho_arquivo = os.path.join(diretorio_script, "saida_tabuleiro.txt")
            with open(caminho_arquivo, "w") as arquivo:
                arquivo.write(str(nova_matriz))
            print(f"[ OK ] O vetor da nova jogada foi salvo no arquivo: '{caminho_arquivo}'")
            print("--- VISUALIZAÇÃO DO TABULEIRO PÓS-JOGADA ---")
            tabuleiro.printMatrizCLI()
            estado_jogo = tabuleiro.verificaEstado(MEU_AGENTE)
            if estado_jogo == VITORIA:
                print("\n🏆 VITÓRIA! Sua IA ganhou o jogo com essa jogada!")
                break
            elif estado_jogo == EMPATE:
                print("\n🤝 EMPATE! O tabuleiro encheu e ninguém ganhou.")
                break
            print("Aguardando o turno do oponente...")

        except ValueError:
            print(f"\n[ERRO] Entrada inválida! Digite apenas um número inteiro entre 0 e {COLUNAS - 1}.")
        except Exception as e:
            print(f"\n[ERRO] Ocorreu um erro inesperado: {e}")

    input("\nPressione ENTER para fechar a janela...")