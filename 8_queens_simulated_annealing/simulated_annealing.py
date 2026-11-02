import random
import math
import matplotlib.pyplot as plt


def conflicts(state):
    """Count attacking diagonal pairs."""
    n = len(state)
    count = 0

    for i in range(n):
        for j in range(i + 1, n):
            if abs(state[i] - state[j]) == abs(i - j):
                count += 1

    return count


def simulated_annealing(
    n,
    initial_temp=100,
    cooling_rate=0.995,
    min_temp=0.01,
    max_steps=100000,
    max_restarts=20
):
    if not isinstance(n, int) or n < 1:
        raise ValueError("N must be a positive integer.")

    if initial_temp <= 0 or min_temp <= 0:
        raise ValueError("Temperatures must be positive.")

    if not 0 < cooling_rate < 1:
        raise ValueError("Cooling rate must be between 0 and 1.")

    if max_steps < 1 or max_restarts < 1:
        raise ValueError("Step and restart limits must be positive.")

    if n == 1:
        return [0], [0], 0

    if n in (2, 3):
        return None, [], 0

    best_overall = None
    best_cost_overall = float("inf")
    best_history = []
    total_steps = 0

    for restart in range(max_restarts):
        state = list(range(n))
        random.shuffle(state)

        current_cost = conflicts(state)
        temperature = initial_temp
        history = [current_cost]

        for step in range(max_steps):
            if current_cost == 0:
                return state, history, total_steps

            if temperature < min_temp:
                break

            i, j = random.sample(range(n), 2)
            candidate = state[:]
            candidate[i], candidate[j] = candidate[j], candidate[i]

            new_cost = conflicts(candidate)
            delta = new_cost - current_cost

            if delta < 0 or random.random() < math.exp(-delta / temperature):
                state = candidate
                current_cost = new_cost

            history.append(current_cost)
            total_steps += 1

            if current_cost < best_cost_overall:
                best_cost_overall = current_cost
                best_overall = state[:]
                best_history = history[:]

            temperature *= cooling_rate

    if best_cost_overall == 0:
        return best_overall, best_history, total_steps

    return None, best_history, total_steps


def visualize_board(state, history, title):
    n = len(state)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    board = [[(r + c) % 2 for c in range(n)] for r in range(n)]
    axes[0].imshow(board, cmap="binary", interpolation="nearest")

    for col, row in enumerate(state):
        axes[0].text(
            col, row, "♛",
            ha="center", va="center",
            fontsize=max(10, min(30, 300 // n)),
            color="red"
        )

    axes[0].set_xticks(range(n))
    axes[0].set_yticks(range(n))
    axes[0].set_xlabel("Columns")
    axes[0].set_ylabel("Rows")
    axes[0].set_title(title)

    axes[1].plot(range(len(history)), history)
    axes[1].set_xlabel("Iterations")
    axes[1].set_ylabel("Number of conflicts")
    axes[1].set_title("Simulated Annealing Progress")
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    try:
        n = int(input("Enter number of queens: "))

        solution, history, steps = simulated_annealing(n)

        if solution is None:
            print("No solution found within the given search limits.")
            if history:
                print("Best conflicts reached:", min(history))
        else:
            print("Solution:", solution)
            print("Final conflicts:", conflicts(solution))
            print("Iterations performed:", steps)
            visualize_board(
                solution, history, "Simulated Annealing - N Queens"
            )

    except ValueError as e:
        print("Invalid input:", e)