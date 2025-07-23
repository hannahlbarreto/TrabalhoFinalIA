Nomes: Hannah Barreto, Matheus Rocha, Paulo Freitas, Luã Souza e Ricardo Braz

Alunos de Ciência da Computação e Engenharia da Computação

Disciplina: Inteligência Artificial (2025.1) - Prof. Edjard Mota

# ✅ Classificação de Tabuleiros de Sudoku com Logic Tensor Networks (LTN) - Questão 1

## 📥 Como Usar

Execute o script via terminal, passando o caminho da pasta com os tabuleiros como argumento:

```bash
python questao1.py /caminho/para/pasta
```

---
## 📤 Exemplo de Saída

```
--- Testing correct_4x4_sudoku.csv ---
Computed Overall Satisfaction: 1.0
Classification Result: 1 (Expected: 1)

--- Testing incorrect_4x4_row_sudoku.csv ---
Computed Overall Satisfaction: 0.75
Classification Result: 0 (Expected: 0)
```

# ✅ Analisador Híbrido de Sudoku com LTN - Questão 2

## 📥 Como Usar

Execute o script via terminal, passando o caminho da pasta com os tabuleiros como argumento:

```bash
python questao2.py /caminho/para/pasta
```

## 📤 Exemplo de Saída

O script gera uma análise completa por tabuleiro:

```
--- Processando arquivo: possivel_9x9.csv ---
Tabuleiro Lido:
 [[5 3 0 ... 0 0 0]
  [6 0 0 ... 0 0 0]
  ...
  [0 0 0 ... 0 7 9]]

--- RELATÓRIO DE ANÁLISE ---
Classificação: Solução Possível

[ Análise de Movimentos com LTN (1 passo) ]
  - Jogadas com maior probabilidade de manter a solução:
    - Jogar 2 em (0,2) -> Score: 0.9871
    - Jogar 4 em (0,3) -> Score: 0.9855
    - Jogar 9 em (0,6) -> Score: 0.9849
    - Jogar 1 em (0,7) -> Score: 0.9842
    - Jogar 8 em (0,5) -> Score: 0.9833

  - Jogadas com menor probabilidade:
    - Jogar 7 em (1,1) -> Score: 0.1542
    - Jogar 3 em (3,8) -> Score: 0.1498
    - Jogar 8 em (2,1) -> Score: 0.1301
    - Jogar 1 em (4,8) -> Score: 0.1129
    - Jogar 9 em (7,3) -> Score: 0.0875
```
---

# ✅ Sudoku com Heurísticas - Questão 3

## 📥 Como Usar

Execute o script via terminal, passando o caminho da pasta com os tabuleiros como argumento:

```bash
python questao3.py /caminho/para/pasta
```

## 📤 Exemplo de Saída
```
--- Arquivo: sudoku_aberto.csv ---
Tabuleiro carregado:
 [[1 0 0 2]
 [0 0 0 4]
 [4 0 2 0]
 [0 0 0 1]]

Heurística MRV:
Célula (0,2) → 1 possibilidade(s): [3]
Célula (2,3) → 1 possibilidade(s): [3]
Célula (0,1) → 2 possibilidade(s): [3, 4]
Célula (1,0) → 2 possibilidade(s): [2, 3]
Célula (1,1) → 2 possibilidade(s): [2, 3]

Heurística 'Dígito mais restrito':
Dígito 1 → 2 posição(ões) possíveis
Dígito 4 → 2 posição(ões) possíveis
Dígito 2 → 4 posição(ões) possíveis
Dígito 3 → 10 posição(ões) possíveis
```

## Sobre resolver Sudoku com LTN

A aplicação de Logic Tensor Networks ao Sudoku é possível e foi baseada no artigo: “Designing Logic Tensor Networks for Visual Sudoku puzzle classification” (Morra et al., 2023) No entanto, a abordagem LTN:

Depende de definições precisas de predicados e cláusulas lógicas Enfrenta dificuldades de escalabilidade para tabuleiros maiores É boa para classificar e aprender restrições, mas não substitui um SAT solver se a meta for encontrar a solução exata

