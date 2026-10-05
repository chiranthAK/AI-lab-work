import heapq

GOAL_STATE = (1, 2, 3, 
              8, 0, 4, 
              7, 6, 5)

def get_manhattan_distance(state):
    """Calculates the total Manhattan distance for the given state compared to the goal."""
    distance = 0
    for i, tile in enumerate(state):
        if tile != 0:
            current_row, current_col = divmod(i, 3)
            goal_row, goal_col = divmod(tile - 1, 3)
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

def get_neighbors(state):
    """Generates all valid neighboring states by moving the blank tile (0)."""
    neighbors = []
    blank_idx = state.index(0)
    row, col = divmod(blank_idx, 3)
    
    moves = [(-1, 0, 'Up'), (1, 0, 'Down'), (0, -1, 'Left'), (0, 1, 'Right')]
    
    for r_off, c_off, move_name in moves:
        new_row, new_col = row + r_off, col + c_off
        
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_blank_idx = new_row * 3 + new_col
            new_state = list(state)
            new_state[blank_idx], new_state[new_blank_idx] = new_state[new_blank_idx], new_state[blank_idx]
            neighbors.append((tuple(new_state), move_name))
            
    return neighbors

def solve_8_puzzle(start_state):
    """Solves the 8-puzzle using the A* algorithm."""
    start_h = get_manhattan_distance(start_state)
    pq = [(start_h, 0, start_state, [])]
    
    visited = {start_state: 0}
    
    while pq:
        f, g, current_state, path = heapq.heappop(pq)
        
        if current_state == GOAL_STATE:
            return path
            
        for neighbor, move in get_neighbors(current_state):
            new_g = g + 1
            
            if neighbor not in visited or new_g < visited[neighbor]:
                visited[neighbor] = new_g
                new_h = get_manhattan_distance(neighbor)
                new_f = new_g + new_h
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [move]))
                
    return None 
def print_board(state):
    """Utility function to print the board configuration in a 3x3 layout."""
    for i in range(0, 9, 3):
        print(f"{state[i]} {state[i+1]} {state[i+2]}")
    print()

if __name__ == "__main__":
    initial_state = (2, 8, 3, 
                     1, 6, 4, 
                     0, 7, 5)
    
    print("Initial State:")
    print_board(initial_state)
    
    solution_path = solve_8_puzzle(initial_state)
    
    if solution_path is not None:
        print(f"Success! Solved in {len(solution_path)} steps.")
        print(f"Sequence of moves: {', '.join(solution_path)}")
    else:
        print("This initial configuration is unsolvable.")
