
import constants as c
import logic
import random
import pandas as pd

# Load strategies and weights from Excel
def load_best_strategies_and_weights():
    """Loads the top strategies and weights from the Excel file."""
    df = pd.read_excel("best_weights.xlsx")
    strategies = df['strategy'].values
    weights = df['weights'].values
    return strategies, weights

commands = {c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right}

class AI_Heuristics:
    def __init__(self):
        # Load strategies and weights from Excel
        self.strategies, self.heuristic_weights = load_best_strategies_and_weights()

        # Dictionary mapping strategy names to heuristic functions
        self.strategy_functions = {
            'empty_tile': self.heuristic_empty_tile_score,
            'smoothness': self.calculate_smoothness,
            'monotonicity': self.heuristic_monotonicity,
            'merge_opportunities': self.heuristic_merge_opportunities,
            'max_score': self.heuristic_max_score,
            'max_free_lines': self.heuristic_max_free_lines,
            'same_row_col': self.heuristic_same_row_col,
            'tile_grouping': self.heuristic_tile_grouping,
            'adjacent_same_tiles': self.heuristic_adjacent_same_tiles,
            'balance_spread': self.heuristic_balance_spread
        }

    def heuristic_evaluation(self, matrix):
        total_score = 0
        for i, strategy in enumerate(self.strategies):
            heuristic_function = self.strategy_functions.get(strategy, None)
            if heuristic_function:
                heuristic_score = heuristic_function(matrix)
                total_score += self.heuristic_weights[i] * heuristic_score
        return total_score


    def get_move(self, matrix):
        best_move = None
        best_score = -float('inf')
        heuristic_scores = {}

        for key in commands:
            game, done, points = commands[key](matrix)
            if not done:
                continue

            score = 0
            # Loop through strategies and apply corresponding heuristic function
            for i, strategy in enumerate(self.strategies):
                heuristic_function = self.strategy_functions.get(strategy, None)
                if heuristic_function:
                    heuristic_score = heuristic_function(game)
                    score += self.heuristic_weights[i] * heuristic_score

            heuristic_scores[key] = score

            if score > best_score:
                best_score = score
                best_move = key

        # Print heuristic scores for each move
        print(f"Move {best_move}: Heuristic Scores: {heuristic_scores[best_move]}")
        return best_move

    # Heuristic functions for each strategy

    def heuristic_empty_tile_score(self, matrix):
        """Returns the number of empty tiles."""
        empty_tiles = sum(row.count(0) for row in matrix)
        return empty_tiles


    def calculate_smoothness(self, matrix):
        """Calculates smoothness by evaluating the difference between neighboring tiles."""
        smoothness = 0
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN - 1):
                smoothness += abs(matrix[i][j] - matrix[i][j + 1])
        for i in range(c.GRID_LEN - 1):
            for j in range(c.GRID_LEN):
                smoothness += abs(matrix[i][j] - matrix[i + 1][j])
        return -smoothness  # Smoothness is better with smaller values, so return negative.

    def heuristic_monotonicity(self, matrix):
        """Evaluates the monotonicity of rows and columns."""
        score = 0
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN - 1):
                if matrix[i][j] <= matrix[i][j + 1]:
                    score += 1
        return score


    def heuristic_merge_opportunities(self, matrix):
        """Counts the number of merge opportunities."""
        score = sum(matrix[i][j] == matrix[i][j + 1] for i in range(c.GRID_LEN) for j in range(c.GRID_LEN - 1))
        return score

    def heuristic_max_score(self, matrix):
        """Calculates the total score of the board."""
        return sum(sum(row) for row in matrix)

    def heuristic_max_free_lines(self, matrix):
        """Counts the number of rows or columns that are completely empty."""
        return sum([1 for row in matrix if all(tile == 0 for tile in row)])


    def heuristic_same_row_col(self, matrix):
        """Prefers moves that keep the same tiles in rows or columns for future merges."""
        score = sum(matrix[i][j] == matrix[i][j + 1] for i in range(c.GRID_LEN) for j in range(c.GRID_LEN - 1))
        return score

    def heuristic_tile_grouping(self, matrix):
        """Selects moves that group similar tiles together."""
        score = sum(matrix[i][j] == matrix[i][j + 1] for i in range(c.GRID_LEN) for j in range(c.GRID_LEN - 1))
        return score


    def heuristic_adjacent_same_tiles(self, matrix):
        """Selects moves that keep adjacent tiles of the same value together."""
        score = sum(matrix[i][j] == matrix[i][j + 1] for i in range(c.GRID_LEN) for j in range(c.GRID_LEN - 1))
        return score

    def heuristic_balance_spread(self, matrix):
        """Selects moves that balance the spread of tiles across the board."""
        spread = 0
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN - 1):
                spread += abs(matrix[i][j] - matrix[i][j + 1])
        return -spread  # Less spread is better, so return the negative value.
