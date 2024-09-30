import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
import random
import logic
import constants as c
import AI_heuristics as AI
from tkinter import Frame

class GameGrid(Frame):
    def __init__(self):
        super().__init__()
        self.grid()
        self.master.title('2048')
        self.done = False

        # Only use the primary movement keys (remove references to alternative keys)
        self.commands = {
            c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right
        }

        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.run_simulation()

    def run_simulation(self):
        # List of strategies available from AI_heuristics.py
        strategies = ["empty_tile", "monotonicity", "smoothness",
                       "merge_opportunities", "max_score", 
                      "max_free_lines", 
                       "same_row_col", "tile_grouping",
                       "adjacent_same_tiles", "balance_spread"]

        # This will store aggregated results for each strategy
        aggregated_results = {
            'Strategy': [],
            'Max Tile': [],
            'Avg Score': []
        }

        for strategy in strategies:
            max_tiles = []  # Store max tile for each run
            scores = []  # Store scores for each run

            # Running 100 simulations for each strategy
            for i in range(1000):  # Loop over 100 runs per strategy
                self.matrix = logic.new_game(c.GRID_LEN)
                self.done = False
                self.points = 0

                while not self.done:
                    # AI_play returns the best move based on the strategy
                    key = AI.AI_play(self.matrix, strategy)

                    if key is None:
                        key = random.choice([c.KEY_UP, c.KEY_DOWN, c.KEY_LEFT, c.KEY_RIGHT])

                    # Perform the move using the logic commands (up, down, left, right)
                    self.matrix, done, points = self.commands[key](self.matrix)
                    self.points += points
                    if done:
                        self.matrix = logic.add_two(self.matrix)

                    # Check game state
                    if logic.game_state(self.matrix) == 'win' or logic.game_state(self.matrix) == 'lose':
                        self.done = True

                # Get the maximum tile achieved during the game
                max_tile = max(max(row) for row in self.matrix)

                # Ensure the max_tile is a power of 2
                if max_tile > 0:
                    max_tile = 2 ** round(np.log2(max_tile))  # Ensure it's a power of 2

                # Append the max tile and score for this run
                max_tiles.append(max_tile)
                scores.append(self.points)

            # Append the aggregated results (max of max_tiles and average score)
            aggregated_results['Strategy'].append(strategy)
            aggregated_results['Max Tile'].append(max(max_tiles))  # Max of max tiles
            aggregated_results['Avg Score'].append(np.mean(scores))  # Average score over 100 runs

        # Save aggregated results of all strategies to an Excel file
        df = pd.DataFrame(aggregated_results)
        df.to_excel("aggregated_simulation_results.xlsx", index=False)
        print("Aggregated simulation results saved to 'aggregated_simulation_results.xlsx'")

    def find_top_strategies(self, n=5):
        # Read the Excel file with aggregated results
        df = pd.read_excel("aggregated_simulation_results.xlsx")

        # Sort first by 'Max Tile' (descending), and in case of ties, by 'Avg Score' (descending)
        df_sorted = df.sort_values(by=['Max Tile', 'Avg Score'], ascending=[False, False])

        # Select the top 'n' strategies
        top_strategies = df_sorted.head(n)

        # Save top strategies to a new Excel file
        top_strategies.to_excel("top_strategies.xlsx", index=False)

        print(f"Top {n} Strategies based on Max Tile and Avg Score saved to 'top_strategies.xlsx'")
        print(top_strategies[['Strategy', 'Max Tile', 'Avg Score']])
        return top_strategies


if __name__ == "__main__":
    gamegrid = GameGrid()

    top_strategies = gamegrid.find_top_strategies(5)
