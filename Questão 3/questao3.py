import numpy as np
import pandas as pd
import os
import sys

# Parâmetros do Sudoku 4x4
N = 4
block_size = 2

# Carrega o tabuleiro a partir de um CSV
def load_board_from_csv(path):
    df = pd.read_csv(path, header=None)
    return df.values.astype(int)

# Inicializa variáveis binárias 3D indicando onde estão os números
def initialize_binary_variables(board):
    binary_vars = np.zeros((N, N, N), dtype=int)
    for i in range(N):
        for j in range(N):
            num = board[i, j]
            if num != 0:
                binary_vars[i, j, num - 1] = 1
    return binary_vars

# Verifica se um número pode ser inserido em uma posição
def is_valid(binary_vars, row, col, num):
    if np.sum(binary_vars[row, :, num - 1]) > 0:
        return False
    if np.sum(binary_vars[:, col, num - 1]) > 0:
        return False
    block_row_start = (row // block_size) * block_size
    block_col_start = (col // block_size) * block_size
    if np.sum(binary_vars[block_row_start:block_row_start + block_size,
                          block_col_start:block_col_start + block_size, num - 1]) > 0:
        return False
    return True

# Heurística MRV (Menor número de valores restantes)
def heuristic_mrv(binary_vars):
    cell_options = []
    for i in range(N):
        for j in range(N):
            if np.sum(binary_vars[i, j, :]) == 0:
                options = [k+1 for k in range(N) if is_valid(binary_vars, i, j, k+1)]
                cell_options.append(((i, j), options))
    cell_options.sort(key=lambda x: len(x[1]))  # Ordena pela quantidade de opções
    return cell_options

# Heurística "Dígito mais restrito" (menos posições possíveis para o número)
def heuristic_most_constrained_digit(binary_vars):
    digit_spaces = {}
    for num in range(1, N+1):
        count = 0
        for i in range(N):
            for j in range(N):
                if np.sum(binary_vars[i, j, :]) == 0 and is_valid(binary_vars, i, j, num):
                    count += 1
        digit_spaces[num] = count
    sorted_digits = sorted(digit_spaces.items(), key=lambda x: x[1])  # Crescente
    return sorted_digits

# Aplica as heurísticas ao tabuleiro carregado
def aplicar_heuristicas(csv_path):
    board = load_board_from_csv(csv_path)
    binary_vars = initialize_binary_variables(board)

    print("Tabuleiro carregado:\n", board)

    print("\nHeurística MRV:")
    mrv = heuristic_mrv(binary_vars)
    for (i, j), opts in mrv[:5]:  # Mostra no máximo 5 células
        print(f"Célula ({i},{j}) → {len(opts)} possibilidade(s): {opts}")

    print("\nHeurística 'Dígito mais restrito':")
    digits = heuristic_most_constrained_digit(binary_vars)
    for d, count in digits[:4]:  # Mostra no máximo 4 dígitos
        print(f"Dígito {d} → {count} posição(ões) possíveis")

# Execução principal com argumentos via terminal
if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_directory_path = sys.argv[1]
        for filename in os.listdir(test_directory_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(test_directory_path, filename)
                print(f"\n--- Arquivo: {filename} ---")
                aplicar_heuristicas(file_path)
    else:
        print("Usage: python questao3.py <directory_path>")
        print("Please provide the path to the directory containing Sudoku board CSV files.")
