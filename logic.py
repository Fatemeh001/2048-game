# import random
# import constants as c

# def new_game(n):
#     matrix = [[0] * n for _ in range(n)]
#     matrix = add_two(matrix)
#     matrix = add_two(matrix)
#     return matrix

# def add_two(mat):
#     a, b = random.randint(0, len(mat)-1), random.randint(0, len(mat)-1)
#     while mat[a][b] != 0:
#         a, b = random.randint(0, len(mat)-1), random.randint(0, len(mat)-1)
#     mat[a][b] = 4 if random.randint(0, 9) == 9 else 2
#     return mat

# def game_state(mat):
#     for row in mat:
#         if 2048 in row:
#             return 'win'
#     for row in mat:
#         if 0 in row:
#             return 'not over'
#     for i in range(c.GRID_LEN):
#         for j in range(c.GRID_LEN - 1):
#             if mat[i][j] == mat[i][j + 1]:
#                 return 'not over'
#             if mat[j][i] == mat[j + 1][i]:
#                 return 'not over'
#     return 'lose'

# def reverse(mat):
#     return [row[::-1] for row in mat]

# def transpose(mat):
#     return [[mat[j][i] for j in range(c.GRID_LEN)] for i in range(c.GRID_LEN)]

# def cover_up(mat):
#     new = [[0] * c.GRID_LEN for _ in range(c.GRID_LEN)]
#     done = False
#     for i in range(c.GRID_LEN):
#         count = 0
#         for j in range(c.GRID_LEN):
#             if mat[i][j] != 0:
#                 new[i][count] = mat[i][j]
#                 if j != count:
#                     done = True
#                 count += 1
#     return new, done

# def merge(mat, done):
#     points = 0
#     for i in range(c.GRID_LEN):
#         for j in range(c.GRID_LEN-1):
#             if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
#                 mat[i][j] *= 2
#                 mat[i][j+1] = 0
#                 points += mat[i][j]
#                 done = True
#     return mat, done, points

# def up(game):
#     game = transpose(game)
#     game, done = cover_up(game)
#     game, done, points = merge(game, done)
#     game = cover_up(game)[0]
#     game = transpose(game)
#     return game, done, points

# def down(game):
#     game = reverse(transpose(game))
#     game, done = cover_up(game)
#     game, done, points = merge(game, done)
#     game = cover_up(game)[0]
#     game = transpose(reverse(game))
#     return game, done, points

# def left(game):
#     game, done = cover_up(game)
#     game, done, points = merge(game, done)
#     game = cover_up(game)[0]
#     return game, done, points

# def right(game):
#     game = reverse(game)
#     game, done = cover_up(game)
#     game, done, points = merge(game, done)
#     game = cover_up(game)[0]
#     game = reverse(game)
#     return game, done, points

# # Define the commands dictionary to map keys to functions
# commands = {
#     c.KEY_UP: up,
#     c.KEY_DOWN: down,
#     c.KEY_LEFT: left,
#     c.KEY_RIGHT: right
# }


import random
import constants as c

def new_game(n):
    matrix = [[0] * n for _ in range(n)]
    matrix = add_two(matrix)
    matrix = add_two(matrix)
    return matrix
def get_empty_cells(board):
    """
    Get a list of empty cells in the current board.
    Empty cells are represented by value 0.
    :param board: The 2048 game grid
    :return: List of positions (tuples) of empty cells
    """
    empty_cells = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                empty_cells.append((i, j))
    return empty_cells
def add_two(mat):
    a, b = random.randint(0, len(mat)-1), random.randint(0, len(mat)-1)
    while mat[a][b] != 0:
        a, b = random.randint(0, len(mat)-1), random.randint(0, len(mat)-1)
    mat[a][b] = 4 if random.randint(0, 9) == 9 else 2
    return mat

def game_state(mat):
    for row in mat:
        if 2048 in row:
            return 'win'
    for row in mat:
        if 0 in row:
            return 'not over'
    for i in range(c.GRID_LEN):
        for j in range(c.GRID_LEN - 1):
            if mat[i][j] == mat[i][j + 1]:
                return 'not over'
            if mat[j][i] == mat[j + 1][i]:
                return 'not over'
    return 'lose'

def reverse(mat):
    return [row[::-1] for row in mat]

def transpose(mat):
    return [[mat[j][i] for j in range(c.GRID_LEN)] for i in range(c.GRID_LEN)]

def cover_up(mat):
    new = [[0] * c.GRID_LEN for _ in range(c.GRID_LEN)]
    done = False
    for i in range(c.GRID_LEN):
        count = 0
        for j in range(c.GRID_LEN):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return new, done

def merge(mat, done):
    points = 0
    for i in range(c.GRID_LEN):
        for j in range(c.GRID_LEN-1):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] *= 2
                mat[i][j+1] = 0
                points += mat[i][j]
                done = True
    return mat, done, points

def up(game):
    game = transpose(game)
    game, done = cover_up(game)
    game, done, points = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(game)
    return game, done, points

def down(game):
    game = reverse(transpose(game))
    game, done = cover_up(game)
    game, done, points = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(reverse(game))
    return game, done, points

def left(game):
    game, done = cover_up(game)
    game, done, points = merge(game, done)
    game = cover_up(game)[0]
    return game, done, points

def right(game):
    game = reverse(game)
    game, done = cover_up(game)
    game, done, points = merge(game, done)
    game = cover_up(game)[0]
    game = reverse(game)
    return game, done, points

# Define the commands dictionary to map keys to functions
commands = {
    c.KEY_UP: up,
    c.KEY_DOWN: down,
    c.KEY_LEFT: left,
    c.KEY_RIGHT: right
}
