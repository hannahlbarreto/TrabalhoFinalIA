# Sudoku com Heurísticas — Questão 3 (IA 2025.1)

A resolução da **Questão 3** do Trabalho Final da disciplina de **Inteligência Artificial (EC034 / ICC265)** — UFAM, 2025.1.

---

## Enunciado

> Indicar para um tabuleiro aberto quais heurísticas são mais recomendadas:

> 1. Escolha conjuntos de heurísticas e compare o uso delas  
> 2. Gere cláusulas para elas e insira no problema  
> 3. Rode um SAT-solver ou outro solucionador do Sudoku que leia restrições lógicas + heurísticas  
> 4. Responda: Seria possível resolver o Sudoku com LTN?

---

## Heurísticas Implementadas

### 1. **MRV (Minimum Remaining Values)**
Prioriza a célula com **menor número de valores possíveis**.

### 2. **Dígito mais restrito**
Prioriza o número que **possui menos locais válidos** para ser jogado.

---

## Cláusulas (Axiomas)

As heurísticas foram representadas como **restrições lógicas**, inspiradas no modelo de Logic Tensor Networks (LTNs):

- **Axioma 1 (MRV):**  
  _Se uma célula possui apenas uma possibilidade, deve receber esse valor._

- **Axioma 2 (Mais restrito):**  
  _Se um dígito pode ser alocado em apenas uma célula, ele deve ser alocado._

---

## Execução

### Pré-requisitos
- Python 3.x
- pandas, numpy

### Rodando o script
python questão3.py (certifique que o sudoku_aberto.csv está na mesma pasta)

---

## Exemplo de saída

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

Esses valores indicam o grau de satisfação das restrições lógicas aprendidas com as heurísticas. 

---

## Sobre resolver Sudoku com LTN

A aplicação de Logic Tensor Networks ao Sudoku é possível e foi baseada no artigo: “Designing Logic Tensor Networks for Visual Sudoku puzzle classification” (Morra et al., 2023)
No entanto, a abordagem LTN:
> Depende de definições precisas de predicados e cláusulas lógicas
> Enfrenta dificuldades de escalabilidade para tabuleiros maiores
> É boa para classificar e aprender restrições, mas não substitui um SAT solver se a meta for encontrar a solução exata
