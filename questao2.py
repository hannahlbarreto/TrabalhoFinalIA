import torch
import ltn
import numpy as np
import os
import sys
import glob
import copy

# --- Parte 0: Configuração do Dispositivo (GPU ou CPU) ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"INFO: Usando dispositivo: {device}\n")


# --- Parte 1: Definições da Rede Neural e do Predicado LTN ---

class SudokuNet(torch.nn.Module):
    """
    Rede Neural (o 'cérebro' do nosso predicado).
    Recebe um tabuleiro e retorna um único valor que representa a 'solvabilidade'.
    """
    def __init__(self, board_size):
        super(SudokuNet, self).__init__()
        self.board_size = board_size
        input_size = board_size * board_size
        self.fc1 = torch.nn.Linear(input_size, 64)
        self.fc2 = torch.nn.Linear(64, 64)
        self.fc3 = torch.nn.Linear(64, 1)

    def forward(self, x):
        x = x.reshape(-1, self.board_size * self.board_size)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return torch.sigmoid(self.fc3(x))

# --- Parte 2: Funções Auxiliares e Determinísticas ---

def violates_constraint(board, move, board_size, block_size):
    """Verifica se uma jogada viola uma regra básica do Sudoku."""
    row, col, digit = move
    if digit in board[row, :]: return True
    if digit in board[:, col]: return True
    start_row, start_col = row - row % block_size, col - col % block_size
    if digit in board[start_row:start_row + block_size, start_col:start_col + block_size]: return True
    return False

def get_empty_cells(board, board_size):
    """Retorna uma lista de tuplas (linha, coluna) para células vazias."""
    cells = []
    for r in range(board_size):
        for c in range(board_size):
            if board[r, c] == 0:
                cells.append((r, c))
    return cells

def check_sem_solucao_deterministico(board, board_size, block_size):
    """Verifica a regra específica da Questão 2, Parte 1."""
    empty_cells = get_empty_cells(board, board_size)
    if not empty_cells: return False, None
    for digit_to_check in range(1, board_size + 1):
        can_place_digit = False
        for cell in empty_cells:
            if not violates_constraint(board, (cell[0], cell[1], digit_to_check), board_size, block_size):
                can_place_digit = True
                break
        if not can_place_digit:
            return True, digit_to_check
    return False, None

# --- Parte 3: Treinamento do Modelo LTN ---

