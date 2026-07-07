import os
import matplotlib.pyplot as plt

def ler_log_ag(caminho, tam_populacao=150):
    avaliacoes_lista, custos = [], []
    with open(caminho, 'r', encoding='utf-8') as f:
        for linha in f:
            if linha.startswith("Geração"):
                partes = linha.split('|')
                # Extrai a Geração (ex: 100)
                geracao = int(partes[0].split()[1])
                # Extrai o Custo (ex: 2070.0)
                custo = float(partes[1].split(':')[1].strip())
                
                # CÁLCULO CIENTÍFICO: Geração * População
                avaliacoes = geracao * tam_populacao
                
                avaliacoes_lista.append(avaliacoes)
                custos.append(custo)
    return avaliacoes_lista, custos

def ler_log_sa(caminho, iteracoes_por_temp=122):
    avaliacoes_lista, custos = [], []
    with open(caminho, 'r', encoding='utf-8') as f:
        for linha in f:
            if linha.startswith("Ciclo"):
                partes = linha.split('|')
                # Extrai o Ciclo (ex: 100)
                ciclo = int(partes[0].split()[1])
                # Extrai o Custo (ex: 4424.0)
                custo = float(partes[2].split(':')[1].strip())
                
                # CÁLCULO CIENTÍFICO: Ciclo * Iterações na Temperatura
                avaliacoes = ciclo * iteracoes_por_temp
                
                avaliacoes_lista.append(avaliacoes)
                custos.append(custo)
    return avaliacoes_lista, custos

def gerar_grafico_batalha(caminho_ga, caminho_sa, nome_saida="batalha_final_avaliacoes.png"):
    plt.figure(figsize=(10, 6))
    
    # 1. Processar o Algoritmo Genético
    if os.path.exists(caminho_ga):
        avals_ga, custos_ga = ler_log_ag(caminho_ga)
        # Manter o "Zoom" estatístico ignorando a Geração 0 (Avaliação 0)
        # para que o valor de ~5000 não achate as curvas de convergência
        if len(avals_ga) > 1:
            avals_ga = avals_ga[1:]
            custos_ga = custos_ga[1:]
            
        resultado_ga = custos_ga[-1] if custos_ga else 0
        plt.plot(avals_ga, custos_ga, marker='o', markersize=5, color='#d62728', 
                 linewidth=2.5, label=f'Algoritmo Genético (Melhor: {resultado_ga:.0f})')
    else:
        print(f"Erro: Arquivo do GA não encontrado -> {caminho_ga}")

    # 2. Processar o Simulated Annealing
    if os.path.exists(caminho_sa):
        avals_sa, custos_sa = ler_log_sa(caminho_sa)
        # Manter o "Zoom" estatístico ignorando o Ciclo 0 (Avaliação 0)
        if len(avals_sa) > 1:
            avals_sa = avals_sa[1:]
            custos_sa = custos_sa[1:]
            
        resultado_sa = custos_sa[-1] if custos_sa else 0
        plt.plot(avals_sa, custos_sa, marker='s', markersize=5, color='#1f77b4', 
                 linewidth=2.5, label=f'Simulated Annealing (Melhor: {resultado_sa:.0f})')
    else:
        print(f"Erro: Arquivo do SA não encontrado -> {caminho_sa}")

    # 3. Adicionar linha do Ótimo Global
    plt.axhline(y=2020.0, color='black', linestyle='--', linewidth=1.5, label='Ótimo Global (2020.0)')

    # 4. Formatação Acadêmica do Gráfico
    plt.title('Comparação da convergência sob orçamento computacional equivalente (GA vs SA)', fontsize=14, fontweight='bold')
    plt.xlabel('Número de avaliações da função objetivo', fontsize=12)
    plt.ylabel('Custo da Rota', fontsize=12)
    
    # TRUQUE IMPORTANTE: Evita que o Matplotlib transforme 200.000 em "2e5"
    plt.ticklabel_format(style='plain', axis='x')
    
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(fontsize=11, loc='upper right')
    plt.tight_layout()
    
    # 5. Salvar a imagem
    plt.savefig(nome_saida, dpi=300)
    print(f"\n[SUCESSO] Gráfico da batalha final salvo como: {nome_saida}")

if __name__ == "__main__":
    print("Iniciando geração do gráfico da Batalha Final (Por Avaliações)...")
    
    # =========================================================
    # CAMINHOS DOS DOIS LOGS CAMPEÕES
    # =========================================================
    CAMINHO_LOG_GA = "teste_AG\log_execucao_mut_30.txt"   # Campeão do GA
    CAMINHO_LOG_SA = "teste_SA\log_execucao_taxa_995.txt" # Campeão do SA
    
    gerar_grafico_batalha(CAMINHO_LOG_GA, CAMINHO_LOG_SA)