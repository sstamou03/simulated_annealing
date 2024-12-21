import time
from unruly_problem import UnrulyProblem
from search import simulated_annealing, exp_schedule

"""

Main function for solving the Unruly puzzle using Simulated Annealing.

"""


def decode_board(n, m, encoded):
    board = [['' for _ in range(m)] for _ in range(n)]
    x, y = 0, 0
    for char in encoded:
        steps = ord(char.lower()) - ord('a') + 1
        for _ in range(steps):
            if y == m:
                x, y = x + 1, 0
            if x < n and y < m:
                y += 1
        if x < n:
            board[x][y - 1] = 'B' if char.isupper() else 'W'
    return board

def print_board(board):
    for row in board:
        print(' '.join(cell if cell else '.' for cell in row))

def encode_solution(board):
    n, m = len(board), len(board[0])
    encoded = []
    steps = 0

    for i in range(n):
        for j in range(m):
            if board[i][j]: 
                letter = chr(ord('a') + steps) 
                if board[i][j] == 'B':  
                    encoded.append(letter.upper())
                else:  
                    encoded.append(letter)
                steps = 0  
            else:
                steps += 1 

    encoded.append('a')
    return f"{n}x{m}:{''.join(encoded)}"

def main():
    print('=' * 35)
    print('Welcome to the Unruly Solver Pro')
    print('=' * 35)

    filename = input("Enter the input filename: ")
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.readline().strip()
        dimensions, encode = data.split(':')
        n, m = map(int, dimensions.split('x'))

        board = decode_board(n, m, encode)
        print("Initial Board:")
        print_board(board)

        max_steps = int(input("Enter the maximum number of steps: "))
        schedule = exp_schedule(k=20, lam=0.005, limit=max_steps)

        problem = UnrulyProblem(board)

        print("\nRunning Simulated Annealing...")
        start_time = time.time()

        solution = simulated_annealing(problem, schedule=schedule)
        solution_cost = UnrulyProblem.evaluate_cost(solution)
        end_time = time.time()

        execution_time = end_time - start_time

        print("\nSolution Board:")
        print_board(solution)
        print(f"\nEncoded Solution: {encode_solution(solution)}")
        print(f"Solution Cost (violations): {solution_cost}")
        print(f"Execution Time: {execution_time:.2f} seconds")
        print(f"Steps Taken: {max_steps}")

if __name__ == "__main__":
    main()
