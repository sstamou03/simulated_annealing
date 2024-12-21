import random
from search import Problem

"""
This function implements the cost evaluation for a given board configuration in the Unruly puzzle.
The evaluation is based on the objective function f(s), which measures the violations of the game's rules:
- Balance Rule: Ensures an equal number of black and white cells in each row and column.
- No Consecutive Triplets Rule: Prevents three or more consecutive cells of the same color in any row or column.

The cost function f(s) is defined as:
f(s) = Σ|rb_i - rw_i| + Σ|cb_j - cw_j| + Σtri(s) + Σtrj(s)

Where:
- rb_i, rw_i: The number of black and white cells in row i.
- cb_j, cw_j: The number of black and white cells in column j.
- tri(s): The number of consecutive triplets in row i.
- trj(s): The number of consecutive triplets in column j.

The function calculates:
1. The absolute difference in the number of black and white cells in each row and column.
2. The total number of consecutive triplets of the same color (black or white) in rows and columns.

A valid solution minimizes the cost to 0, indicating no violations.
"""

class UnrulyProblem(Problem):
    def __init__(self, initial):

        super().__init__(initial)

    def actions(self, state):

        n, m = len(state), len(state[0])
        return [(i, j) for i in range(n) for j in range(m)]

    def result(self, state, action):

        i, j = action
        new_state = [row[:] for row in state]
        if new_state[i][j] == 'B':
            new_state[i][j] = 'W'
        elif new_state[i][j] == 'W':
            new_state[i][j] = 'B'
        else:
            new_state[i][j] = random.choice(['B', 'W'])
        return new_state

    def value(self, state):

        return -self.evaluate_cost(state)

    @staticmethod
    def evaluate_cost(board):

        n = len(board)
        m = len(board[0])
        cost = 0


        '''  
            f(s) = Σ|rb_i - rw_i| + Σ|cb_j - cw_j| + Σtri(s) + Σtrj(s)
        '''

        # Υπολογισμός |rb_i(s) - rw_i(s)| για κάθε γραμμή i
        for i in range(n):
            row_colors = [cell for cell in board[i] if cell]
            cost += abs(row_colors.count('B') - row_colors.count('W'))

        # Υπολογισμός |cb_j(s) - cw_j(s)| για κάθε στήλη j
        for j in range(m):
            col_colors = [board[i][j] for i in range(n) if board[i][j]]
            cost += abs(col_colors.count('B') - col_colors.count('W'))

        # Υπολογισμός των tri(s) (τριάδες συνεχόμενων ίδιου χρώματος) για γραμμές
        for i in range(n):
            for j in range(m - 2):
                if board[i][j] == board[i][j + 1] == board[i][j + 2] and board[i][j] != '':
                    cost += 1

        # Υπολογισμός των trj(s) (τριάδες συνεχόμενων ίδιου χρώματος) για στήλες
        for j in range(m):
            for i in range(n - 2):
                if board[i][j] == board[i + 1][j] == board[i + 2][j] and board[i][j] != '':
                    cost += 1

        return cost
