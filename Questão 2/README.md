
# 🧠 Analisador Híbrido de Sudoku com LTN - Questão 2

Este projeto implementa uma **solução neuro-simbólica híbrida** para a **Questão 2** do Trabalho Final de Inteligência Artificial.

O script `questao2.py` combina uma **verificação heurística determinística** com uma **análise probabilística** baseada em redes neurais treinadas com **Logic Tensor Networks (LTN)**, oferecendo uma abordagem completa para avaliação de tabuleiros abertos de Sudoku.

---

## 🎯 Heurística + Lógica Tensorial

A análise é feita em duas etapas principais:

- **Filtro Heurístico (Determinístico)**  
  Aplica a regra de "Sem Solução" do enunciado. Se não há mais jogadas possíveis para algum dígito válido em células vazias, o tabuleiro é classificado como *Sem Solução* e a análise termina.

- **Análise de Movimentos com LTN (Probabilística)**  
  Se o tabuleiro é considerado *Solução Possível*, o script usa um modelo treinado com LTN para:

  - Atribuir um **score de solvabilidade (0.0 a 1.0)** para cada jogada.
  - **Rankear as jogadas** com base nas que mais contribuem para uma solução válida.

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi desenvolvido utilizando:

- Python 3.12.3
- NumPy  
- PyTorch (com suporte a GPU CUDA, se disponível)  
- LTNtorch  

Para instalar as dependências:

```bash
pip install numpy torch ltntorch
```

---

## 📥 Como Usar

### 1. Estrutura de Pastas

Organize o projeto da seguinte forma:

```
/projeto_ia/
│-- questao2.py
│-- /test_boards/
    │-- 4x4_possivel.csv
    │-- 9x9_dificil.csv
```

- Os arquivos devem estar no formato `.csv`
- Os tabuleiros podem ser de tamanho misto (4x4 e 9x9)
- Use `0` para representar células vazias

### 2. Executar

Execute o script via terminal, passando o caminho da pasta com os tabuleiros como argumento:

```bash
python questao2.py <caminho_para_a_pasta>
```

Exemplo:

```bash
python questao2.py test_boards
```

---

## ⚙️ Lógica Interna

- **Detecção de Tamanho**  
  O script identifica automaticamente o tamanho dos tabuleiros e organiza o fluxo de análise.

- **Treinamento LTN**  
  Um modelo LTN específico (para 4x4 ou 9x9) é treinado com base em axiomas para distinguir tabuleiros bons e ruins.

- **Processamento Individual**  
  Cada tabuleiro é processado da seguinte forma:
  1. Passa pelo filtro heurístico.
  2. Se aplicável, é avaliado por um modelo LTN para ranqueamento de jogadas.
  3. Um relatório detalhado é gerado.

---

## ✅ Funcionalidades Implementadas

| Funcionalidade            | Descrição                                                            | Status |
|---------------------------|----------------------------------------------------------------------|--------|
| Análise Híbrida           | Combinação de lógica heurística com redes neurais LTN                | ✅     |
| Score de Solvabilidade    | Avaliação probabilística por jogada                                  | ✅     |
| Treinamento Automático    | Treinamento de modelos LTN por tamanho de tabuleiro                  | ✅     |
| Processamento em Lote     | Processa automaticamente todos os `.csv` de uma pasta                | ✅     |
| Aceleração com GPU        | Suporte automático a CUDA (se disponível)                            | ✅     |

---

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

## 📚 Referências

- [LTNTorch](https://github.com/logictensornetworks/ltntorch)
- [LTN: Learning with Soft Logic and Neural Networks](https://www.researchgate.net/profile/Marco-Russo-12/), Morra et al., 2023
