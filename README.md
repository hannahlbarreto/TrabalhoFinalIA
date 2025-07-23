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
Tabuleiro carregado:

[[1 0 0 2]

[0 0 0 4]

[4 0 2 0]

[0 0 0 1]]

Epoch 0 - SAT: MRV=0.401, Restrito=0.353

Epoch 10 - SAT: MRV=0.472, Restrito=0.437

Epoch 20 - SAT: MRV=0.563, Restrito=0.519

Epoch 30 - SAT: MRV=0.618, Restrito=0.588

Epoch 40 - SAT: MRV=0.669, Restrito=0.632

Epoch 50 - SAT: MRV=0.712, Restrito=0.691

Epoch 60 - SAT: MRV=0.754, Restrito=0.725

Epoch 70 - SAT: MRV=0.779, Restrito=0.761

Epoch 80 - SAT: MRV=0.812, Restrito=0.786

Epoch 90 - SAT: MRV=0.839, Restrito=0.811
```
