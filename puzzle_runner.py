import json
import os
from puzzle_engine import CubicPuzzle
from search_algorithm import AdaptiveSearchEngine, KnowledgeBaseBuilder

# Configuration Parameters
EXPLORATION_DEPTH = 3
REBUILD_KNOWLEDGE = True
DATABASE_FILE = 'knowledge_base.json'

def main():
    """Main execution pipeline for the puzzle solving system"""
    
    print("=== Advanced Cubic Puzzle Solver ===")
    print("Initializing puzzle engine...")
    
    # Initialize puzzle system
    puzzle = CubicPuzzle(dimension=3)
    puzzle.display_configuration()
    print('=' * 50)
    
    # Knowledge base management
    knowledge_db = load_or_build_knowledge_base(puzzle)
    
    # Create challenge scenario
    print("Generating puzzle challenge...")
    scramble_moves = min(EXPLORATION_DEPTH, 5) if EXPLORATION_DEPTH < 5 else 5
    puzzle.randomize_configuration(min_operations=scramble_moves, max_operations=EXPLORATION_DEPTH)
    puzzle.display_configuration()
    print('=' * 50)
    
    # Solve the puzzle
    print("Initiating solution process...")
    search_engine = AdaptiveSearchEngine(knowledge_db)
    solution_sequence = search_engine.solve_puzzle(puzzle.export_state())
    
    print(f"Solution found: {solution_sequence}")
    
    # Apply solution and verify
    print("Applying solution moves...")
    apply_solution_moves(puzzle, solution_sequence)
    puzzle.display_configuration()
    
    print(f"Puzzle solved: {puzzle.is_completion_achieved()}")


def load_or_build_knowledge_base(puzzle: CubicPuzzle) -> dict:
    """Load existing knowledge base or build new one"""
    
    knowledge_db = None
    
    # Try to load existing knowledge base
    if os.path.exists(DATABASE_FILE):
        print(f"Loading existing knowledge base from {DATABASE_FILE}...")
        try:
            with open(DATABASE_FILE, 'r') as file:
                knowledge_db = json.load(file)
            print(f"Loaded {len(knowledge_db)} state mappings")
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            knowledge_db = None
    
    # Build new knowledge base if needed
    if knowledge_db is None or REBUILD_KNOWLEDGE:
        print("Building new knowledge base...")
        
        move_catalog = generate_move_catalog(puzzle.size)
        knowledge_db = KnowledgeBaseBuilder.construct_heuristic_database(
            target_state=puzzle.export_state(),
            move_set=move_catalog,
            exploration_depth=EXPLORATION_DEPTH,
            existing_knowledge=knowledge_db
        )
        
        # Save knowledge base
        print(f"Saving knowledge base to {DATABASE_FILE}...")
        try:
            with open(DATABASE_FILE, 'w', encoding='utf-8') as file:
                json.dump(knowledge_db, file, ensure_ascii=False, indent=2)
            print(f"Saved {len(knowledge_db)} state mappings")
        except Exception as e:
            print(f"Error saving knowledge base: {e}")
    
    return knowledge_db


def generate_move_catalog(puzzle_size: int) -> list:
    """Generate comprehensive catalog of all possible moves"""
    return [
        (rotation_type, layer_idx, direction)
        for rotation_type in ['horizontal', 'vertical', 'sideways']
        for direction in [0, 1]
        for layer_idx in range(puzzle_size)
    ]


def apply_solution_moves(puzzle: CubicPuzzle, move_sequence: list) -> None:
    """Apply sequence of moves to solve the puzzle"""
    
    for move in move_sequence:
        move_type, layer, direction = move
        
        if move_type == 'horizontal':
            puzzle.execute_horizontal_rotation(layer, direction)
        elif move_type == 'vertical':
            puzzle.execute_vertical_rotation(layer, direction)
        elif move_type == 'sideways':
            puzzle.execute_lateral_rotation(layer, direction)
        else:
            print(f"Warning: Unknown move type '{move_type}' - skipping")


def interactive_mode():
    """Interactive mode for manual puzzle manipulation"""
    
    puzzle = CubicPuzzle(dimension=3)
    
    print("=== Interactive Puzzle Mode ===")
    print("Commands:")
    print("  h <layer> <direction> - Horizontal rotation")
    print("  v <layer> <direction> - Vertical rotation") 
    print("  s <layer> <direction> - Sideways rotation")
    print("  show - Display puzzle")
    print("  reset - Reset to solved state")
    print("  scramble - Randomize puzzle")
    print("  quit - Exit")
    
    while True:
        puzzle.display_configuration()
        print(f"Solved: {puzzle.is_completion_achieved()}")
        
        try:
            command = input("\nEnter command: ").strip().lower().split()
            
            if not command:
                continue
            
            if command[0] == 'quit':
                break
            elif command[0] == 'show':
                continue  # Display handled at loop start
            elif command[0] == 'reset':
                puzzle.restore_factory_settings()
                print("Puzzle reset to solved state")
            elif command[0] == 'scramble':
                puzzle.randomize_configuration()
                print("Puzzle scrambled")
            elif command[0] in ['h', 'v', 's'] and len(command) == 3:
                layer = int(command[1])
                direction = int(command[2])
                
                if command[0] == 'h':
                    puzzle.execute_horizontal_rotation(layer, direction)
                elif command[0] == 'v':
                    puzzle.execute_vertical_rotation(layer, direction)
                elif command[0] == 's':
                    puzzle.execute_lateral_rotation(layer, direction)
            else:
                print("Invalid command format")
                
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_mode()
    else:
        main()