def generate_training_data(num_samples, board_size):
    """Gera dados de treino: tabuleiros solucionáveis e sem solução."""
    solvable_boards = []
    unsolvable_boards = []
    
    if board_size == 9:
        base_solved = np.array([
            [5,3,4,6,7,8,9,1,2],[6,7,2,1,9,5,3,4,8],[1,9,8,3,4,2,5,6,7],
            [8,5,9,7,6,1,4,2,3],[4,2,6,8,5,3,7,9,1],[7,1,3,9,2,4,8,5,6],
            [9,6,1,5,3,7,2,8,4],[2,8,7,4,1,9,6,3,5],[3,4,5,2,8,6,1,7,9]
        ])
    else: # Exemplo 4x4
        base_solved = np.array([
            [1,2,3,4],[3,4,1,2],[2,1,4,3],[4,3,2,1]
        ])

    for _ in range(num_samples):
        board = base_solved.copy()
        for _ in range(board_size * board_size // 2):
            r, c = np.random.randint(0, board_size, 2)
            board[r,c] = 0
        solvable_boards.append(board)

        board = base_solved.copy()
        r, c = np.random.randint(0, board_size, 2)
        board[r, c] = board[r, (c + 1) % board_size]
        unsolvable_boards.append(board)
        
    return torch.tensor(np.array(solvable_boards), dtype=torch.float32), \
        torch.tensor(np.array(unsolvable_boards), dtype=torch.float32)


def train_model(is_solvable_predicate, board_size):
    """Treina o predicado LTN usando axiomas de supervisão."""
    print(f"Iniciando treinamento do modelo LTN para {board_size}x{board_size}...")
    
    # Usaremos apenas o quantificador ForAll, que está funcionando
    ForAll = ltn.Quantifier(ltn.fuzzy_ops.AggregPMeanError(p=2), quantifier="f")
    
    solvable_data, unsolvable_data = generate_training_data(128, board_size)
    solvable_data = solvable_data.to(device)
    unsolvable_data = unsolvable_data.to(device)
    
    s_solvable = ltn.Variable("s_solvable", solvable_data)
    s_unsolvable = ltn.Variable("s_unsolvable", unsolvable_data)
    optimizer = torch.optim.Adam(is_solvable_predicate.model.parameters(), lr=0.001)

    for epoch in range(1000):
        optimizer.zero_grad()
        
        # Axioma 1: Para todos os tabuleiros solucionáveis, o predicado é verdadeiro.
        sat_ax1 = ForAll(s_solvable, is_solvable_predicate(s_solvable))
        
        # Axioma 2: Para todos os tabuleiros sem solução, o predicado é verdadeiro.
        # (Lemos o resultado e o tratamos como uma perda na próxima etapa)
        sat_ax2 = ForAll(s_unsolvable, is_solvable_predicate(s_unsolvable))
        
        # Calculamos a perda de cada axioma separadamente
        # e as somamos, evitando os operadores lógicos problemáticos.
        loss1 = 1. - sat_ax1.value # Queremos que sat_ax1 seja 1.0
        loss2 = sat_ax2.value     # Queremos que sat_ax2 seja 0.0
        loss = loss1 + loss2
        
        loss.backward()
        optimizer.step()
        if epoch % 200 == 0:
            print(f"  Epoch {epoch}, Loss Total: {loss.item():.4f} (bons_boards_sat: {sat_ax1.value.item():.2f}, maus_boards_sat: {sat_ax2.value.item():.2f})")
    print("Treinamento concluído.\n")

# --- Parte 4: Análise e Relatório ---

def analyze_sudoku_with_ltn(board, file_name, board_size, block_size, is_solvable_predicate):
    """Realiza a análise completa, usando o modelo LTN treinado."""
    print(f"--- Processando arquivo: {file_name} ---")
    print("Tabuleiro Lido:\n", board)

    is_unsolvable, problematic_digit = check_sem_solucao_deterministico(board, board_size, block_size)

    print("\n--- RELATÓRIO DE ANÁLISE ---")
    if is_unsolvable:
        print(f"Classificação: Sem Solução")
        print(f"Motivo: O dígito '{problematic_digit}' não pode ser colocado em nenhuma célula vazia.")
        return

    print("Classificação: Solução Possível")
    print("\n[ Análise de Movimentos com LTN (1 passo) ]")
    
    possible_moves_with_scores = []
    empty_cells = get_empty_cells(board, board_size)
    
    for cell in empty_cells:
        for digit in range(1, board_size + 1):
            if not violates_constraint(board, (cell[0], cell[1], digit), board_size, block_size):
                temp_board = torch.tensor(board.copy(), dtype=torch.float32).to(device)
                temp_board[cell[0], cell[1]] = digit
                score = is_solvable_predicate(ltn.Constant(temp_board)).value.item()
                possible_moves_with_scores.append(((cell[0], cell[1], digit), score))

    if not possible_moves_with_scores:
        print("  - Nenhuma jogada válida encontrada.")
        return

    possible_moves_with_scores.sort(key=lambda x: x[1], reverse=True)

    print("  - Jogadas com maior probabilidade de manter a solução (melhores scores):")
    for move, score in possible_moves_with_scores[:5]:
        print(f"    - Jogar {move[2]} em ({move[0]},{move[1]}) -> Score de Solvabilidade: {score:.4f}")

    print("\n  - Jogadas com menor probabilidade de manter a solução (piores scores):")
    for move, score in possible_moves_with_scores[-5:]:
        print(f"    - Jogar {move[2]} em ({move[0]},{move[1]}) -> Score de Solvabilidade: {score:.4f}")


# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("ERRO: Formato de uso incorreto.")
        print("Uso: python questao2.py <caminho_para_pasta_de_testes>")
        exit()

    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print(f"ERRO: O diretório '{directory_path}' não é válido.")
        exit()

    csv_files = glob.glob(os.path.join(directory_path, '*.csv'))
    if not csv_files:
        print(f"Nenhum arquivo .csv encontrado no diretório '{directory_path}'.")
        exit()
        
    required_sizes = set()
    for file_path in csv_files:
        try:
            board_shape = np.loadtxt(file_path, delimiter=',', dtype=int).shape
            if board_shape[0] == board_shape[1] and int(np.sqrt(board_shape[0]))**2 == board_shape[0]:
                required_sizes.add(board_shape[0])
        except Exception:
            print(f"Aviso: Não foi possível ler as dimensões de {os.path.basename(file_path)}. O arquivo será ignorado.")
            continue
    
    trained_predicates = {}
    for size in sorted(list(required_sizes)):
        print(f"--- Preparando modelo para tabuleiros {size}x{size} ---")
        model = SudokuNet(board_size=size).to(device)
        predicate = ltn.Predicate(model=model)
        train_model(predicate, board_size=size)
        trained_predicates[size] = predicate

    print(f"--- INICIANDO ANÁLISE EM LOTE DE {len(csv_files)} ARQUIVOS ---\n")
    for file_path in csv_files:
        try:
            board = np.loadtxt(file_path, delimiter=',', dtype=int)
            board_size = board.shape[0]
            
            if board_size not in trained_predicates:
                continue

            block_size = int(np.sqrt(board_size))
            predicate = trained_predicates[board_size]
            
            analyze_sudoku_with_ltn(board, os.path.basename(file_path), board_size, block_size, predicate)
            print("-" * 50)
            
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo {os.path.basename(file_path)}: {e}\n")

    print("--- ANÁLISE EM LOTE CONCLUÍDA ---")
