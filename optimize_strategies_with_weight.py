import tkinter as tk
from tkinter import Frame, Label, CENTER
import logic
import constants as c
import AI_heuristics1 as AI  # Import the AI with combined heuristics
import pandas as pd
import numpy as np
import time
import itertools

def get_top_strategies(n=5):

    df = pd.read_excel("top_strategies.xlsx")
    df_grouped = df.groupby('Strategy').agg({'Max Tile': 'max', 'Avg Score': 'mean'}).reset_index()
    df_sorted = df_grouped.sort_values(by=['Max Tile', 'Avg Score'], ascending=[False, False])
    top_strategies = df_sorted.head(n)
    strategy_names = top_strategies['Strategy'].values
    return strategy_names

class GameGrid(Frame):
    def __init__(self, ai, weights, strategies, run_count=2, delay=0.01, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title('2048')
        self.grid_cells = []
        self.ai = ai  # Pass the AI with combined heuristics
        self.weights = weights
        self.strategies = strategies
        self.run_count = run_count
        self.delay = delay
        self.all_results = []
        self.init_grid()
        self.run_multiple_games()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME, width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY, width=c.SIZE / c.GRID_LEN, height=c.SIZE / c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING, pady=c.GRID_PADDING)
                t = Label(master=cell, text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=c.FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def init_matrix(self):
        self.matrix = logic.new_game(c.GRID_LEN)
        self.add_random_tile()
        self.add_random_tile()

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=c.BACKGROUND_COLOR_DICT.get(new_number, "#3c3a32"),
                                                    fg=c.CELL_COLOR_DICT.get(new_number, "#f9f6f2"))
        self.update_idletasks()

    def add_random_tile(self):
        self.matrix = logic.add_two(self.matrix)

    def run_game(self):
        max_tile = 0
        total_score = 0
        moves = 0

        self.init_matrix()

        while logic.game_state(self.matrix) == 'not over':
            move = self.ai.get_move(self.matrix)
            self.matrix, done, points = logic.commands[move](self.matrix)
            total_score += points
            moves += 1
            if done:
                self.add_random_tile()

            self.update_grid_cells()
            self.update()  # Ensure the GUI updates
            time.sleep(self.delay)  # Optional delay for visualization

        max_tile = max([max(row) for row in self.matrix])
        return max_tile, total_score, moves

    def run_multiple_games(self):
        for i in range(self.run_count):
            max_tile, total_score, moves = self.run_game()
            print(f"Weights: {self.weights}, Strategies: {self.strategies} - Max Tile: {max_tile}, Total Score: {total_score}, Moves: {moves}")
            self.all_results.append({
                'Weights': self.weights,
                'Strategies': self.strategies,
                'Max Tile': max_tile,
                'Total Score': total_score,
                'Total Moves': moves
            })

    def get_average_performance(self):
        df = pd.DataFrame(self.all_results)
        max_max_tile = df['Max Tile'].max()  # Find the max tile achieved across all games
        avg_score = df['Total Score'].mean()  # Average score across games
        return max_max_tile, avg_score

# Function to evaluate different weight combinations
def evaluate_weights(weights, strategies, num_games=1):
    ai = AI.AI_Heuristics()  # Instantiate the AI class with combined heuristics
    ai.set_weights(weights, strategies) 

    all_results = []
    for _ in range(num_games):
        root = tk.Tk()  # Create a new window for each game
        gamegrid = GameGrid(ai, weights, strategies, run_count=1, master=root, delay=0)  # Set delay to 0 for fast execution
        max_tile, total_score, moves = gamegrid.run_game()
        all_results.append({
            'Max Tile': max_tile,
            'Total Score': total_score,
            'Total Moves': moves,
            'Weights': weights,
            'Strategies': strategies
        })
        root.destroy()  # Destroy the window after each game finishes

    # Calculate performance metrics
    df = pd.DataFrame(all_results)
    max_max_tile = df['Max Tile'].max()
    avg_score = df['Total Score'].mean()
    return max_max_tile, avg_score, df  # Return the DataFrame containing the results

# دریافت استراتژی‌های پویا
top_strategies = get_top_strategies(n=5)

# Define possible weight values
weights_range = np.arange(0.0, 1.1, 0.1)

# Generate all valid combinations of weights for the top strategies
combinations = itertools.product(weights_range, repeat=len(top_strategies)) 
valid_combinations = [combo for combo in combinations if np.isclose(sum(combo), 1.0)]

best_weights = None
best_performance = -float('inf')
best_avg_score = -float('inf')  # To track the best average score
results = []
all_results_df = pd.DataFrame()  # To store all results

for weights in valid_combinations:
    max_max_tile, avg_score, df = evaluate_weights(weights, top_strategies)
    
    # Use max_max_tile as the primary performance metric
    performance = max_max_tile

    print(f"Weights {weights} - Max Max Tile: {max_max_tile}, Avg Score: {avg_score}")
    
    results.append({
        'Weights': weights,
        'Max Max Tile': max_max_tile,
        'Avg Score': avg_score
    })

    # Append the results for this combination to the all_results_df DataFrame
    all_results_df = pd.concat([all_results_df, df])

    # First, select based on Max Max Tile, then based on Avg Score if Max Max Tile is the same
    if performance > best_performance or (performance == best_performance and avg_score > best_avg_score):
        best_performance = performance
        best_avg_score = avg_score
        best_weights = weights

print(f"\nBest Weights: {best_weights} with Max Max Tile: {best_performance} and Avg Score: {best_avg_score}")


best_results = pd.DataFrame({
    'strategy': top_strategies,
    'weights': best_weights,  # This will work if best_weights is the same length as top_strategies
    'performance': [best_performance] * len(top_strategies)  # Repeat the performance for each strategy
})

best_results.to_excel("best_weights.xlsx", index=False)  # Save the best strategies and weights
print("Best strategies and weights saved to 'best_weights.xlsx'")

# Save results to Excel
df_results = pd.DataFrame(results)
all_results_df.to_excel("detailed_game_results.xlsx", index=False)
print("Results saved to 'best_weights.xlsx' and 'detailed_game_results.xlsx'")
