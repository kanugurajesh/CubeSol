import json
import os
import time
from puzzle_engine import CubicPuzzle
from search_algorithm import AdaptiveSearchEngine, KnowledgeBaseBuilder

# Configuration Parameters
EXPLORATION_DEPTH = 5  # Reduced from 10 to 5 for better performance
DATABASE_FILE = 'knowledge_base.json'
SOLVE_TIMEOUT = 30  # Maximum time to spend solving (seconds)

def main():
    """Main execution pipeline for the puzzle solving system"""
    
    print("=== Advanced Cubic Puzzle Solver ===")
    print("Initializing puzzle engine...")
    
    # Initialize puzzle system
    puzzle_size = 3
    puzzle = CubicPuzzle(dimension=puzzle_size)
    puzzle.display_configuration()
    print('=' * 50)
    
    # Smart knowledge base management
    knowledge_db, build_time = load_or_build_knowledge_base(puzzle_size, EXPLORATION_DEPTH)
    
    # Create challenge scenario
    print("Generating puzzle challenge...")
    scramble_moves = 5  # Reduced from 8 to 5 for better performance
    puzzle.randomize_configuration(min_operations=scramble_moves, max_operations=scramble_moves)
    puzzle.display_configuration()
    print(f'Scrambled with {scramble_moves} moves')
    print('=' * 50)
    
    # Solve with timing and algorithm comparison
    solve_with_comparison(puzzle, knowledge_db)
    
    # Performance analysis
    print("\n=== Performance Analysis ===")
    print(f"Knowledge base build time: {build_time:.2f}s")
    print(f"Knowledge base size: {len(knowledge_db)} states")
    print(f"Puzzle dimension: {puzzle_size}x{puzzle_size}x{puzzle_size}")
    print(f"Exploration depth: {EXPLORATION_DEPTH}")
    
    # Scalability demo
    print("\n=== Scalability Demo ===")
    scalability_demo()


def should_rebuild_knowledge_base(puzzle_size: int, exploration_depth: int) -> bool:
    """Smart decision on whether to rebuild knowledge base"""
    if not os.path.exists(DATABASE_FILE):
        print("No existing knowledge base found - building new one")
        return True
    
    try:
        with open(DATABASE_FILE, 'r') as f:
            data = json.load(f)
            metadata = data.get('metadata', {})
            
            stored_size = metadata.get('puzzle_size', 0)
            stored_depth = metadata.get('exploration_depth', 0)
            
            if stored_size != puzzle_size:
                print(f"Puzzle size changed ({stored_size} → {puzzle_size}) - rebuilding")
                return True
            
            if stored_depth < exploration_depth:
                print(f"Exploration depth increased ({stored_depth} → {exploration_depth}) - rebuilding")
                return True
            
            print(f"Using existing knowledge base (size: {stored_size}, depth: {stored_depth})")
            return False
            
    except Exception as e:
        print(f"Error reading knowledge base metadata: {e} - rebuilding")
        return True


def load_or_build_knowledge_base(puzzle_size: int, exploration_depth: int) -> tuple:
    """Load existing knowledge base or build new one with smart caching"""
    
    build_time = 0
    knowledge_db = None
    
    # Check if we need to rebuild
    if should_rebuild_knowledge_base(puzzle_size, exploration_depth):
        start_time = time.time()
        
        print("Building new knowledge base...")
        temp_puzzle = CubicPuzzle(dimension=puzzle_size)
        move_catalog = generate_move_catalog(puzzle_size)
        
        knowledge_db = KnowledgeBaseBuilder.construct_heuristic_database(
            target_state=temp_puzzle.export_state(),
            move_set=move_catalog,
            exploration_depth=exploration_depth
        )
        
        build_time = time.time() - start_time
        
        # Save with metadata
        print(f"Saving knowledge base to {DATABASE_FILE}...")
        try:
            data_to_save = {
                'metadata': {
                    'puzzle_size': puzzle_size,
                    'exploration_depth': exploration_depth,
                    'build_time': build_time,
                    'total_states': len(knowledge_db)
                },
                'knowledge_base': knowledge_db
            }
            
            with open(DATABASE_FILE, 'w', encoding='utf-8') as file:
                json.dump(data_to_save, file, ensure_ascii=False, indent=2)
            print(f"Saved {len(knowledge_db)} state mappings")
            
        except Exception as e:
            print(f"Error saving knowledge base: {e}")
    
    else:
        # Load existing knowledge base
        try:
            with open(DATABASE_FILE, 'r') as file:
                data = json.load(file)
                knowledge_db = data.get('knowledge_base', data)  # Backward compatibility
                build_time = data.get('metadata', {}).get('build_time', 0)
            print(f"Loaded {len(knowledge_db)} state mappings")
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            return load_or_build_knowledge_base(puzzle_size, exploration_depth)  # Fallback to rebuild
    
    return knowledge_db, build_time


