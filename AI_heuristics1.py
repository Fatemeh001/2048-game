import constants as c
import numpy as np
import logic
import pandas as pd

# تابعی برای خواندن استراتژی‌های برتر از فایل اکسل
def get_top_strategies(n=5):
    """Reads the simulation results and selects the top N strategies."""
    df = pd.read_excel("top_strategies.xlsx")
    df_grouped = df.groupby('Strategy').agg({'Max Tile': 'max', 'Avg Score': 'mean'}).reset_index()
    df_sorted = df_grouped.sort_values(by=['Max Tile', 'Avg Score'], ascending=[False, False])
    top_strategies = df_sorted.head(n)
    return top_strategies['Strategy'].values

# تعریف دستورات برای حرکت‌ها
commands = {
    c.KEY_UP: logic.up,
    c.KEY_DOWN: logic.down,
    c.KEY_LEFT: logic.left,
    c.KEY_RIGHT: logic.right
}

# کلاس AI_Heuristics برای اجرای هیورستیک‌ها و وزن‌دهی به آنها
class AI_Heuristics:
    def __init__(self):
        # دریافت استراتژی‌های برتر هنگام مقداردهی اولیه کلاس
        self.strategies = get_top_strategies()

    def set_weights(self, weights, strategies):
        if len(weights) != len(strategies):
            raise ValueError("تعداد وزن‌ها و استراتژی‌ها باید برابر باشد.")
        
        # تنظیم وزن‌ها برای استراتژی‌های انتخاب شده
        self.heuristic_weights = {}
        for i, strategy in enumerate(strategies):
            self.heuristic_weights[strategy] = weights[i]

    def get_move(self, matrix):
        best_move = None
        best_score = -float('inf')

        # استفاده از استراتژی‌های برتر ذخیره‌شده در کلاس
        for key in commands:
            game, done, points = commands[key](matrix)
            if not done:
                continue

            # محاسبه امتیاز وزنی با استفاده از وزن‌ها و تمام هیورستیک‌های انتخاب شده
            score = 0
            for strategy, weight in self.heuristic_weights.items():
                if strategy == "empty_tile":
                    score += weight * self.heuristic_empty_tile(game)
                elif strategy == "monotonicity":
                    score += weight * self.heuristic_monotonicity(game)
                elif strategy == "smoothness":
                    score += weight * self.calculate_smoothness(game)
                elif strategy == "merge_opportunities":
                    score += weight * self.heuristic_merge_opportunities(game)
                elif strategy == "max_score":
                    score += weight * self.heuristic_max_score(game)
                elif strategy == "max_free_lines":
                    score += weight * self.heuristic_max_free_lines(game)
                elif strategy == "same_row_col":
                    score += weight * self.heuristic_same_row_col(game)
                elif strategy == "tile_grouping":
                    score += weight * self.heuristic_tile_grouping(game)
                elif strategy == "adjacent_same_tiles":
                    score += weight * self.heuristic_adjacent_same_tiles(game)
                elif strategy == "balance_spread":
                    score += weight * self.heuristic_balance_spread(game)
                else:
                    score += weight * self.heuristic_random()

            if score > best_score:
                best_score = score
                best_move = key

        return best_move

    # توابع هیورستیک برای محاسبه امتیاز هر استراتژی
    def heuristic_empty_tile(self, matrix):
        """Returns the number of empty tiles (score) instead of move."""
        n_empty = sum(row.count(0) for row in matrix)
        return n_empty

    def heuristic_monotonicity(self, matrix):
        """Measures the monotonicity of the grid."""
        total = 0
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN - 1):
                total += abs(matrix[i][j] - matrix[i][j + 1])
        for i in range(c.GRID_LEN - 1):
            for j in range(c.GRID_LEN):
                total += abs(matrix[i][j] - matrix[i + 1][j])
        return -total

    def calculate_smoothness(self, matrix):
        """Returns a score that reflects how smooth the board is."""
        smoothness = 0
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN - 1):
                smoothness += abs(matrix[i][j] - matrix[i][j + 1])
        for i in range(c.GRID_LEN - 1):
            for j in range(c.GRID_LEN):
                smoothness += abs(matrix[i][j] - matrix[i + 1][j])
        return -smoothness

    def heuristic_merge_opportunities(self, matrix):
        """Counts the number of possible merges."""
        merges = 0
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN - 1):
                if matrix[i][j] == matrix[i][j + 1]:
                    merges += 1
        return merges

    def heuristic_max_score(self, matrix):
        """Returns the score based on the maximum tile."""
        return max(max(row) for row in matrix)

    def heuristic_max_free_lines(self, matrix):
        """Counts the number of free lines (rows/columns with zeroes)."""
        return sum(1 for row in matrix if row.count(0) == c.GRID_LEN)

    def heuristic_same_row_col(self, matrix):
        """Counts the number of same tiles in the same row or column."""
        same_tiles = 0
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN - 1):
                if matrix[i][j] == matrix[i][j + 1]:
                    same_tiles += 1
        return same_tiles

    def heuristic_tile_grouping(self, matrix):
        """Counts how many tiles are grouped together."""
        groups = 0
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN - 1):
                if matrix[i][j] == matrix[i][j + 1]:
                    groups += 1
        return groups

    def heuristic_adjacent_same_tiles(self, matrix):
        """Counts the number of adjacent same tiles."""
        adjacent_tiles = 0
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN - 1):
                if matrix[i][j] == matrix[i][j + 1]:
                    adjacent_tiles += 1
        return adjacent_tiles

    def heuristic_balance_spread(self, matrix):
        """Measures how balanced the tiles are spread across the board."""
        total_spread = 0
        for i in range(c.GRID_LEN):
            total_spread += sum(matrix[i])
        return total_spread

