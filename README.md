Nomes: Hannah Barreto, Matheus Rocha, Paulo Freitas, Luã Souza e Ricardo Braz

Alunos de Ciência da Computação e Engenharia da Computação

Disciplina: Inteligência Artificial (2025.1) - Prof. Edjard Mota

# Sudoku com Lógica e Heurísticas

Este projeto implementa a classificação e análise de tabuleiros de Sudoku 4x4 utilizando **restrições lógicas**, **heurísticas** e **Logic Tensor Networks (LTN)**. A proposta explora abordagens simbólicas para validar, resolver e analisar Sudokus com e sem solução.

## Objetivo

Resolver e classificar tabuleiros de Sudoku, com base nas seguintes etapas:

1. **Escolher uma forma de representação compatível com LTN**.
2. **Definir um conjunto de heurísticas H**, cuja lógica seja similar às restrições do Sudoku.
3. **Escrever os axiomas em LTN**, conforme exemplos do repositório do [LTNTorch](https://github.com/logictensornetworks/ltntorch).
4. **Ler qualquer tabuleiro via CSV** e realizar as tarefas de verificação, classificação e análise.

## Funcionalidades

- **Classificação de tabuleiros fechados** (completamente preenchidos).
- **Classificação de tabuleiros abertos** (com células vazias), com simulação de possíveis jogadas.
- **Aplicação de heurísticas**:
  - MRV (Minimum Remaining Values)
  - Dígito mais restrito
- **Geração de cláusulas lógicas** representando as heurísticas.
