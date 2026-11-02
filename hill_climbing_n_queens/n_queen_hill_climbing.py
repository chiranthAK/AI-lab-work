import random
import matplotlib.pyplot as plt


def conflicts(state):
    """Count pairs of queens attacking diagonally."""
    n = len(state)
    count = 0

    for i in range(n):
        for j in range(i + 1, n):
            if abs(state[i] - state[j]) == abs(i - j):
                count += 1

    return count


def hill_climbing(n, max_restarts=1000):
    if not isinstance(n, int) or n < 1:
        raise ValueError("N must be a positive integer.")

    if n == 1:
        return [0], [0], 0

    if n in (2, 3):
        return None, [], 0

    total_steps = 0

    for restart in range(max_restarts):
        state = list(range(n))
        random.shuffle(state)

        history = [conflicts(state)]

        while True:
            current_cost = conflicts(state)
            best_state = state[:]
            best_cost = current_cost

            # Try every possible pairwise swap
            for i in range(n):
                for j in range(i + 1, n):
                    candidate = state[:]
                    candidate[i], candidate[j] = (
                        candidate[j], candidate[i]
                    )

                    cost = conflicts(candidate)

                    if cost < best_cost:
                        best_cost = cost
                        best_state = candidate

            # No better neighbor: local minimum reached
            if best_cost >= current_cost:
                break

            state = best_state
            history.append(best_cost)
            total_steps += 1

            if best_cost == 0:
                return state, history, total_steps

    return None, [], total_steps


def visualize_board(state, history, title):
    n = len(state)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Chessboard
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

    # Search progress
    axes[1].plot(range(len(history)), history, marker="o")
    axes[1].set_xlabel("Successful moves")
    axes[1].set_ylabel("Number of conflicts")
    axes[1].set_title("Hill Climbing Progress")
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    try:
        n = int(input("Enter number of queens: "))

        solution, history, steps = hill_climbing(n)

        if solution is None:
            print("No solution found. Try increasing max_restarts.")
        else:
            print("Solution:", solution)
            print("Final conflicts:", conflicts(solution))
            print("Successful moves:", len(history) - 1)
            visualize_board(solution, history, "Hill Climbing - N Queens")

    except ValueError as e:
        print("Invalid input:", e)