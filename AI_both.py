from AI_expectimax import expectimax_decision

class AI:
    def __init__(self):
        self.depth = 4  # Set the depth for Expectimax

    def get_move(self, board):
        # Use Expectimax for decision-making
        return expectimax_decision(board, self.depth)
