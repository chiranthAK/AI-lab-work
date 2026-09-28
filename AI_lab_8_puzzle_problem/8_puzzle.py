class EightPuzzleAgent:
    def __init__(self, initial_state):
        self.initial_state = tuple(tuple(row) for row in initial_state)
        self.goal_state = ((1, 2, 3), 
                            (4, 5, 6), 
                            (7, 8, 0)) 
        
    def find_blank(self, state):
        """Finds the row and column index of the empty tile (0)."""
        for r in range(3):
            for c in range(3):
                if state[r][c] == 0:
                    return r, c

    def get_neighbors(self, state):
        """Generates valid next states by moving the blank tile."""
        neighbors = []
        r, c = self.find_blank(state)
        
        moves = {
            'Up': (r - 1, c),
            'Down': (r + 1, c),
            'Left': (r, c - 1),
            'Right': (r, c + 1)
        }
        
        for move_name, (nr, nc) in moves.items():
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_state = [list(row) for row in state]
                new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
                neighbors.append((tuple(tuple(row) for row in new_state), move_name))
                
        return neighbors

    def solve_dfs(self):
        """Solves the puzzle using Iterative Depth-First Search."""
        stack = [(self.initial_state, [])]
        visited = set()
        
        nodes_expanded = 0

        while stack:
            current_state, path = stack.pop()
            
            if current_state in visited:
                continue
                
            visited.add(current_state)
            nodes_expanded += 1
            
            if current_state == self.goal_state:
                return path, nodes_expanded
                
            for neighbor, move in reversed(self.get_neighbors(current_state)):
                if neighbor not in visited:
                    stack.append((neighbor, path + [move]))
                    
        return None, nodes_expanded

def print_board(state):
    """Helper to display the board in a 3x3 format."""
    for row in state:
        print(" ".join(map(str, row)))
    print("-" * 10)

if __name__ == "__main__":
    initial_puzzle = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]
    
    agent = EightPuzzleAgent(initial_puzzle)
    
    print("Initial State:")
    print_board(agent.initial_state)
    
    print("Searching for solution via DFS...")
    solution_path, total_nodes = agent.solve_dfs()
    
    if solution_path is not None:
        print(f"Goal Reached successfully!")
        print(f"Total steps: {len(solution_path)}")
        print(f"Nodes expanded: {total_nodes}")
        print(f"Moves sequence: {', '.join(solution_path)}")
    else:
        print("No solution found or state is mathematically unsolvable.")
