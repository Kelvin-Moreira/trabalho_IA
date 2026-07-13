import os
import ast
from defines import *
from tabuleiro import Tabuleiro
from agenteIA import AgenteIA

# ==========================================
# CONFIGURAÇÃO DA IA
# Defina aqui se a ia desse codigo será o Agente 1 ou 2
# ==========================================
MEU_AGENTE = AGENTE_2  # Mude para AGENTE_1 se a IA desse codigo for a primeira a jogar

if __name__ == "__main__":
    print("=== Batalha de IAs - Iniciando Partida ===")
    print("O terminal ficará aberto até o fim do jogo.")
    
    agente_ia = AgenteIA(MEU_AGENTE)
    nome_arquivo = "saida_tabuleiro.txt"
    
    # Identifica o oponente para as validações
    oponente = AGENTE_1 if MEU_AGENTE == AGENTE_2 else AGENTE_2



    if MEU_AGENTE == AGENTE_1:
        matriz_entrada= [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
        tabuleiro = Tabuleiro(LINHAS, COLUNAS, matriz_entrada)
        agente_ia.jogar(tabuleiro)
        tabuleiro.printMatrizCLI()

    # O laço 'while True' mantém o programa rodando turnos infinitos até alguém ganhar
    while True:
        try:
            print("\n" + "="*50)
            entrada = input("Cole o vetor do tabuleiro (ou digite 'sair' para encerrar):\n> ").strip()
            
            # Condição de saída manual
            if entrada.lower() == 'sair':
                print("Encerrando o jogo prematuramente...")
                break
                
            if not entrada:
                continue

            # Converte a string recebida para matriz do Python
            matriz_entrada = ast.literal_eval(entrada)
            
            # Validação de tamanho
            if len(matriz_entrada) != LINHAS or len(matriz_entrada[0]) != COLUNAS:
                print(f"Erro: O tabuleiro precisa ter {LINHAS} linhas e {COLUNAS} colunas.")
                continue
                
            tabuleiro = Tabuleiro(LINHAS, COLUNAS, matriz_entrada)
            
            # Verifica se o oponente já ganhou na matriz que você acabou de colar
            if tabuleiro.verificaEstado(oponente) == VITORIA:
                print("\n💀 FIM DE JOGO: O oponente venceu!")
                tabuleiro.printMatrizCLI()
                break # Quebra o loop e vai para o fim do programa

            elif tabuleiro.verificaEstado(oponente) == EMPATE:
                print("\n🤝 FIM DE JOGO: Empate! O tabuleiro encheu.")
                tabuleiro.printMatrizCLI()
                break
                
            print("\nSua IA está calculando a jogada...")
            
            # A IA realiza a jogada e altera o tabuleiro internamente
            agente_ia.jogar(tabuleiro)
            nova_matriz = tabuleiro.getMatriz()
            
            # Salvar no TXT
            diretorio_script = os.path.dirname(os.path.abspath(__file__))
            caminho_arquivo = os.path.join(diretorio_script, "saida_tabuleiro.txt")
            with open(caminho_arquivo, "w") as arquivo:
                arquivo.write(str(nova_matriz))
                
            print(f"[ OK ] O vetor da nova jogada foi salvo no arquivo: '{caminho_arquivo}'")
            
            # Mostrar o visual no terminal
            print("--- VISUALIZAÇÃO DO TABULEIRO PÓS-JOGADA ---")
            tabuleiro.printMatrizCLI()
            
            # Verifica se a IA ganhou ou empatou após essa jogada
            estado_jogo = tabuleiro.verificaEstado(MEU_AGENTE)
            if estado_jogo == VITORIA:
                print("\n🏆 VITÓRIA! Sua IA ganhou o jogo com essa jogada!")
                break 
            elif estado_jogo == EMPATE:
                print("\n🤝 EMPATE! O tabuleiro encheu e ninguém ganhou.")
                break
                
            print("Aguardando o turno do oponente...")

        except (ValueError, SyntaxError):
            print("\n[ERRO] Formato de vetor inválido! Cole apenas uma única linha do tipo [[0,0...], ...]")
        except Exception as e:
            print(f"\n[ERRO] Ocorreu um erro inesperado: {e}")
            
    input("\nPressione ENTER para fechar a janela...")