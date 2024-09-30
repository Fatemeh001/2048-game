import copy
import constants as c
import logic
from AI_heuristicsForExpectimax import AI_Heuristics  # Import your heuristics

# Define commands for movement
commands = {
    c.KEY_UP: logic.up,
    c.KEY_DOWN: logic.down,
    c.KEY_LEFT: logic.left,
    c.KEY_RIGHT: logic.right
}

# Initialize heuristics
heuristics = AI_Heuristics()

def expectimax_decision(board, depth=4):  # Start with depth 4
    best_move = None
    best_score = -float('inf')

    for move in commands:
        new_board, done, points = commands[move](board)
        if not done:
            continue

        # Call expectimax with depth-1
        score = expectimax(new_board, depth - 1, False)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move

def expectimax(board, depth, is_maximizing_player):
    # Base case: stop when depth is 0 or game is over
    if depth == 0 or logic.game_state(board) != 'not over':
        return evaluate_board(board)  # Use the combined heuristic evaluation

    if is_maximizing_player:
        # Maximizing player (AI's turn)
        best_score = -float('inf')
        for move in commands:
            new_board, done, points = commands[move](board)
            if not done:
                continue
            score = expectimax(new_board, depth - 1, False)
            best_score = max(best_score, score)
        return best_score
    else:
        # Minimizing player (chance node: simulate placing new tiles)
        empty_cells = logic.get_empty_cells(board)
        if not empty_cells:
            return evaluate_board(board)  # No empty cells, evaluate the board

        score_sum = 0
        for cell in empty_cells:
            # Simulate adding '2' and '4' tiles to the board
            board_2 = copy.deepcopy(board)
            board_4 = copy.deepcopy(board)
            board_2[cell[0]][cell[1]] = 2
            board_4[cell[0]][cell[1]] = 4

            # Expectimax for both possibilities
            score_sum += 0.9 * expectimax(board_2, depth - 1, True)  # 90% chance of adding a 2
            score_sum += 0.1 * expectimax(board_4, depth - 1, True)  # 10% chance of adding a 4

        return score_sum / len(empty_cells)  # Average the score

def evaluate_board(board):
    """Evaluate the board using the heuristic approach."""
    # Simply use the heuristics' evaluation on the board matrix
    score = 0
    for strategy in heuristics.strategies:
        strategy_function = heuristics.strategy_functions.get(strategy, None)
        if strategy_function:
            score += strategy_function(board)
    return score

    
 