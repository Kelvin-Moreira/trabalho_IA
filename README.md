# Meta-heurísticas para o TSP: GA vs. SA

Este repositório contém a implementação e a análise comparativa de duas meta-heurísticas fundamentais da Inteligência Artificial — o **Algoritmo Genético (GA)** e o **Simulated Annealing (SA)** — aplicadas à resolução do Problema do Caixeiro Viajante (TSP - *Traveling Salesman Problem*).

O projeto foi desenvolvido como um ambiente de *benchmarking* rigoroso, submetendo ambos os algoritmos a um orçamento computacional estritamente equivalente (~225.000 avaliações da função objetivo) para avaliar o compromisso entre **Eficácia** (capacidade de encontrar o ótimo global) e **Eficiência** (tempo de execução na CPU). O conjunto de testes utiliza a instância simétrica **bays29** (29 cidades da Baviera), cujo ótimo global provado é de `2020.0`.

## 🚀 Como Executar o Benchmarking

1. Clone este repositório.
2. Certifique-se de que a instância `Bays29.txt` está na pasta `/tsp/`.
3. Execute a main.py:
   ```bash
   python main.py