import os
import pandas as pd
import numpy as np
import torch
import ltn # Ensure ltn is imported for predicate definitions

# Redefine DummyModel and Predicates within the test scope for clarity and self-containment
class DummyModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        pass

    def forward(self, *inputs):
        return None

class HasNumber(ltn.Predicate):
    def __init__(self, model, board_tensor):
        super().__init__(model)
        self.board_tensor = board_tensor
        self.board_size = board_tensor.shape[0]

    def __call__(self, row, col, number):
        row_idx = torch.round(row).long()
        col_idx = torch.round(col).long()
        num_idx = torch.round(number).long()

        if not (torch.all(row_idx >= 0) and torch.all(row_idx < self.board_size) and
                torch.all(col_idx >= 0) and torch.all(col_idx < self.board_size) and
                torch.all(num_idx >= 1) and torch.all(num_idx <= self.board_size)):
             return torch.tensor(0.0, device=row.device).expand(row_idx.shape)

        try:
            truth_values = self.board_tensor[row_idx, col_idx, num_idx]
        except IndexError:
             return torch.tensor(0.0, device=row.device).expand(row_idx.shape)

        return truth_values

class IsFilled(ltn.Predicate):
    def __init__(self, model, board_tensor):
        super().__init__(model)
        self.board_tensor = board_tensor
        self.board_size = board_tensor.shape[0]

    def __call__(self, row, col):
        row_idx = torch.round(row).long()
        col_idx = torch.round(col).long()

        if not (torch.all(row_idx >= 0) and torch.all(row_idx < self.board_size) and
                torch.all(col_idx >= 0) and torch.all(col_idx < self.board_size)):
             return torch.tensor(0.0, device=row.device).expand(row_idx.shape)

        selected_slices = self.board_tensor[row_idx, col_idx, 1:]
        truth_values = torch.sum(selected_slices, dim=-1)
        truth_values_float = (truth_values == 1).float()

        return truth_values_float

# Redefine constraint satisfaction functions
def compute_row_constraint_satisfaction(has_number_pred, rows, cols, numbers):
    satisfactions = []
    for r in rows:
        for n in numbers:
            sum_c_truth_values = []
            for c in cols:
                 sum_c_truth_values.append(has_number_pred(r.unsqueeze(0), c.unsqueeze(0), n.unsqueeze(0)).squeeze(0))
            total_sum = torch.sum(torch.stack(sum_c_truth_values))
            row_n_satisfaction = (total_sum == 1.0).float()
            satisfactions.append(row_n_satisfaction)
    if not satisfactions: return torch.tensor(0.0) # Handle empty case
    return torch.mean(torch.stack(satisfactions))

def compute_col_constraint_satisfaction(has_number_pred, rows, cols, numbers):
    satisfactions = []
    for c in cols:
        for n in numbers:
            sum_r_truth_values = []
            for r in rows:
                 sum_r_truth_values.append(has_number_pred(r.unsqueeze(0), c.unsqueeze(0), n.unsqueeze(0)).squeeze(0))
            total_sum = torch.sum(torch.stack(sum_r_truth_values))
            col_n_satisfaction = (total_sum == 1.0).float()
            satisfactions.append(col_n_satisfaction)
    if not satisfactions: return torch.tensor(0.0)
    return torch.mean(torch.stack(satisfactions))

def compute_square_constraint_satisfaction(has_number_pred, rows, cols, numbers, sqrt_board_size):
    satisfactions = []
    # Ensure board_size is consistent with sqrt_board_size
    board_size = int(rows[-1].item()) + 1
    if sqrt_board_size * sqrt_board_size != board_size:
        print(f"Warning: Board size {board_size} is not a perfect square for square constraint check.")
        return torch.tensor(0.0) # Cannot compute square satisfaction if size is invalid

    for sr in range(sqrt_board_size):
        for sc in range(sqrt_board_size):
            for n in numbers:
                sum_rc_truth_values = []
                for r_offset in range(sqrt_board_size):
                    for c_offset in range(sqrt_board_size):
                        r = torch.tensor(sr * sqrt_board_size + r_offset, dtype=torch.float32)
                        c = torch.tensor(sc * sqrt_board_size + c_offset, dtype=torch.float32)
                        sum_rc_truth_values.append(has_number_pred(r.unsqueeze(0), c.unsqueeze(0), n.unsqueeze(0)).squeeze(0))
                if not sum_rc_truth_values: continue # Handle empty square case
                total_sum = torch.sum(torch.stack(sum_rc_truth_values))
                square_n_satisfaction = (total_sum == 1.0).float()
                satisfactions.append(square_n_satisfaction)
    if not satisfactions: return torch.tensor(0.0)
    return torch.mean(torch.stack(satisfactions))

