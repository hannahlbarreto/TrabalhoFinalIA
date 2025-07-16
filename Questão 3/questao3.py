import numpy as np
import pandas as pd

N = 4
block_size = 2

def load_board_from_csv(path):
    df = pd.read_csv(path, header=None)
    return df.values.astype(int)

def initialize_binary_variables(board):
    binary_vars = np.zeros((N, N, N), dtype=int)
    for i in range(N):
        for j in range(N):
            num = board[i, j]
            if num != 0:
                binary_vars[i, j, num - 1] = 1
    return binary_vars

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

def heuristic_mrv(binary_vars):
    cell_options = []
    for i in range(N):
        for j in range(N):
            if np.sum(binary_vars[i, j, :]) == 0:
                options = [k+1 for k in range(N) if is_valid(binary_vars, i, j, k+1)]
                cell_options.append(((i, j), options))
    cell_options.sort(key=lambda x: len(x[1]))
    return cell_options

def heuristic_most_constrained_digit(binary_vars):
    digit_spaces = {}
    for num in range(1, N+1):
        count = 0
        for i in range(N):
            for j in range(N):
                if np.sum(binary_vars[i, j, :]) == 0 and is_valid(binary_vars, i, j, num):
                    count += 1
        digit_spaces[num] = count
    sorted_digits = sorted(digit_spaces.items(), key=lambda x: x[1])
    return sorted_digits

def aplicar_heuristicas(csv_path):
    board = load_board_from_csv(csv_path)
    binary_vars = initialize_binary_variables(board)

    print("Tabuleiro carregado:\n", board)

    print("\n Heurística MRV:")
    mrv = heuristic_mrv(binary_vars)
    for (i, j), opts in mrv[:5]:
        print(f"Célula ({i},{j}) → {len(opts)} possibilidade(s): {opts}")

    print("\n Heurística 'Dígito mais restrito':")
    digits = heuristic_most_constrained_digit(binary_vars)
    for d, count in digits[:4]:
        print(f"Dígito {d} → {count} posição(ões) possíveis")

if __name__ == "__main__":
    aplicar_heuristicas("sudoku_aberto.csv")

