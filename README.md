# Algoritmo Genético com Order Crossover (OX) para o Problema do Caixeiro Viajante

Este projeto implementa um **Algoritmo Genético (Genetic Algorithm - GA)** para resolver o **Problema do Caixeiro Viajante (Travelling Salesman Problem - TSP)**, um dos problemas clássicos de otimização combinatória.

O algoritmo representa cada solução como uma permutação das cidades e utiliza o **Order Crossover (OX)** como operador de cruzamento, preservando a ordem relativa das cidades entre os indivíduos. A seleção dos pais é realizada por **torneio**, a diversidade da população é mantida por **mutação por inversão (Inversion Mutation)** e o melhor indivíduo de cada geração é preservado por meio de **elitismo**.

A implementação foi desenvolvida de forma modular, separando as responsabilidades de leitura da instância, operadores genéticos e mecanismo evolutivo, facilitando a manutenção do código e a reutilização de componentes em outros algoritmos, como o **Simulated Annealing (SA)**.

O projeto utiliza como conjunto de testes a instância **bays29**, composta por uma matriz de distâncias entre 29 cidades da Baviera, amplamente utilizada em estudos sobre o TSP.

## Estrutura do projeto

- **utils.py** – Leitura da matriz de distâncias e cálculo do custo das rotas.
- **operadores.py** – Implementação da seleção por torneio, Order Crossover (OX) e mutação por inversão.
- **ga.py** – Implementação do Algoritmo Genético, incluindo população inicial, elitismo e processo evolutivo.
- **main.py** – Ponto de entrada da aplicação, responsável por carregar a instância e executar o algoritmo.

## Objetivo

Este projeto foi desenvolvido para fins acadêmicos, com o objetivo de estudar e avaliar o desempenho de um Algoritmo Genético utilizando o operador **Order Crossover (OX)** na resolução do Problema do Caixeiro Viajante, servindo posteriormente como base para comparações com outras metaheurísticas, como o **Simulated Annealing**.
