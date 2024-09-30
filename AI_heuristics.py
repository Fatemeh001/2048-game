import constants as c
import random
import numpy as np
import logic  # Keeping import of logic for actual move commands

# Defining commands dictionary locally to avoid circular import issues
commands = {
    c.KEY_UP: logic.up,
    c.KEY_DOWN: logic.down,
    c.KEY_LEFT: logic.left,
    c.KEY_RIGHT: logic.right
}

def AI_play(matrix, strategy="empty_tile"):
    """Select the heuristic strategy to use."""
    if strategy == "empty_tile":
        return heuristic_empty_tile(matrix)
    elif strategy == "monotonicity":
        return heuristic_monotonicity(matrix)
    elif strategy == "smoothness":
        return heuristic_smoothness(matrix)
    elif strategy == "merge_opportunities":
        return heuristic_merge_opportunities(matrix)
    elif strategy == "max_score":
        return heuristic_max_score(matrix)
    elif strategy == "max_free_lines":
        return heuristic_max_free_lines(matrix)
    elif strategy == "same_row_col":
        return heuristic_same_row_col(matrix)
    elif strategy == "tile_grouping":
        return heuristic_tile_grouping(matrix)
    elif strategy == "adjacent_same_tiles":
        return heuristic_adjacent_same_tiles(matrix)
    elif strategy == "balance_spread":
        return heuristic_balance_spread(matrix)
    else:
        return heuristic_random()

def heuristic_random():
    """Randomly selects one of the four possible directions."""
    tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_LEFT, c.KEY_RIGHT]
    key = tmp[random.randint(0, 3)]
    return key

def heuristic_empty_tile(matrix):
    """Selects the move that maximizes the number of empty tiles."""
    best_score = -1
    return_key = None
    for key in commands.keys():
        game, done, _ = commands[key](matrix)
        if not done:
            continue
        n_empty = sum(row.count(0) for row in game)
        if n_empty > best_score:
            best_score = n_empty
            return_key = key
    return return_key



def heuristic_monotonicity(matrix):
    """Selects the move that maximizes the monotonicity of rows or columns."""
    best_score = -1
    return_key = None
    for key in commands.keys():
        game, done, _ = commands[key](matrix)
        if not done:
            continue
        score = sum(game[i][j] <= game[i + 1][j] for i in range(c.GRID_LEN - 1) for j in range(c.GRID_LEN))
        if score > best_score:
            best_score = score
            return_key = key
    return return_key

def heuristic_smoothness(matrix):
    """Selects the move that minimizes the difference between neighboring tiles."""
    best_score = -1
    return_key = None
    for key in commands.keys():
        game, done, _ = commands[key](matrix)
        if not done:
            continue
        score = sum(abs(game[i][j] - game[i][j + 1]) for i in range(c.GRID_LEN) for j in range(c.GRID_LEN - 1))
        if score < best_score or best_score == -1:
            best_score = score
            return_key = key
    return return_key


def heuristic_merge_opportunities(matrix):
    """Selects moves that maximize merge opportunities."""
    best_score = -1
    return_key = None
    for key in commands.keys():
        game, done, _ = commands[key](matrix)
        if not done:
            continue
        score = sum(game[i][j] == game[i][j + 1] for i in range(c.GRID_LEN) for j in range(c.GRID_LEN - 1))
        if score > best_score:
            best_score = score
            return_key = key
    return return_key

def heuristic_max_score(matrix):
    """Selects moves that maximize the score."""
    best_score = -1
    return_key = None
    for key in commands.keys():
        game, done, points = commands[key](matrix)
        if not done:
            continue
        if points > best_score:
            best_score = points
            return_key = key
    return return_key

def heuristic_max_free_lines(matrix):
    """Selects moves that maximize the number of free lines (rows/columns with zeroes)."""
    best_score = -1
    return_key = None
    for key in commands.keys():
        game, done, _ = commands[key](matrix)
        if not done:
            continue
        score = sum(game[i].count(0) for i in range(c.GRID_LEN))
        if score > best_score:
            best_score = score
            return_key = key
    return return_key



def heuristic_same_row_col(matrix):
    """Prefers moves that keep same tiles in rows or columns for future merges."""
    best_score = -1
    return_key = None
    for key in commands.keys():
        game, done, _ = commands[key](matrix)
        if not done:
            continue
        score = sum(game[i][j] == game[i][j + 1] for i in range(c.GRID_LEN) for j in range(c.GRID_LEN - 1))
        if score > best_score:
            best_score = score
            return_key = key
    return return_key

def heuristic_tile_grouping(matrix):
    """Selects moves that group similar tiles together."""
    best_score = -1
    return_key = None
    for key in commands.keys():
        game, done, _ = commands[key](matrix)
        if not done:
            continue
        score = sum(game[i][j] == game[i][j + 1] for i in range(c.GRID_LEN) for j in range(c.GRID_LEN - 1))
        if score > best_score:
            best_score = score
            return_key = key
    return return_key

def heuristic_avoid_blocking_large_tiles(matrix):
    """Prefers moves that avoid blocking large tiles with small ones."""
    best_score = -1
    return_key = None
    for key in commands.keys():
        game, done, _ = commands[key](matrix)
        if not done:
            continue
        max_tile = max(max(row) for row in game)
        if max_tile > best_score:
            best_score = max_tile
            return_key = key
    return return_key

def heuristic_adjacent_same_tiles(matrix):
    """Selects moves that keep adjacent tiles of the same value together."""
    best_score = -1
    return_key = None
    for key in commands.keys():
        game, done, _ = commands[key](matrix)
        if not done:
            continue
        score = sum(game[i][j] == game[i][j + 1] for i in range(c.GRID_LEN) for j in range(c.GRID_LEN - 1))
        if score > best_score:
            best_score = score
            return_key = key
    return return_key

def heuristic_balance_spread(matrix):
    """Selects moves that balance the spread of tiles across the board."""
    best_score = -1
    return_key = None
    for key in commands.keys():
        game, done, _ = commands[key](matrix)
        if not done:
            continue
        score = sum(abs(game[i][j] - game[i][j + 1]) for i in range(c.GRID_LEN) for j in range(c.GRID_LEN - 1))
        if score < best_score or best_score == -1:
            best_score = score
            return_key = key
    return return_key
