"""
Comparativo GA (AG + OX) vs SA (SA + 2-opt) no Problema do Caixeiro Viajante
Lê os dados diretamente de um arquivo de log de benchmarking (texto) e gera
um gráfico de linha comparando o custo de cada execução dos dois algoritmos.

Uso:
    python comparativo_ga_sa.py caminho/para/log_batalha_1.txt

Se nenhum caminho for informado, usa o padrão definido em LOG_PATH.
"""

import re
import statistics
import sys
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Caminho padrão do log (pode ser sobrescrito via argumento de linha de comando)
# ----------------------------------------------------------------------------
LOG_PATH = "teste_comparativo/log_batalha_3.txt"

# Cabeçalhos que marcam o início de cada seção no log
MARCADOR_GA = "ALGORITMO GENÉTICO"
MARCADOR_SA = "SIMULATED ANNEALING"

# Regex para capturar "Teste NN | Custo: XXXX.X | Tempo: YYYY s | ..."
PADRAO_TESTE = re.compile(
    r"Teste\s+\d+\s*\|\s*Custo:\s*([\d.]+)\s*\|\s*Tempo:\s*([\d.]+)"
)

# Regex para capturar o ótimo global, se presente no log
PADRAO_OTIMO = re.compile(r"Ótimo global.*?:\s*([\d.]+)")


def extrair_dados(caminho_log):
    """Lê o log e retorna (custo_ga, tempo_ga, custo_sa, tempo_sa, otimo)."""
    with open(caminho_log, "r", encoding="utf-8") as f:
        conteudo = f.read()

    # Divide o conteúdo nas seções GA e SA usando os cabeçalhos como âncora
    idx_ga = conteudo.find(MARCADOR_GA)
    idx_sa = conteudo.find(MARCADOR_SA)

    if idx_ga == -1 or idx_sa == -1:
        raise ValueError(
            "Não foi possível localizar as seções do GA e/ou SA no log. "
            "Verifique se os marcadores de fase estão presentes."
        )

    if idx_ga < idx_sa:
        secao_ga = conteudo[idx_ga:idx_sa]
        secao_sa = conteudo[idx_sa:]
    else:
        secao_sa = conteudo[idx_sa:idx_ga]
        secao_ga = conteudo[idx_ga:]

    custo_ga = [float(m[0]) for m in PADRAO_TESTE.findall(secao_ga)]
    tempo_ga = [float(m[1]) for m in PADRAO_TESTE.findall(secao_ga)]
    custo_sa = [float(m[0]) for m in PADRAO_TESTE.findall(secao_sa)]
    tempo_sa = [float(m[1]) for m in PADRAO_TESTE.findall(secao_sa)]

    if not custo_ga or not custo_sa:
        raise ValueError("Nenhum dado de teste foi encontrado em uma das seções.")

    otimo_match = PADRAO_OTIMO.search(conteudo)
    otimo = float(otimo_match.group(1)) if otimo_match else None

    return custo_ga, tempo_ga, custo_sa, tempo_sa, otimo


def calcular_estatisticas(custo, tempo):
    """Retorna um dicionário com média de custo, desvio padrão de custo e tempo médio."""
    return {
        "custo_medio": statistics.mean(custo),
        "custo_desvio": statistics.pstdev(custo),
        "tempo_medio": statistics.mean(tempo),
    }


def gerar_grafico(custo_ga, tempo_ga, custo_sa, tempo_sa, otimo,
                   caminho_saida="comparativo_ga_sa_teste3.png"):
    testes = list(range(1, len(custo_ga) + 1))

    stats_ga = calcular_estatisticas(custo_ga, tempo_ga)
    stats_sa = calcular_estatisticas(custo_sa, tempo_sa)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(testes, custo_ga, marker='o', linewidth=2, color='#d62728',
             label=f'AG + OX (média: {stats_ga["custo_medio"]:.1f})')
    ax.plot(testes, custo_sa, marker='s', linewidth=2, color='#1f77b4',
             label=f'SA + 2-opt (média: {stats_sa["custo_medio"]:.1f})')

    if otimo is not None:
        ax.axhline(y=otimo, color='gray', linestyle='--', linewidth=1.2,
                    label=f'Ótimo global ({otimo:.0f})')

    ax.set_title('Comparativo de Custo por Execução — AG + OX vs SA + 2-opt',
                  fontsize=13, fontweight='bold')
    ax.set_xlabel('Número do teste')
    ax.set_ylabel('Custo da rota')
    ax.set_xticks(testes)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right')

    # Caixa de texto com Tempo Médio e Desvio Padrão de cada algoritmo
    texto_stats = (
        "Estatísticas adicionais\n"
        "————————————————\n"
        f"AG + OX     | Tempo médio: {stats_ga['tempo_medio']:.4f}s | "
        f"Desvio padrão (custo): {stats_ga['custo_desvio']:.2f}\n"
        f"SA + 2-opt  | Tempo médio: {stats_sa['tempo_medio']:.4f}s | "
        f"Desvio padrão (custo): {stats_sa['custo_desvio']:.2f}"
    )
    fig.text(0.5, -0.02, texto_stats, ha='center', va='top', fontsize=9,
              family='monospace',
              bbox=dict(boxstyle='round', facecolor='#f0f0f0', edgecolor='gray'))

    fig.tight_layout()
    fig.savefig(caminho_saida, dpi=150, bbox_inches='tight')
    print(f"Gráfico salvo em {caminho_saida}")

    return stats_ga, stats_sa


if __name__ == "__main__":
    caminho = sys.argv[1] if len(sys.argv) > 1 else LOG_PATH
    custo_ga, tempo_ga, custo_sa, tempo_sa, otimo = extrair_dados(caminho)

    print(f"AG + OX: {len(custo_ga)} testes lidos | custos: {custo_ga}")
    print(f"SA + 2-opt: {len(custo_sa)} testes lidos | custos: {custo_sa}")
    if otimo is not None:
        print(f"Ótimo global encontrado no log: {otimo}")

    stats_ga, stats_sa = gerar_grafico(custo_ga, tempo_ga, custo_sa, tempo_sa, otimo)

    print("\nResumo estatístico")
    print("-------------------")
    print(f"AG + OX     | Tempo médio: {stats_ga['tempo_medio']:.4f}s | "
          f"Desvio padrão (custo): {stats_ga['custo_desvio']:.2f}")
    print(f"SA + 2-opt  | Tempo médio: {stats_sa['tempo_medio']:.4f}s | "
          f"Desvio padrão (custo): {stats_sa['custo_desvio']:.2f}")