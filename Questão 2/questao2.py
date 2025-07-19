import numpy as np
import sys
import os
import copy

# --- Constantes ---
# BOARD_SIZE e BLOCK_SIZE serão definidos ao carregar cada tabuleiro.
BOARD_SIZE = None
BLOCK_SIZE = None

# --- Funções Auxiliares ---
def set_board_size(board):
    """Define BOARD_SIZE e BLOCK_SIZE com base nas dimensões do tabuleiro."""
    global BOARD_SIZE, BLOCK_SIZE
    BOARD_SIZE = board.shape[0]
    BLOCK_SIZE = int(np.sqrt(BOARD_SIZE))
    if BLOCK_SIZE * BLOCK_SIZE != BOARD_SIZE:
        return False # Not a valid Sudoku board size (e.g., 5x5)
    return True


def violates_constraint(board, move, board_size, block_size):
    """Verifica se uma jogada viola uma regra básica do Sudoku."""
    row, col, digit = move
    # Verifica linha
    if digit in board[row, :]:
        return True
    # Verifica coluna
    if digit in board[:, col]:
        return True
    # Verifica bloco
    start_row, start_col = row - row % block_size, col - col % block_size
    if digit in board[start_row:start_row + block_size, start_col:start_col + block_size]:
        return True
    return False

def get_empty_cells(board, board_size):
    """Retorna uma lista de tuplas (linha, coluna) para células vazias (valor 0)."""
    cells = []
    for r in range(board_size):
        for c in range(board_size):
            if board[r, c] == 0:
                cells.append((r, c))
    return cells

# --- Funções Principais ---
def load_and_validate_board(file_path):
    """
    Carrega o tabuleiro de Sudoku de um arquivo CSV e valida suas dimensões.
    Define BOARD_SIZE e BLOCK_SIZE.
    Retorna o tabuleiro numpy array ou None em caso de erro.
    """
    print(f"\nLendo o tabuleiro do arquivo '{file_path}'...")
    try:
        board = np.loadtxt(file_path, delimiter=',', dtype=int)
        print("Tabuleiro Lido:\n", board)

        # Define e valida as dimensões do tabuleiro
        if not set_board_size(board):
            print(f"ERRO: O tabuleiro no arquivo '{file_path}' tem dimensões {board.shape}, "
                f"que não são válidas para um tabuleiro de Sudoku (apenas 4x4 ou 9x9).")
            return None
        if board.shape[0] != board.shape[1]:
            print(f"ERRO: O tabuleiro no arquivo '{file_path}' tem dimensões não quadradas {board.shape}.")
            return None


        return board

    except IOError:
        print(f"ERRO: Arquivo '{file_path}' não encontrado.")
        return None
    except ValueError:
        print(f"ERRO: O arquivo '{file_path}' não parece ser um CSV válido para o tabuleiro.")
        return None

def check_sem_solucao(board, board_size, block_size):
    """
    Verifica se a condição de 'sem solução' foi atingida no tabuleiro atual.
    Retorna True se for "Sem Solução", False caso contrário.
    """
    empty_cells = get_empty_cells(board, board_size)
    if not empty_cells:
        # Se não há células vazias, o tabuleiro está completo e não é "Sem Solução" por falta de movimentos.
        return False

    for digit_to_check in range(1, board_size + 1):
        can_place_digit = False
        for cell in empty_cells:
            move = (cell[0], cell[1], digit_to_check)
            # Verifica se o dígito pode ser colocado em pelo menos uma célula vazia
            if not violates_constraint(board, move, board_size, block_size):
                can_place_digit = True
                break

        # Se um dígito não pode ser colocado em nenhuma célula vazia, o tabuleiro está em um estado "Sem Solução"
        if not can_place_digit:
            print(f"DIAGNÓSTICO: O dígito '{digit_to_check}' não pode ser colocado em nenhuma célula vazia restante.")
            return True

    # Se todos os dígitos podem ser colocados em pelo menos uma célula vazia, não é "Sem Solução" nesta etapa
    return False


