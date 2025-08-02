import time
import statistics
import json
import matplotlib.pyplot as plt
import threading
from puzzle_engine import CubicPuzzle
from search_algorithm import AdaptiveSearchEngine, KnowledgeBaseBuilder

class PerformanceBenchmark:
    """
    Comprehensive performance benchmarking suite for the Rubik's Cube solver
    """
    
    def __init__(self, puzzle_sizes=[2, 3], exploration_depths=[5, 10, 15]):
        self.puzzle_sizes = puzzle_sizes
        self.exploration_depths = exploration_depths
        self.results = {}
        self.knowledge_base_cache = {}  # Cache for knowledge bases
        
    def get_or_build_knowledge_base(self, cube_size, exploration_depth):
        """Get cached knowledge base or build new one if not exists"""
        cache_key = (cube_size, exploration_depth)
        
        if cache_key not in self.knowledge_base_cache:
            print(f"   Building knowledge base for {cube_size}x{cube_size}x{cube_size}, depth {exploration_depth}...")
            puzzle = CubicPuzzle(dimension=cube_size)
            from puzzle_runner import generate_move_catalog
            move_catalog = generate_move_catalog(cube_size)
            
            start_time = time.time()
            knowledge_db = KnowledgeBaseBuilder.construct_heuristic_database(
                target_state=puzzle.export_state(),
                move_set=move_catalog,
                exploration_depth=exploration_depth
            )
            build_time = time.time() - start_time
            
            self.knowledge_base_cache[cache_key] = {
                'knowledge_db': knowledge_db,
                'build_time': build_time,
                'size': len(knowledge_db)
            }
            print(f"   Built in {build_time:.2f}s, {len(knowledge_db)} states")
        else:
            print(f"   Using cached knowledge base for {cube_size}x{cube_size}x{cube_size}, depth {exploration_depth}")
            
        return self.knowledge_base_cache[cache_key]
    
    def run_with_timeout(self, func, timeout_seconds=30):
        """Run a function with a timeout (Windows compatible)"""
        result = [None]
        exception = [None]
        timed_out = [False]
        
        def target():
            try:
                result[0] = func()
            except Exception as e:
                exception[0] = e
        
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join(timeout_seconds)
        
        if thread.is_alive():
            timed_out[0] = True
            return None, True  # None, timed_out
        
        if exception[0]:
            raise exception[0]
            
        return result[0], False  # result, not_timed_out
        
    def run_full_benchmark(self):
        """Run comprehensive benchmark suite"""
        print("🚀 Starting Comprehensive Performance Benchmark")
        print("=" * 60)
        
        # Test 1: Algorithm Comparison
        self.benchmark_algorithms()
        
        # Test 2: Scalability Analysis
        self.benchmark_scalability()
        
        # Test 3: Knowledge Base Impact
        self.benchmark_knowledge_base()
        
        # Test 4: Move Complexity Analysis
        self.benchmark_move_complexity()
        
        # Generate report
        self.generate_report()
        
    def benchmark_algorithms(self):
        """Compare performance of different solving algorithms"""
        print("\n📊 Algorithm Performance Comparison")
        print("-" * 40)
        
        puzzle = CubicPuzzle(dimension=3)
        scramble_levels = [3, 6, 9, 12, 15]
        algorithms = ['BFS', 'Bidirectional', 'IDA*']
        
        self.results['algorithms'] = {}
        
        # Pre-build knowledge base for IDA* to avoid rebuilding in trial loop
        ida_star_kb = None
        for algorithm in algorithms:
            if algorithm == 'IDA*':
                kb_data = self.get_or_build_knowledge_base(3, 8)
                ida_star_kb = kb_data['knowledge_db']
                break
        
        for scramble_count in scramble_levels:
            print(f"\nTesting with {scramble_count} scramble moves:")
            self.results['algorithms'][scramble_count] = {}
            
            # Test multiple scrambles for statistical significance
            for algorithm in algorithms:
                times = []
                solution_lengths = []
                success_count = 0
                
                # Select appropriate knowledge base
                knowledge_db = ida_star_kb if algorithm == 'IDA*' else {}
                
                for trial in range(5):  # 5 trials per scramble level
                    puzzle.restore_factory_settings()
                    puzzle.randomize_configuration(scramble_count, scramble_count)
                    
                    engine = AdaptiveSearchEngine(knowledge_db, depth_limit=20)
                    
                    # Define the solving function
                    def solve_func():
                        if algorithm == 'BFS':
                            # Limit BFS depth based on scramble complexity
                            max_depth = min(scramble_count + 2, 8)
                            return engine._breadth_first_search(puzzle.export_state(), max_depth=max_depth)
                        elif algorithm == 'Bidirectional':
                            return engine._bidirectional_search(puzzle.export_state())
                        else:  # IDA*
                            return engine._ida_star_search(puzzle.export_state())
                    
                    start_time = time.time()
                    
                    try:
                        # Set timeout based on algorithm and scramble complexity
                        timeout = 5 if algorithm == 'BFS' and scramble_count >= 6 else 30
                        solution, timed_out = self.run_with_timeout(solve_func, timeout)
                        
                        solve_time = time.time() - start_time
                        
                        if timed_out:
                            print(f"   {algorithm} timed out after {timeout}s")
                        elif solution:
                            times.append(solve_time)
                            solution_lengths.append(len(solution))
                            success_count += 1
                        
                    except Exception as e:
                        print(f"   Error in {algorithm}: {e}")
                
                # Calculate statistics
                if times:
                    avg_time = statistics.mean(times)
                    avg_length = statistics.mean(solution_lengths)
                    success_rate = success_count / 5 * 100
                    
                    print(f"   {algorithm:12}: {avg_time:.3f}s avg, {avg_length:.1f} moves avg, {success_rate:.0f}% success")
                    
                    self.results['algorithms'][scramble_count][algorithm] = {
                        'avg_time': avg_time,
                        'avg_length': avg_length,
                        'success_rate': success_rate,
                        'times': times,
                        'lengths': solution_lengths
                    }
                else:
                    print(f"   {algorithm:12}: No solutions found")
                    self.results['algorithms'][scramble_count][algorithm] = {
                        'avg_time': float('inf'),
                        'avg_length': float('inf'),
                        'success_rate': 0,
                        'times': [],
                        'lengths': []
                    }
    
    def benchmark_scalability(self):
        """Test scalability across different cube sizes"""
        print("\n📈 Scalability Analysis")
        print("-" * 40)
        
        self.results['scalability'] = {}
        
        for size in self.puzzle_sizes:
            print(f"\nTesting {size}x{size}x{size} cube:")
            self.results['scalability'][size] = {}
            
            # Limit exploration depth for larger cubes
            exploration_depth = min(8, 12 - size)
            
            # Use cached knowledge base
            kb_data = self.get_or_build_knowledge_base(size, exploration_depth)
            knowledge_db = kb_data['knowledge_db']
            kb_build_time = kb_data['build_time']
            
            # Test solving time
            puzzle = CubicPuzzle(dimension=size)
            puzzle.randomize_configuration(5, 5)  # Fixed scramble for comparison
            engine = AdaptiveSearchEngine(knowledge_db)
            
            start_time = time.time()
            solution = engine.solve_puzzle(puzzle.export_state())
            solve_time = time.time() - start_time
            
            print(f"   Knowledge base: {kb_build_time:.2f}s, {len(knowledge_db)} states")
            print(f"   Solving time: {solve_time:.3f}s, {len(solution) if solution else 'No solution'} moves")
            
            self.results['scalability'][size] = {
                'kb_build_time': kb_build_time,
                'kb_size': len(knowledge_db),
                'solve_time': solve_time,
                'solution_length': len(solution) if solution else None,
                'exploration_depth': exploration_depth
            }
    
    def benchmark_knowledge_base(self):
        """Analyze impact of knowledge base depth on performance"""
        print("\n🧠 Knowledge Base Impact Analysis")
        print("-" * 40)
        
        self.results['knowledge_base'] = {}
        puzzle = CubicPuzzle(dimension=3)
        
        for depth in self.exploration_depths:
            print(f"\nTesting exploration depth {depth}:")
            
            # Use cached knowledge base
            kb_data = self.get_or_build_knowledge_base(3, depth)
            knowledge_db = kb_data['knowledge_db']
            kb_build_time = kb_data['build_time']
            
            # Test solving with different scramble complexities
            solve_times = []
            solution_lengths = []
            
            for scramble_moves in [5, 8, 12]:
                puzzle.restore_factory_settings()
                puzzle.randomize_configuration(scramble_moves, scramble_moves)
                
                engine = AdaptiveSearchEngine(knowledge_db)
                start_time = time.time()
                solution = engine.solve_puzzle(puzzle.export_state())
                solve_time = time.time() - start_time
                
                if solution:
                    solve_times.append(solve_time)
                    solution_lengths.append(len(solution))
            
            avg_solve_time = statistics.mean(solve_times) if solve_times else float('inf')
            avg_solution_length = statistics.mean(solution_lengths) if solution_lengths else float('inf')
            
            print(f"   Build time: {kb_build_time:.2f}s, DB size: {len(knowledge_db)}")
            print(f"   Avg solve time: {avg_solve_time:.3f}s, Avg solution: {avg_solution_length:.1f} moves")
            
            self.results['knowledge_base'][depth] = {
                'build_time': kb_build_time,
                'db_size': len(knowledge_db),
                'avg_solve_time': avg_solve_time,
                'avg_solution_length': avg_solution_length,
                'solve_times': solve_times,
                'solution_lengths': solution_lengths
            }
    
    def benchmark_move_complexity(self):
        """Analyze relationship between scramble complexity and solving difficulty"""
        print("\n🎲 Move Complexity Analysis")
        print("-" * 40)
        
        self.results['complexity'] = {}
        puzzle = CubicPuzzle(dimension=3)
        
        # Use cached knowledge base
        kb_data = self.get_or_build_knowledge_base(3, 10)
        knowledge_db = kb_data['knowledge_db']
        
        scramble_levels = range(1, 21, 2)  # 1, 3, 5, ..., 19
        
        for scramble_count in scramble_levels:
            times = []
            lengths = []
            success_count = 0
            
            print(f"Testing {scramble_count} scramble moves: ", end="")
            
            for trial in range(3):  # 3 trials per level
                puzzle.restore_factory_settings()
                puzzle.randomize_configuration(scramble_count, scramble_count)
                
                engine = AdaptiveSearchEngine(knowledge_db)
                start_time = time.time()
                
                try:
                    solution = engine.solve_puzzle(puzzle.export_state())
                    solve_time = time.time() - start_time
                    
                    if solution:
                        times.append(solve_time)
                        lengths.append(len(solution))
                        success_count += 1
                        print("✓", end="")
                    else:
                        print("✗", end="")
                        
                except Exception:
                    print("E", end="")
            
            avg_time = statistics.mean(times) if times else float('inf')
            avg_length = statistics.mean(lengths) if lengths else float('inf')
            success_rate = success_count / 3 * 100
            
            print(f" | {avg_time:.3f}s, {avg_length:.1f} moves, {success_rate:.0f}% success")
            
            self.results['complexity'][scramble_count] = {
                'avg_time': avg_time,
                'avg_length': avg_length,
                'success_rate': success_rate,
                'sample_size': 3
            }
    
    def generate_report(self):
        """Generate comprehensive performance report"""
        print("\n" + "=" * 60)
        print("📋 PERFORMANCE BENCHMARK REPORT")
        print("=" * 60)
        
        # Algorithm Performance Summary
        print("\n🏆 Best Performing Algorithms:")
        for scramble_level in [6, 12]:
            if scramble_level in self.results.get('algorithms', {}):
                print(f"\n{scramble_level} moves scramble:")
                algos = self.results['algorithms'][scramble_level]
                
                # Sort by average time
                sorted_algos = sorted(
                    [(name, data['avg_time'], data['success_rate']) 
                     for name, data in algos.items() if data['success_rate'] > 0],
                    key=lambda x: x[1]
                )
                
                for i, (name, time, success) in enumerate(sorted_algos):
                    medal = ["🥇", "🥈", "🥉"][i] if i < 3 else "  "
                    print(f"   {medal} {name}: {time:.3f}s ({success:.0f}% success)")
        
        # Scalability Summary
        print("\n📊 Scalability Results:")
        if 'scalability' in self.results:
            for size, data in self.results['scalability'].items():
                kb_size = data['kb_size']
                kb_time = data['kb_build_time']
                solve_time = data['solve_time']
                print(f"   {size}x{size}x{size}: {kb_time:.1f}s build, {solve_time:.3f}s solve, {kb_size} states")
        
        # Knowledge Base Impact
        print("\n🧠 Knowledge Base Optimization:")
        if 'knowledge_base' in self.results:
            best_depth = min(
                self.results['knowledge_base'].items(),
                key=lambda x: x[1]['avg_solve_time'] + x[1]['build_time'] / 10
            )
            print(f"   Optimal depth: {best_depth[0]} (balanced speed vs build time)")
            print(f"   Performance: {best_depth[1]['avg_solve_time']:.3f}s solve, {best_depth[1]['build_time']:.1f}s build")
        
        # Complexity Analysis
        print("\n📈 Complexity Insights:")
        if 'complexity' in self.results:
            # Find the knee of the curve (where difficulty increases significantly)
            times = [(k, v['avg_time']) for k, v in self.results['complexity'].items() 
                    if v['avg_time'] != float('inf')]
            
            if len(times) > 2:
                # Simple analysis: find where time > 2x the time at scramble=5
                baseline = next((t for s, t in times if s == 5), None)
                if baseline:
                    knee_point = next((s for s, t in times if t > baseline * 2), None)
                    if knee_point:
                        print(f"   Difficulty increases significantly at {knee_point}+ scramble moves")
                        print(f"   BFS effective up to ~6 moves, IDA* needed for 12+ moves")
        
        # Save detailed results
        with open('benchmark_results.json', 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n💾 Detailed results saved to benchmark_results.json")
        
        # Performance recommendations
        print("\n🎯 Performance Recommendations:")
        print("   • Use BFS for scrambles ≤ 6 moves (fastest)")
        print("   • Use Bidirectional search for 6-12 moves (balanced)")
        print("   • Use IDA* with pattern DB for 12+ moves (comprehensive)")
        print("   • Build knowledge base with depth 8-12 for optimal balance")
        print("   • Consider caching for repeated solves")
        
    def plot_results(self):
        """Generate performance visualization plots"""
        try:
            import matplotlib.pyplot as plt
            
            # Plot 1: Algorithm comparison
            if 'algorithms' in self.results:
                plt.figure(figsize=(12, 8))
                
                scramble_levels = sorted(self.results['algorithms'].keys())
                algorithms = ['BFS', 'Bidirectional', 'IDA*']
                
                for algo in algorithms:
                    times = []
                    for level in scramble_levels:
                        time_val = self.results['algorithms'][level].get(algo, {}).get('avg_time', float('inf'))
                        times.append(time_val if time_val != float('inf') else None)
                    
                    # Filter out None values for plotting
                    valid_levels = [l for l, t in zip(scramble_levels, times) if t is not None]
                    valid_times = [t for t in times if t is not None]
                    
                    if valid_times:
                        plt.plot(valid_levels, valid_times, marker='o', label=algo, linewidth=2)
                
                plt.xlabel('Scramble Moves')
                plt.ylabel('Average Solve Time (seconds)')
                plt.title('Algorithm Performance vs Scramble Complexity')
                plt.legend()
                plt.grid(True, alpha=0.3)
                plt.yscale('log')
                plt.savefig('algorithm_performance.png', dpi=300, bbox_inches='tight')
                plt.show()
                
                print("📊 Performance plot saved as 'algorithm_performance.png'")
                
        except ImportError:
            print("📊 Install matplotlib to generate performance plots: pip install matplotlib")


def main():
    """Run the performance benchmark"""
    # Quick benchmark
    benchmark = PerformanceBenchmark(
        puzzle_sizes=[2, 3],  # Test 2x2 and 3x3
        exploration_depths=[5, 8, 12]  # Different knowledge base depths
    )
    
    benchmark.run_full_benchmark()
    
    # Generate plots if matplotlib is available
    try:
        benchmark.plot_results()
    except Exception as e:
        print(f"Plotting skipped: {e}")


if __name__ == "__main__":
    main()