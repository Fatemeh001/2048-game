import tkinter as tk
from tkinter import Frame
import logic
import constants as c
import AI_both as AI
import pandas as pd

class GameGrid(Frame):
    def __init__(self, ai, run_count=1 , delay=1, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title('2048')
        self.grid_cells = []
        self.ai = ai  # Expectimax AI or any other AI passed to the game
        self.run_count = run_count
        self.delay = delay  # delay in milliseconds, use with after()
        self.all_results = []
        self.current_game = 0
        self.init_grid()
        self.init_matrix()
        self.run_game_step()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME, width=c.SIZE, height=c.SIZE)
        background.grid()
        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY, width=c.SIZE / c.GRID_LEN, height=c.SIZE / c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING, pady=c.GRID_PADDING)
                t = tk.Label(master=cell, text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY, justify=tk.CENTER, font=c.FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def init_matrix(self):
        self.matrix = logic.new_game(c.GRID_LEN)
        self.add_random_tile()
        self.add_random_tile()
        self.update_grid_cells()

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

    def run_game_step(self):
        if logic.game_state(self.matrix) == 'not over':
            move = self.ai.get_move(self.matrix)
            self.matrix, done, points = logic.commands[move](self.matrix)
            if done:
                self.add_random_tile()

            self.update_grid_cells()
            self.after(self.delay, self.run_game_step)  # Schedule the next step
        else:
            max_tile = max([max(row) for row in self.matrix])
            total_score = sum(sum(row) for row in self.matrix)
            self.all_results.append({'Game': self.current_game + 1, 'Max Tile': max_tile, 'Total Score': total_score})
            print(f"Game {self.current_game + 1}: Max Tile: {max_tile}, Total Score: {total_score}")

            self.current_game += 1
            if self.current_game < self.run_count:
                self.init_matrix()  # Start a new game
                self.run_game_step()  # Continue to next game
            else:
                self.save_results()  # Save the results after all games are done

    def save_results(self):
        df = pd.DataFrame(self.all_results)
        df.to_excel("multiple_game_results.xlsx", index=False)
        print(f"Results saved to 'multiple_game_results.xlsx'")

def start_game():
    root = tk.Tk()
    ai = AI.AI()  # Use the Expectimax AI or any other AI you want
    game_grid = GameGrid(ai, run_count=100, delay=5, master=root)  # Run 10 games with a delay of 200ms between steps
    root.mainloop()

if __name__ == "__main__":
    start_game()
