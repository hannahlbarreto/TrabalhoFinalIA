
# 🧠 Analisador Heurístico de Sudoku - Questão 2

Este projeto implementa um analisador heurístico para tabuleiros de Sudoku abertos (incompletos).

O script analisa um ou mais tabuleiros a partir de arquivos `.csv`, classifica o estado atual do jogo e avalia as consequências de movimentos futuros, baseando-se em regras determinísticas para identificar estados sem solução.

---

## 🎯 Heurísticas e Análises Consideradas

O script avalia um tabuleiro aberto com base nas seguintes regras e análises, conforme solicitado na **Questão 2** do trabalho:

- **Classificação de "Sem Solução"**  
  Um tabuleiro é classificado como *Sem Solução* se um dígito válido (1–N) não pode mais ser colocado em nenhuma célula vazia sem violar as regras básicas do Sudoku.

- **Classificação de "Solução Possível"**  
  Se a condição acima não for atendida, o tabuleiro é considerado como tendo *Solução Possível*.

- **Análise de 1 Movimento**  
  Para tabuleiros com solução possível, o script identifica quais jogadas individuais levariam o tabuleiro a um estado de "Sem Solução".

- **Análise de 2 Movimentos**  
  O script também avalia sequências de duas jogadas para determinar se elas levam a um estado de "Sem Solução".

---

## 🛠️ Tecnologias Utilizadas

Este script foi construído com foco em eficiência para a análise determinística, utilizando:

- Python 3.12.3
- NumPy  

Instale a única dependência com:

```bash
pip install numpy
```

---

## 📥 Como Usar

### 1. Estrutura de Pastas

Prepare uma pasta com os tabuleiros de teste:

```
/projeto_ia/
│-- analisador_sudoku.py
│-- /test_boards/
    │-- 4x4_possivel.csv
    │-- 9x9_dificil.csv
```

- Os arquivos devem estar no formato `.csv`
- Podem conter tabuleiros 4x4 ou 9x9
- Use `0` para representar células vazias

### 2. Executar

Execute o script via terminal, passando o caminho da pasta com os tabuleiros como argumento:

```bash
python seu_script.py <caminho_para_a_pasta>
```

Exemplo:

```bash
python analisador_sudoku.py test_boards
```

---

## ⚙️ Lógica Interna

- **Detecção Dinâmica**  
  O script valida o tamanho do tabuleiro lido e adapta-se automaticamente para Sudoku 4x4 ou 9x9.

- **Função `check_sem_solucao`**  
  Núcleo da análise. Para um dado tabuleiro, verifica se todos os dígitos possíveis ainda podem ser jogados legalmente.

- **Funções `evaluate_one_move` e `evaluate_two_moves`**  
  Simulam uma jogada (ou sequência de duas) para verificar se levam a um estado sem solução.

---

## ✅ Análises Realizadas

| Análise                  | Descrição                                               | Status |
|--------------------------|---------------------------------------------------------|--------|
| Classificação Inicial    | "Sem Solução" vs. "Solução Possível"                    | ✅     |
| Análise de 1 Movimento   | Identifica jogadas que levam a um beco sem saída        | ✅     |
| Análise de 2 Movimentos  | Identifica 2 jogadas consecutivas que causam falha      | ✅     |
| Validação de Entrada     | Verifica dimensões e formato do arquivo `.csv`          | ✅     |
| Processamento em Lote    | Analisa todos os `.csv` de uma pasta                    | ✅     |

---

## 📤 Exemplo de Saída

O script gera um relatório claro para cada tabuleiro analisado:

```
Processando arquivos CSV na pasta 'test_boards'...

Lendo o tabuleiro do arquivo 'tabuleiro_A.csv'...
Analisando o tabuleiro: tabuleiro_A.csv...
Tabuleiro Lido:
 [[4 1 0 0]
  [0 0 1 0]
  [0 2 0 0]
  [0 0 3 2]]

--- RELATÓRIO DE ANÁLISE ---
Arquivo: tabuleiro_A.csv
Dimensões: 4x4
Classificação: Solução Possível

[ Análise de 1 Movimento ]
  - Nenhum movimento único leva a um estado 'Sem Solução'.
  - 34 jogadas mantêm o estado de 'Solução Possível'.

[ Análise de 2 Movimentos ]
  - Análise pulada: o tabuleiro está muito aberto e o cálculo seria muito longo.
```
