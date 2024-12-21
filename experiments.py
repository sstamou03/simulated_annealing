import random
import time
from unruly_problem import UnrulyProblem
from search import simulated_annealing, exp_schedule
from main import decode_board, print_board
import pandas as pd

def run_experiments(board, step_values, runs=20):
    """
    Run multiple experiments with increasing max_steps values.
    :param board: The initial board configuration.
    :param step_values: List of max_steps values to test.
    :param runs: Number of runs for each max_steps value.
    :return: A list of results for each max_steps value.
    """
    results = []

    for max_steps in step_values:
        success_count = 0
        total_violations = 0
        total_steps = 0
        total_time = 0

        for _ in range(runs):
            # Initialize the random seed with the current time
            random.seed(time.time())

            schedule = exp_schedule(k=20, lam=0.005, limit=max_steps)
            problem = UnrulyProblem(board)

            start_time = time.time()
            solution = simulated_annealing(problem, schedule=schedule)
            end_time = time.time()

            solution_cost = UnrulyProblem.evaluate_cost(solution)
            total_time += (end_time - start_time)

            if solution_cost == 0:
                success_count += 1
            else:
                total_violations += solution_cost

            total_steps += max_steps

        avg_violations = total_violations / (runs - success_count) if (runs - success_count) > 0 else 0
        avg_time = total_time / runs

        results.append({
            "Max Steps": max_steps,
            "Success Rate (%)": success_count / runs * 100,
            "Average Violations": avg_violations,
            "Average Steps": total_steps / runs,
            "Average Time (s)": avg_time
        })

    return results

if __name__ == "__main__":
    dimensions = "8x8"
    encoded_board = "bceadEDgCcAgCcabBi"
    n, m = map(int, dimensions.split('x'))
    board = decode_board(n, m, encoded_board)

    step_values = [50, 100, 500, 800, 1000, 2000, 5000, 8000, 10000]
    runs_per_step = 20  

    experiment_results = run_experiments(board, step_values, runs_per_step)

    df_results = pd.DataFrame(experiment_results)

    print(df_results)

    df_results.to_csv("experiment_results.csv", index=False)

    print("\nResults saved to 'experiment_results.csv'")