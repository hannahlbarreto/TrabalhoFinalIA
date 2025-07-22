# Sudoku com Heurísticas — Questão 3 (IA 2025.1)

Este repositório contém a resolução da **Questão 3** do Trabalho Final da disciplina de **Inteligência Artificial (EC034 / ICC265)** — UFAM, 2025.1.

---

## Eunciado

> Indicar para um tabuleiro aberto quais heurísticas são mais recomendadas:
>
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

### 🔹 Pré-requisitos
- Python 3.x
- pandas, numpy

### 🔹 Rodando o script
```bash
python heuristicas_sudoku.py