def evaluate_one_move(board, board_size, block_size):
    """
    Avalia o impacto de cada possível movimento (colocar um dígito em uma célula vazia)
    na classificação do tabuleiro ("Sem Solução" ou "Solução Possível").
    Retorna duas listas: movimentos que levam a "Sem Solução" e movimentos que mantêm "Solução Possível".
    """
    empty_cells = get_empty_cells(board, board_size)
    moves_leading_to_sem_solucao = []
    moves_maintaining_solucao_possivel = []

    for row, col in empty_cells:
        for digit in range(1, board_size + 1):
            move = (row, col, digit)

            # Verifica restrições básicas antes de aplicar o movimento
            if violates_constraint(board, move, board_size, block_size):
                continue

            # Cria uma cópia do tabuleiro e aplica o movimento
            copied_board = np.copy(board)
            copied_board[row, col] = digit

            # Verifica se o tabuleiro copiado é "Sem Solução" após o movimento
            # Passa as dimensões do tabuleiro copiado para a função de verificação
            if check_sem_solucao(copied_board, board_size, block_size):
                moves_leading_to_sem_solucao.append(move)
            else:
                moves_maintaining_solucao_possivel.append(move)


    return moves_leading_to_sem_solucao, moves_maintaining_solucao_possivel

def evaluate_two_moves(board, board_size, block_size):
    """
    Avalia o impacto de sequências de dois movimentos na classificação do tabuleiro.
    Retorna duas listas de sequências de dois movimentos: aquelas que levam a "Sem Solução"
    e aquelas que mantêm "Solução Possível".
    """
    empty_cells = get_empty_cells(board, board_size)
    two_moves_leading_to_sem_solucao = []
    two_moves_maintaining_solucao_possivel = []

    # Itera sobre cada possível primeiro movimento
    for r1, c1 in empty_cells:
        for d1 in range(1, board_size + 1):
            first_move = (r1, c1, d1)

            # Verifica restrições básicas para o primeiro movimento
            if violates_constraint(board, first_move, board_size, block_size):
                continue

            # Cria uma cópia profunda do tabuleiro e aplica o primeiro movimento
            board_after_first_move = copy.deepcopy(board)
            board_after_first_move[r1, c1] = d1

            # Verifica se o tabuleiro após o primeiro movimento já é "Sem Solução"
            if check_sem_solucao(board_after_first_move, board_size, block_size):
                # Se o primeiro movimento isoladamente leva a "Sem Solução", registra e continua
                # Podemos registrar a sequência como levando a "Sem Solução" após 1 passo.
                # Para a análise de 2 passos, não precisamos explorar segundos movimentos.
                # two_moves_leading_to_sem_solucao.append((first_move, "Any second move leads to Sem Solução"))
                continue

            # Se o tabuleiro após o primeiro movimento não é "Sem Solução", avalia possíveis segundos movimentos
            empty_cells_after_first_move = get_empty_cells(board_after_first_move, board_size)

            # Itera sobre cada possível segundo movimento
            for r2, c2 in empty_cells_after_first_move:
                for d2 in range(1, board_size + 1):
                    second_move = (r2, c2, d2)

                    # Verifica restrições básicas para o segundo movimento no tabuleiro após o primeiro movimento
                    if violates_constraint(board_after_first_move, second_move, board_size, block_size):
                        continue

                    # Cria outra cópia profunda do tabuleiro (a partir do estado após o primeiro movimento) e aplica o segundo movimento
                    board_after_two_moves = copy.deepcopy(board_after_first_move)
                    board_after_two_moves[r2, c2] = d2

                    # Verifica se o tabuleiro após os dois movimentos é "Sem Solução"
                    if check_sem_solucao(board_after_two_moves, board_size, block_size):
                        two_moves_leading_to_sem_solucao.append((first_move, second_move))
                    else:
                        two_moves_maintaining_solucao_possivel.append((first_move, second_move))


    return two_moves_leading_to_sem_solucao, two_moves_maintaining_solucao_possivel