def compute_heuristic_satisfaction(is_filled_pred, rows, cols):
    satisfactions = []
    for r in rows:
        for c in cols:
            satisfactions.append(is_filled_pred(r.unsqueeze(0), c.unsqueeze(0)).squeeze(0))
    if not satisfactions: return torch.tensor(0.0)
    return torch.mean(torch.stack(satisfactions))


# Define the classification function
def classify_sudoku(csv_file_path):
    """
    Classifies a completed Sudoku board from a CSV file as correctly filled (1) or not (0).

    Args:
        csv_file_path (str): The path to the CSV file containing the Sudoku board.

    Returns:
        int: 1 if the board is correctly filled, 0 otherwise.
    """
    try:
        df = pd.read_csv(csv_file_path, header=None)
        # Attempt to convert to numeric, coercing errors to NaN
        sudoku_board_np = df.apply(pd.to_numeric, errors='coerce').to_numpy()
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
        return 0
    except Exception as e:
        print(f"Error loading or processing CSV file: {e}")
        return 0

    board_size = sudoku_board_np.shape[0]
    if sudoku_board_np.shape[1] != board_size:
        print(f"Error: Board is not square. Shape: {sudoku_board_np.shape}")
        return 0
    if board_size not in [4, 9]:
         print(f"Error: Unsupported board size: {board_size}x{board_size}. Only 4x4 and 9x9 are supported.")
         return 0

    sqrt_board_size = int(np.sqrt(board_size))
    if sqrt_board_size * sqrt_board_size != board_size:
         print(f"Error: Board size {board_size} is not a perfect square (required for square constraints).")
         return 0

    # Check for NaN values (introduced by 'coerce' on non-numeric data)
    if np.isnan(sudoku_board_np).any():
        print(f"Error: Invalid (non-numeric) entries found in the board.")
        # Set overall satisfaction to 0 if invalid entries exist
        overall_satisfaction = torch.tensor(0.0)
    else:
        # Convert to the 3D PyTorch tensor representation
        sudoku_tensor = torch.zeros(board_size, board_size, board_size + 1)
        for r in range(board_size):
            for c in range(board_size):
                value = int(sudoku_board_np[r, c]) # Cast to int after checking for NaN
                # The predicates handle values outside [1, board_size] by returning 0 truth value.
                if value >= 1 and value <= board_size:
                     sudoku_tensor[r, c, value] = 1
                # Invalid values (<=0 or >board_size) will result in the slice being all zeros,
                # which the has_number predicate will correctly interpret as false,
                # and the is_filled predicate might interpret incorrectly if not all other numbers are 0.
                # The current predicates handle this implicitly. If value is out of bounds, num_idx will be.
                # Let's rely on the predicate's bounds checking.

        # Instantiate predicates with the board tensor
        dummy_model = DummyModel()
        has_number_pred = HasNumber(dummy_model, sudoku_tensor)
        is_filled_pred = IsFilled(dummy_model, sudoku_tensor)

        # Define grounding tensors
        rows = torch.arange(0, board_size, dtype=torch.float32)
        cols = torch.arange(0, board_size, dtype=torch.float32)
        numbers = torch.arange(1, board_size + 1, dtype=torch.float32)

        # Compute overall satisfaction level
        try:
            row_sat = compute_row_constraint_satisfaction(has_number_pred, rows, cols, numbers)
            col_sat = compute_col_constraint_satisfaction(has_number_pred, rows, cols, numbers)
            square_sat = compute_square_constraint_satisfaction(has_number_pred, rows, cols, numbers, sqrt_board_size)
            heuristic_sat = compute_heuristic_satisfaction(is_filled_pred, rows, cols)

            overall_satisfaction = torch.mean(torch.stack([row_sat, col_sat, square_sat, heuristic_sat]))
        except Exception as e:
            print(f"Error computing satisfaction: {e}")
            return 0

    print(f"Computed Overall Satisfaction: {overall_satisfaction.item()}")

    satisfaction_threshold = 0.99

    if overall_satisfaction >= satisfaction_threshold:
        return 1
    else:
        return 0

# --- Test Cases ---
# Iterate through files in the test directory and classify
print(f"Classifying all CSV files in '{test_dir}':")
for filename in os.listdir(test_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(test_dir, filename)
        classification_result = classify_sudoku(file_path)
        print(f"File: {filename}, Classification Result: {classification_result}")

