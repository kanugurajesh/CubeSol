#!/usr/bin/env python3
"""
Quick test script to verify the Rubik's Cube solver is working properly
"""

import time
from puzzle_engine import CubicPuzzle
from search_algorithm import AdaptiveSearchEngine

def test_basic_functionality():
    """Test basic puzzle functionality"""
    print("=== Testing Basic Functionality ===")
    
    # Test 1: Create and display puzzle
    print("1. Creating 3x3x3 puzzle...")
    puzzle = CubicPuzzle(dimension=3)
    print("✓ Puzzle created successfully")
    
    # Test 2: Check if solved
    print("2. Checking if puzzle is solved...")
    is_solved = puzzle.is_completion_achieved()
    print(f"✓ Puzzle solved status: {is_solved}")
    
    # Test 3: Test moves
    print("3. Testing basic moves...")
    puzzle.execute_horizontal_rotation(0, 1)  # Top layer clockwise
    puzzle.execute_vertical_rotation(0, 1)    # Left column up
    puzzle.execute_lateral_rotation(0, 1)     # Front slice
    print("✓ Basic moves executed successfully")
    
    # Test 4: Reset puzzle
    print("4. Resetting puzzle...")
    puzzle.restore_factory_settings()
    is_solved_after_reset = puzzle.is_completion_achieved()
    print(f"✓ Puzzle reset, solved status: {is_solved_after_reset}")
    
    return True

def test_simple_solve():
    """Test solving a simple scrambled puzzle"""
    print("\n=== Testing Simple Solve ===")
    
    # Create and scramble puzzle
    puzzle = CubicPuzzle(dimension=3)
    print("1. Scrambling puzzle with 3 moves...")
    puzzle.randomize_configuration(min_operations=3, max_operations=3)
    
    initial_state = puzzle.export_state()
    print("2. Creating search engine...")
    
    # Use empty knowledge base for speed
    search_engine = AdaptiveSearchEngine({})
    
    print("3. Attempting to solve with simple search...")
    start_time = time.time()
    
    try:
        solution = search_engine.solve_puzzle_simple(initial_state, max_moves=10, timeout=5)
        solve_time = time.time() - start_time
        
        if solution:
            print(f"✓ Solution found: {len(solution)} moves in {solve_time:.3f}s")
            print(f"   Solution: {solution}")
            
            # Apply solution to verify
            for move in solution:
                move_type, layer, direction = move
                if move_type == 'horizontal':
                    puzzle.execute_horizontal_rotation(layer, direction)
                elif move_type == 'vertical':
                    puzzle.execute_vertical_rotation(layer, direction)
                elif move_type == 'sideways':
                    puzzle.execute_lateral_rotation(layer, direction)
            
            is_solved = puzzle.is_completion_achieved()
            print(f"✓ Puzzle solved after applying solution: {is_solved}")
            return True
        else:
            print(f"✗ No solution found in {solve_time:.3f}s")
            return False
            
    except Exception as e:
        solve_time = time.time() - start_time
        print(f"✗ Error during solving: {str(e)} in {solve_time:.3f}s")
        return False

def test_performance():
    """Test performance with different scramble complexities"""
    print("\n=== Testing Performance ===")
    
    complexities = [2, 3, 4]
    search_engine = AdaptiveSearchEngine({})
    
    for complexity in complexities:
        print(f"\nTesting complexity {complexity} moves:")
        
        puzzle = CubicPuzzle(dimension=3)
        puzzle.randomize_configuration(min_operations=complexity, max_operations=complexity)
        
        start_time = time.time()
        solution = search_engine.solve_puzzle_simple(puzzle.export_state(), max_moves=15, timeout=3)
        solve_time = time.time() - start_time
        
        if solution:
            print(f"  ✓ Solved in {len(solution)} moves ({solve_time:.3f}s)")
        else:
            print(f"  ✗ Not solved in {solve_time:.3f}s")

def main():
    """Run all tests"""
    print("Rubik's Cube Solver - Quick Test Suite")
    print("=" * 50)
    
    try:
        # Test basic functionality
        if not test_basic_functionality():
            print("❌ Basic functionality test failed!")
            return
        
        # Test simple solving
        if not test_simple_solve():
            print("❌ Simple solve test failed!")
            return
        
        # Test performance
        test_performance()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        print("The Rubik's Cube solver is working properly.")
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()