def analyze_sudoku(board, file_name):
    """
    Realiza a análise completa do tabuleiro de Sudoku, classificando-o e avaliando heurísticas.
    """
    print(f"\nAnalisando o tabuleiro: {file_name}...")

    # Use the global BOARD_SIZE and BLOCK_SIZE set by load_and_validate_board
    is_sem_solucao = check_sem_solucao(board, BOARD_SIZE, BLOCK_SIZE)

    print("\n--- RESULTADO DA CLASSIFICAÇÃO ---")
    if is_sem_solucao:
        print(f"Classificação para '{file_name}': Sem Solução")
    else:
        print(f"Classificação para '{file_name}': Solução Possível")

        # Avaliação de movimentos em um passo
        print("\n--- AVALIAÇÃO DE MOVIMENTOS EM UM PASSO ---")
        moves_leading_to_sem_solucao_one_step, moves_maintaining_solucao_possivel_one_step = evaluate_one_move(board, BOARD_SIZE, BLOCK_SIZE)
        print(f"Movimentos que levam a 'Sem Solução': {moves_leading_to_sem_solucao_one_step}")
        print(f"Movimentos que mantêm 'Solução Possível': {moves_maintaining_solucao_possivel_one_step}")

        # Avaliação de sequências de dois movimentos
        print("\n--- AVALIAÇÃO DE SEQUÊNCIAS DE DOIS MOVIMENTOS ---")
        two_moves_leading_to_sem_solucao, two_moves_maintaining_solucao_possivel = evaluate_two_moves(board, BOARD_SIZE, BLOCK_SIZE)
        print(f"Sequências de dois movimentos que levam a 'Sem Solução': {two_moves_leading_to_sem_solucao}")
        print(f"Sequências de dois movimentos que mantêm 'Solução Possível': {two_moves_maintaining_solucao_possivel}")


# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    # Em um Jupyter Notebook, sys.argv não é usado para argumentos de linha de comando.
    # Vamos simular a leitura de um caminho de diretório.
    
    if len(sys.argv) != 2:
        print("ERRO: Você precisa especificar o caminho para a pasta de tabuleiros.")
        print("Uso: python main.py <caminho_para_a_pasta>")
        exit()
        directory_path = sys.argv[1]

    # Para execução em notebook, defina o caminho da pasta aqui
    # Certifique-se de que a pasta 'test_boards' exista e contenha os arquivos CSV
    directory_path = 'test_boards' # Pasta de exemplo com os arquivos CSV

    if not os.path.isdir(directory_path):
        print(f"ERRO: O caminho '{directory_path}' não é um diretório válido.")
        # Para execução em notebook, podemos tentar criar um diretório de exemplo e alguns arquivos.
        print("Criando diretório de exemplo e arquivos de tabuleiro para demonstração.")
        os.makedirs(directory_path, exist_ok=True)
        # Create some dummy board files for demonstration in the notebook
        # Create a 4x4 solvable board
        board_solucao_possivel_4x4_empty = np.zeros((4, 4), dtype=int)
        np.savetxt(os.path.join(directory_path, 'tabuleiro_solucao_possivel_4x4.csv'), board_solucao_possivel_4x4_empty, delimiter=',', fmt='%d')

        # Create a truly unsolvable 4x4 board
        board_sem_solucao_4x4_v6 = np.array([
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])
        np.savetxt(os.path.join(directory_path, 'tabuleiro_sem_solucao_4x4.csv'), board_sem_solucao_4x4_v6, delimiter=',', fmt='%d')

        # Create a 9x9 solvable board (a simple one)
        board_solucao_possivel_9x9 = np.array([
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ])
        np.savetxt(os.path.join(directory_path, 'tabuleiro_solucao_possivel_9x9.csv'), board_solucao_possivel_9x9, delimiter=',', fmt='%d')

        # Create a 9x9 unsolvable board
        board_sem_solucao_9x9 = np.array([
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 0] # Empty cell at (8,8) where 1-9 are blocked
        ])
        np.savetxt(os.path.join(directory_path, 'tabuleiro_sem_solucao_9x9.csv'), board_sem_solucao_9x9, delimiter=',', fmt='%d')
        print(f"Diretório '{directory_path}' criado com arquivos de exemplo.")
        exit()

    print(f"\nProcessando arquivos CSV na pasta '{directory_path}'...")

    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            board = load_and_validate_board(file_path)
            if board is not None:
                # Set global BOARD_SIZE and BLOCK_SIZE after successful load and validation
                set_board_size(board)
                analyze_sudoku(board, filename)
