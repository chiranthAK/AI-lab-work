def print_board(board):
    for row in range(0, 9, 3):
        print(f"{board[row]} | {board[row+1]} | {board[row+2]}")
        if row < 6:
            print("--+---+--")
    print()

def check_winner(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  
        [0, 4, 8], [2, 4, 6]             
    ]
    return any(all(board[i] == player for i in cond) for cond in win_conditions)

def is_board_full(board):
    return all(cell != ' ' for cell in board)

def find_winning_path(board, current_player, cost=0):
    if check_winner(board, 'X'):
        return [board], cost
    if check_winner(board, 'O') or is_board_full(board):
        return None, float('inf')

    best_path = None
    min_cost = float('inf')

    for i in range(9):
        if board[i] == ' ' :
            new_board = list(board)
            new_board[i] = current_player
            next_player = 'O' if current_player == 'X' else 'X'
            
            path, p_cost = find_winning_path(new_board, next_player, cost + 1)
            if path and p_cost < min_cost:
                min_cost = p_cost
                best_path = [board] + path

    return best_path, min_cost

initial_state = [
    'O', ' ', 'X',
    'X', ' ', ' ',
    'X', 'O', 'O'
]

print("Initial Board State:")
print_board(initial_state)

path, total_cost = find_winning_path(initial_state, current_player='X')

if path and total_cost != float('inf'):
    print(f"Goal Reached! Total Path Cost (Number of moves): {total_cost}\n")
    print("Path sequence of board states:")
    for step, state in enumerate(path):
        print(f"Step {step}:")
        print_board(state)
else:
    print("No winning path found from this state.")
