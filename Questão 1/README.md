
# ✅ Classificação de Tabuleiros de Sudoku com Logic Tensor Networks (LTN)

Este projeto implementa um **classificador lógico para tabuleiros de Sudoku**, utilizando **Logic Tensor Networks (LTN)** com **PyTorch**, capaz de verificar se um tabuleiro preenchido é **válido** (`1`) ou **inválido** (`0`), baseado unicamente em regras simbólicas da lógica de primeira ordem.

---

## 🧠 Regras Consideradas

O tabuleiro é considerado **válido** se:

- Cada número aparece **exatamente uma vez por linha**
- Cada número aparece **exatamente uma vez por coluna**
- Cada número aparece **exatamente uma vez por subquadrado**
- Cada célula contém **um único número entre 1 e N** (onde N é o tamanho do tabuleiro)

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.8+](https://www.python.org)
- [PyTorch](https://pytorch.org)
- [LTN-Torch](https://github.com/logictensornetworks/ltn)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)

Instale as dependências com:

```bash
pip install torch pandas numpy ltn-torch
```

---

## 📥 Como Usar

1. **Prepare seu tabuleiro Sudoku como um arquivo CSV**:

Exemplo 4x4:

```csv
1,2,3,4
3,4,1,2
2,1,4,3
4,3,2,1
```

Exemplo 9x9:

```csv
5,3,4,6,7,8,9,1,2
6,7,2,1,9,5,3,4,8
1,9,8,3,4,2,5,6,7
8,5,9,7,6,1,4,2,3
4,2,6,8,5,3,7,9,1
7,1,3,9,2,4,8,5,6
9,6,1,5,3,7,2,8,4
2,8,7,4,1,9,6,3,5
3,4,5,2,8,6,1,7,9
```

2. **Chame a função de classificação**:

```python
result = classify_sudoku("caminho/para/arquivo.csv")
print("✅ Válido" if result == 1 else "❌ Inválido")
```

---

## ⚙️ Lógica Interna

- O tabuleiro é transformado em um tensor 3D `torch.Tensor` com codificação one-hot.
- Quatro **predicados** lógicos são usados:
  - `HasNumber(r, c, n)` — célula contém o número `n`
  - `IsFilled(r, c)` — célula tem exatamente um número
- Quatro funções avaliam a satisfação lógica:
  - Linhas
  - Colunas
  - Subquadrados
  - Células com número único

A classificação final é baseada na média das satisfações:

```python
overall = mean([row_sat, col_sat, square_sat, heuristic_sat])
```

Com um limiar de 0.99:

```python
if overall >= 0.99:
    return 1  # válido
else:
    return 0  # inválido
```

---

## ✅ Casos de Teste Incluídos

| Teste                           | Esperado | Status |
|--------------------------------|----------|--------|
| Sudoku 4x4 válido              | 1        | ✅      |
| Sudoku 9x9 válido              | 1        | ✅      |
| Duplicata em linha             | 0        | ✅      |
| Duplicata em coluna            | 0        | ✅      |
| Duplicata em subquadrado       | 0        | ✅      |
| Número fora do intervalo       | 0        | ✅      |
| Valor não numérico             | 0        | ✅      |
| Tamanho inválido (3x3, 4x5)     | 0        | ✅      |
| Arquivo inexistente            | 0        | ✅      |

---

## 📥 Como Usar

1. **Prepare seu tabuleiro Sudoku como um arquivo CSV**:

Exemplo 4x4:

```csv
1,2,3,4
3,4,1,2
2,1,4,3
4,3,2,1
```

Exemplo 9x9:

```csv
5,3,4,6,7,8,9,1,2
6,7,2,1,9,5,3,4,8
1,9,8,3,4,2,5,6,7
8,5,9,7,6,1,4,2,3
4,2,6,8,5,3,7,9,1
7,1,3,9,2,4,8,5,6
9,6,1,5,3,7,2,8,4
2,8,7,4,1,9,6,3,5
3,4,5,2,8,6,1,7,9
```

2. **Chame a função de classificação**:

- Para um único tabuleiro:

```python
result = classify_sudoku("caminho/para/arquivo.csv")
print("✅ Válido" if result == 1 else "❌ Inválido")
```

- Para classificar todos os arquivos `.csv` dentro de uma pasta:

```python
import os

test_dir = "caminho/para/pasta_com_csvs"

print(f"Classifying all CSV files in '{test_dir}':")
for filename in os.listdir(test_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(test_dir, filename)
        classification_result = classify_sudoku(file_path)
        print(f"File: {filename}, Classification Result: {classification_result}")
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

---

## 🧩 Referências

- [LTN-Torch GitHub](https://github.com/logictensornetworks/ltn)
- `LTN: Learning with Soft Logic and Neural Networks`, Donadello et al., 2017

---
