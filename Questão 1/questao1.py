import os
import pandas as pd
import numpy as np
import torch
import ltn
import sys

# Modelo dummy necessário para os predicados
class DummyModel(torch.nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, *inputs):
        return None

# Predicado HasNumber
class HasNumber(ltn.Predicate):
    def __init__(self, model, board_tensor):
        super().__init__(model)
        self.board_tensor = board_tensor
        self.board_size = board_tensor.shape[0]

    def forward(self, row, col, number):
        row_idx = torch.round(row).long()
        col_idx = torch.round(col).long()
        num_idx = torch.round(number).long()

        if not (torch.all(row_idx >= 0) and torch.all(row_idx < self.board_size) and
                torch.all(col_idx >= 0) and torch.all(col_idx < self.board_size) and
                torch.all(num_idx >= 1) and torch.all(num_idx <= self.board_size)):
            return torch.tensor(0.0, device=row.device).expand(row_idx.shape)

        try:
            return self.board_tensor[row_idx, col_idx, num_idx]
        except IndexError:
            return torch.tensor(0.0, device=row.device).expand(row_idx.shape)

# Predicado IsFilled
class IsFilled(ltn.Predicate):
    def __init__(self, model, board_tensor):
        super().__init__(model)
        self.board_tensor = board_tensor
        self.board_size = board_tensor.shape[0]

    def forward(self, row, col):
        row_idx = torch.round(row).long()
        col_idx = torch.round(col).long()

        if not (torch.all(row_idx >= 0) and torch.all(row_idx < self.board_size) and
                torch.all(col_idx >= 0) and torch.all(col_idx < self.board_size)):
            return torch.tensor(0.0, device=row.device).expand(row_idx.shape)

        selected_slices = self.board_tensor[row_idx, col_idx, 1:]
        truth_values = torch.sum(selected_slices, dim=-1)
        return (truth_values == 1).float()

# Funções para verificação de restrições
def compute_row_constraint_satisfaction(has_number_pred, rows, cols, numbers):
    satisfactions = []
    for r in rows:
        for n in numbers:
            sum_c_truth_values = [has_number_pred(r.unsqueeze(0), c.unsqueeze(0), n.unsqueeze(0)).squeeze(0) for c in cols]
            total_sum = torch.sum(torch.stack(sum_c_truth_values))
            satisfactions.append((total_sum == 1.0).float())
    return torch.mean(torch.stack(satisfactions)) if satisfactions else torch.tensor(0.0)

def compute_col_constraint_satisfaction(has_number_pred, rows, cols, numbers):
    satisfactions = []
    for c in cols:
        for n in numbers:
            sum_r_truth_values = [has_number_pred(r.unsqueeze(0), c.unsqueeze(0), n.unsqueeze(0)).squeeze(0) for r in rows]
            total_sum = torch.sum(torch.stack(sum_r_truth_values))
            satisfactions.append((total_sum == 1.0).float())
    return torch.mean(torch.stack(satisfactions)) if satisfactions else torch.tensor(0.0)

def compute_square_constraint_satisfaction(has_number_pred, rows, cols, numbers, sqrt_board_size):
    satisfactions = []
    board_size = int(rows[-1].item()) + 1
    if sqrt_board_size * sqrt_board_size != board_size:
        print(f"Warning: Board size {board_size} is not a perfect square.")
        return torch.tensor(0.0)

    for sr in range(sqrt_board_size):
        for sc in range(sqrt_board_size):
            for n in numbers:
                sum_rc_truth_values = []
                for r_offset in range(sqrt_board_size):
                    for c_offset in range(sqrt_board_size):
                        r = torch.tensor(sr * sqrt_board_size + r_offset, dtype=torch.float32)
                        c = torch.tensor(sc * sqrt_board_size + c_offset, dtype=torch.float32)
                        sum_rc_truth_values.append(has_number_pred(r.unsqueeze(0), c.unsqueeze(0), n.unsqueeze(0)).squeeze(0))
                if sum_rc_truth_values:
                    total_sum = torch.sum(torch.stack(sum_rc_truth_values))
                    satisfactions.append((total_sum == 1.0).float())
    return torch.mean(torch.stack(satisfactions)) if satisfactions else torch.tensor(0.0)

def compute_heuristic_satisfaction(is_filled_pred, rows, cols):
    satisfactions = [is_filled_pred(r.unsqueeze(0), c.unsqueeze(0)).squeeze(0) for r in rows for c in cols]
    return torch.mean(torch.stack(satisfactions)) if satisfactions else torch.tensor(0.0)

# Classificação do tabuleiro
def classify_sudoku(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path, header=None)
        sudoku_board_np = df.apply(pd.to_numeric, errors='coerce').to_numpy()
    except FileNotFoundError:
        print(f"Error: File not found: {csv_file_path}")
        return 0
    except Exception as e:
        print(f"Error processing CSV: {e}")
        return 0

    board_size = sudoku_board_np.shape[0]
    if sudoku_board_np.shape[1] != board_size:
        print("Error: Board must be square.")
        return 0
    if board_size not in [4, 9]:
        print("Error: Board size not supported.")
        return 0

    sqrt_board_size = int(np.sqrt(board_size))
    if sqrt_board_size * sqrt_board_size != board_size:
        print("Error: Board size is not a perfect square.")
        return 0

    if np.isnan(sudoku_board_np).any():
        print("Error: Board contains invalid values.")
        return 0

    sudoku_tensor = torch.zeros(board_size, board_size, board_size + 1)
    for r in range(board_size):
        for c in range(board_size):
            value = int(sudoku_board_np[r, c])
            if 1 <= value <= board_size:
                sudoku_tensor[r, c, value] = 1

    dummy_model = DummyModel()
    has_number_pred = HasNumber(dummy_model, sudoku_tensor)
    is_filled_pred = IsFilled(dummy_model, sudoku_tensor)

    rows = torch.arange(0, board_size, dtype=torch.float32)
    cols = torch.arange(0, board_size, dtype=torch.float32)
    numbers = torch.arange(1, board_size + 1, dtype=torch.float32)

    try:
        row_sat = compute_row_constraint_satisfaction(has_number_pred, rows, cols, numbers)
        col_sat = compute_col_constraint_satisfaction(has_number_pred, rows, cols, numbers)
        square_sat = compute_square_constraint_satisfaction(has_number_pred, rows, cols, numbers, sqrt_board_size)
        heuristic_sat = compute_heuristic_satisfaction(is_filled_pred, rows, cols)

        overall_satisfaction = torch.mean(torch.stack([row_sat, col_sat, square_sat, heuristic_sat]))
    except Exception as e:
        print(f"Error computing satisfaction: {e}")
        return 0

    print(f"Computed Overall Satisfaction: {overall_satisfaction.item():.4f}")

    satisfaction_threshold = 0.99
    return int(overall_satisfaction >= satisfaction_threshold)

# Execução principal
if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_directory_path = sys.argv[1]
        for filename in os.listdir(test_directory_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(test_directory_path, filename)
                print(f"\n--- Testing {filename} ---")
                classification_result = classify_sudoku(file_path)
                print(f"Classification Result for {filename}: {classification_result}")
    else:
        print("Usage: python questao1.py <directory_path>")