def solve_with_comparison(puzzle: CubicPuzzle, knowledge_db: dict):
    """Solve puzzle with algorithm comparison and timing"""
    initial_state = puzzle.export_state()
    
    print("=== Algorithm Comparison ===")
    
    # Method 1: BFS (fast for shallow solutions) - with timeout
    print("1. Breadth-First Search (max depth 6):")
    start_time = time.time()
    search_engine = AdaptiveSearchEngine(knowledge_db)
    bfs_solution = None
    
    try:
        bfs_solution = search_engine._breadth_first_search_with_timeout(initial_state, max_depth=6, timeout=10)
        bfs_time = time.time() - start_time
        
        if bfs_solution:
            print(f"   ✓ Solution found: {len(bfs_solution)} moves in {bfs_time:.3f}s")
            print(f"   Solution: {bfs_solution}")
        else:
            print(f"   ✗ No solution found (too complex) in {bfs_time:.3f}s")
    except Exception as e:
        bfs_time = time.time() - start_time
        print(f"   ✗ BFS failed: {str(e)} in {bfs_time:.3f}s")
    
    # Method 2: Bidirectional Search - with timeout
    print("\n2. Bidirectional Search:")
    start_time = time.time()
    bidirectional_solution = None
    
    try:
        bidirectional_solution = search_engine._bidirectional_search_with_timeout(initial_state, timeout=10)
        bidirectional_time = time.time() - start_time
        
        if bidirectional_solution:
            print(f"   ✓ Solution found: {len(bidirectional_solution)} moves in {bidirectional_time:.3f}s")
            print(f"   Solution: {bidirectional_solution}")
        else:
            print(f"   ✗ No solution found in {bidirectional_time:.3f}s")
    except Exception as e:
        bidirectional_time = time.time() - start_time
        print(f"   ✗ Bidirectional search failed: {str(e)} in {bidirectional_time:.3f}s")
    
    # Method 3: Simple heuristic search (faster alternative)
    print("\n3. Simple Heuristic Search:")
    start_time = time.time()
    simple_solution = None
    
    try:
        simple_solution = search_engine.solve_puzzle_simple(initial_state, max_moves=20, timeout=10)
        simple_time = time.time() - start_time
        
        if simple_solution:
            print(f"   ✓ Solution found: {len(simple_solution)} moves in {simple_time:.3f}s")
            print(f"   Solution: {simple_solution}")
        else:
            print(f"   ✗ No solution found in {simple_time:.3f}s")
    except Exception as e:
        simple_time = time.time() - start_time
        print(f"   ✗ Simple search failed: {str(e)} in {simple_time:.3f}s")
    
    # Use the best solution found
    best_solution = bfs_solution or bidirectional_solution or simple_solution
    
    if best_solution:
        print(f"\n=== Applying Best Solution ({len(best_solution)} moves) ===")
        apply_solution_moves(puzzle, best_solution)
        puzzle.display_configuration()
        print(f"Puzzle solved: {puzzle.is_completion_achieved()}")
    else:
        print("\n=== No Solution Found ===")
        print("Try reducing the scramble complexity or increasing timeout limits.")


def scalability_demo():
    """Demonstrate scalability across different cube sizes"""
    sizes_to_test = [2, 3]  # 4x4 would take too long for demo
    
    for size in sizes_to_test:
        print(f"\n--- Testing {size}x{size}x{size} Cube ---")
        
        # Create and scramble cube
        test_puzzle = CubicPuzzle(dimension=size)
        test_puzzle.randomize_configuration(min_operations=5, max_operations=5)
        
        # Quick solve with BFS
        start_time = time.time()
        engine = AdaptiveSearchEngine({})  # Empty knowledge base for speed
        solution = engine._breadth_first_search(test_puzzle.export_state(), max_depth=8)
        solve_time = time.time() - start_time
        
        if solution:
            print(f"   ✓ Solved in {len(solution)} moves ({solve_time:.3f}s)")
        else:
            print(f"   ✗ Not solved in quick test ({solve_time:.3f}s)")


def complexity_analysis():
    """Display complexity analysis of the algorithms"""
    print("\n=== Algorithm Complexity Analysis ===")
    print("1. Breadth-First Search:")
    print("   Time: O(b^d) where b=18 (moves), d=depth")
    print("   Space: O(b^d) - stores all states at current level")
    print("   Best for: Shallow solutions (≤6 moves)")
    
    print("\n2. Bidirectional Search:")
    print("   Time: O(b^(d/2)) - meets in middle")
    print("   Space: O(b^(d/2)) - much better than BFS")
    print("   Best for: Medium complexity (6-12 moves)")
    
    print("\n3. IDA* with Pattern Database:")
    print("   Time: O(b^d) worst case, but heavily pruned")
    print("   Space: O(d) - only stores current path")
    print("   Best for: Complex puzzles (12+ moves)")
    
    print("\n4. Pattern Database:")
    print("   Preprocessing: O(|S|) where S is state space")
    print("   Lookup: O(1) - constant time heuristic")
    print("   Memory: Stores states up to exploration depth")


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
    
    for i, move in enumerate(move_sequence):
        move_type, layer, direction = move
        
        print(f"Move {i+1}/{len(move_sequence)}: {move_type[0].upper()}{layer}{'′' if direction == 0 else ''}")
        
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
    print("  scramble [moves] - Randomize puzzle")
    print("  solve - Auto-solve current state")
    print("  analysis - Show complexity analysis")
    print("  quit - Exit")
    
    # Load knowledge base for solving
    knowledge_db, _ = load_or_build_knowledge_base(3, EXPLORATION_DEPTH)
    
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
                moves = int(command[1]) if len(command) > 1 else 10
                puzzle.randomize_configuration(min_operations=moves, max_operations=moves)
                print(f"Puzzle scrambled with {moves} moves")
            elif command[0] == 'solve':
                print("Solving puzzle...")
                engine = AdaptiveSearchEngine(knowledge_db)
                solution = engine.solve_puzzle(puzzle.export_state())
                if solution:
                    print(f"Solution found: {len(solution)} moves")
                    apply_solution_moves(puzzle, solution)
                else:
                    print("No solution found")
            elif command[0] == 'analysis':
                complexity_analysis()
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
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--interactive':
            interactive_mode()
        elif sys.argv[1] == '--analysis':
            complexity_analysis()
        elif sys.argv[1] == '--demo':
            # Quick demo mode
            EXPLORATION_DEPTH = 5
            main()
    else:
        main()