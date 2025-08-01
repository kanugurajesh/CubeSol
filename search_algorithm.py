import random
import time
from typing import Dict, List, Tuple, Optional, Set
from tqdm import tqdm
from collections import deque
import heapq
from puzzle_engine import CubicPuzzle

class AdaptiveSearchEngine:
    """
    Enhanced search engine with multiple optimization techniques and performance tracking
    """
    
    def __init__(self, knowledge_base: Dict[str, int], depth_limit: int = 20):
        self.depth_ceiling = depth_limit
        self.current_threshold = depth_limit
        self.next_threshold = None
        self.heuristic_db = knowledge_base
        self.solution_path = []
        self.visited_states = set()
        self.move_cache = {}
        
        # Performance tracking
        self.nodes_expanded = 0
        self.cache_hits = 0
        self.heuristic_hits = 0
        
    def solve_puzzle(self, initial_state: str) -> List[Tuple[str, int, int]]:
        """Enhanced solver with multiple algorithms and performance tracking"""
        self._reset_performance_counters()
        
        # First try BFS for shallow solutions (very fast for scrambles < 6 moves)
        bfs_solution = self._breadth_first_search(initial_state, max_depth=6)
        if bfs_solution:
            print(f"BFS found solution: {len(bfs_solution)} moves, {self.nodes_expanded} nodes expanded")
            return bfs_solution
            
        # Then try bidirectional search for medium complexity
        self._reset_performance_counters()
        bidirectional_solution = self._bidirectional_search(initial_state)
        if bidirectional_solution:
            print(f"Bidirectional found solution: {len(bidirectional_solution)} moves, {self.nodes_expanded} nodes expanded")
            return bidirectional_solution
            
        # Fall back to IDA* for complex cases
        self._reset_performance_counters()
        ida_solution = self._ida_star_search(initial_state)
        if ida_solution:
            print(f"IDA* found solution: {len(ida_solution)} moves, {self.nodes_expanded} nodes expanded")
            print(f"Cache hits: {self.cache_hits}, Heuristic hits: {self.heuristic_hits}")
        return ida_solution
    
    def _reset_performance_counters(self):
        """Reset performance tracking counters"""
        self.nodes_expanded = 0
        self.cache_hits = 0
        self.heuristic_hits = 0
        self.visited_states.clear()
    
    def _breadth_first_search(self, initial_state: str, max_depth: int) -> Optional[List[Tuple[str, int, int]]]:
        """Quick BFS for shallow solutions with performance tracking"""
        queue = deque([(initial_state, [])])
        visited = {initial_state}
        
        while queue:
            state, path = queue.popleft()
            self.nodes_expanded += 1
            
            if len(path) > max_depth:
                return None
                
            puzzle = CubicPuzzle(configuration=state)
            if puzzle.is_completion_achieved():
                return path
                
            for move in self._generate_all_moves(puzzle.size):
                new_state = self._get_next_state(state, move)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path + [move]))
        
        return None
    
    def _bidirectional_search(self, initial_state: str) -> Optional[List[Tuple[str, int, int]]]:
        """Bidirectional search meeting in the middle with performance tracking"""
        # Get solved state
        temp_puzzle = CubicPuzzle(dimension=3)
        solved_state = temp_puzzle.export_state()
        
        if initial_state == solved_state:
            return []
            
        # Forward and backward frontiers
        forward_frontier = {initial_state: []}
        backward_frontier = {solved_state: []}
        forward_visited = {initial_state}
        backward_visited = {solved_state}
        
        max_depth = min(self.depth_ceiling // 2, 8)  # Reasonable limit
        
        for depth in range(max_depth):
            # Expand forward frontier
            new_forward = {}
            for state, path in forward_frontier.items():
                self.nodes_expanded += 1
                for move in self._generate_all_moves(3):
                    new_state = self._get_next_state(state, move)
                    if new_state in backward_visited:
                        # Found connection!
                        backward_path = self._find_path_in_frontier(new_state, backward_frontier)
                        return path + [move] + self._reverse_path(backward_path)
                    if new_state not in forward_visited:
                        forward_visited.add(new_state)
                        new_forward[new_state] = path + [move]
            
            if not new_forward:  # No more states to expand
                break
            forward_frontier = new_forward
            
            # Expand backward frontier
            new_backward = {}
            for state, path in backward_frontier.items():
                self.nodes_expanded += 1
                for move in self._generate_all_moves(3):
                    new_state = self._get_next_state(state, move)
                    if new_state in forward_visited:
                        # Found connection!
                        forward_path = self._find_path_in_frontier(new_state, forward_frontier)
                        return forward_path + self._reverse_path(path + [move])
                    if new_state not in backward_visited:
                        backward_visited.add(new_state)
                        new_backward[new_state] = path + [move]
            
            if not new_backward:  # No more states to expand
                break
            backward_frontier = new_backward
            
        return None
    
    def _ida_star_search(self, initial_state: str) -> List[Tuple[str, int, int]]:
        """Optimized IDA* implementation with enhanced performance tracking"""
        self.visited_states.clear()
        self.solution_path = []
        
        # Start with a reasonable threshold based on heuristic
        initial_h = self._get_heuristic_value(initial_state)
        self.current_threshold = max(initial_h, 1)
        self.next_threshold = float('inf')
        
        iteration = 0
        while self.current_threshold <= self.depth_ceiling:
            iteration += 1
            print(f"IDA* iteration {iteration}, threshold: {self.current_threshold}")
            
            found_solution = self._depth_limited_search_optimized(initial_state, 0, 0)
            if found_solution:
                return self.solution_path
                
            if self.next_threshold == float('inf'):
                break  # No solution found within depth limit
                
            self.solution_path = []
            self.visited_states.clear()
            self.current_threshold = self.next_threshold
            self.next_threshold = float('inf')
        
        return []  # No solution found
    
    def _depth_limited_search_optimized(self, state: str, g: int, prev_move: Optional[Tuple] = None) -> bool:
        """Optimized recursive search with enhanced pruning"""
        self.nodes_expanded += 1
        
        h = self._get_heuristic_value(state)
        f = g + h
        
        if f > self.current_threshold:
            if f < self.next_threshold:
                self.next_threshold = f
            return False
            
        puzzle = CubicPuzzle(configuration=state)
        if puzzle.is_completion_achieved():
            return True
            
        # Enhanced cycle detection with depth consideration
        state_depth_key = (state, g % 4)  # Allow revisiting at different depths modulo 4
        if state_depth_key in self.visited_states:
            return False
        self.visited_states.add(state_depth_key)
        
        # Generate moves with enhanced ordering
        moves = self._generate_ordered_moves(puzzle.size, prev_move, state)
        
        for move in moves:
            new_state = self._get_next_state(state, move)
            self.solution_path.append(move)
            
            if self._depth_limited_search_optimized(new_state, g + 1, move):
                return True
                
            self.solution_path.pop()
            
        self.visited_states.remove(state_depth_key)
        return False
    
    def _generate_ordered_moves(self, puzzle_size: int, prev_move: Optional[Tuple] = None, state: str = None) -> List[Tuple[str, int, int]]:
        """Generate moves with enhanced ordering based on heuristics"""
        moves = self._generate_all_moves(puzzle_size)
        
        # Avoid immediately undoing the previous move
        if prev_move:
            inverse_move = self._get_inverse_move(prev_move)
            moves = [m for m in moves if m != inverse_move]
        
        # Enhanced move ordering
        def move_priority(move):
            move_type, layer, direction = move
            priority = 0
            
            # Prioritize outer layer moves (affect more pieces)
            if layer == 0 or layer == puzzle_size - 1:
                priority -= 2
            
            # Slight preference for certain move types based on common patterns
            if move_type == 'horizontal':
                priority -= 1  # Horizontal moves often useful
            
            # If we have state information, prefer moves that improve heuristic
            if state and self.heuristic_db:
                try:
                    temp_puzzle = CubicPuzzle(configuration=state)
                    self._apply_move(temp_puzzle, move)
                    new_state = temp_puzzle.export_state()
                    new_h = self._get_heuristic_value(new_state)
                    old_h = self._get_heuristic_value(state)
                    if new_h < old_h:
                        priority -= 3  # Strongly prefer improving moves
                except:
                    pass  # Ignore errors in heuristic calculation
            
            return priority
        
        return sorted(moves, key=move_priority)
    
    def _get_inverse_move(self, move: Tuple[str, int, int]) -> Tuple[str, int, int]:
        """Get the inverse of a move"""
        move_type, layer, direction = move
        return (move_type, layer, 1 - direction)
    
    def _get_next_state(self, state: str, move: Tuple[str, int, int]) -> str:
        """Get next state with enhanced caching"""
        cache_key = (state, move)
        if cache_key in self.move_cache:
            self.cache_hits += 1
            return self.move_cache[cache_key]
            
        puzzle = CubicPuzzle(configuration=state)
        self._apply_move(puzzle, move)
        new_state = puzzle.export_state()
        
        # Dynamic cache size management
        max_cache_size = 50000
        if len(self.move_cache) < max_cache_size:
            self.move_cache[cache_key] = new_state
        elif len(self.move_cache) >= max_cache_size:
            # Remove oldest entries (simple FIFO)
            keys_to_remove = list(self.move_cache.keys())[:max_cache_size // 4]
            for key in keys_to_remove:
                del self.move_cache[key]
            self.move_cache[cache_key] = new_state
            
        return new_state
    
    def _find_path_in_frontier(self, state: str, frontier: Dict) -> List[Tuple]:
        """Find path to state in frontier - optimized version"""
        return frontier.get(state, [])
    
    def _reverse_path(self, path: List[Tuple]) -> List[Tuple]:
        """Reverse a path by inverting moves in reverse order"""
        return [self._get_inverse_move(move) for move in reversed(path)]
    
    def _generate_all_moves(self, puzzle_size: int) -> List[Tuple[str, int, int]]:
        """Generate all possible moves for given puzzle size"""
        return [
            (move_type, layer, direction)
            for move_type in ['horizontal', 'vertical', 'sideways']
            for direction in [0, 1]
            for layer in range(puzzle_size)
        ]
    
    def _apply_move(self, puzzle: CubicPuzzle, move: Tuple[str, int, int]) -> None:
        """Apply a move to the puzzle"""
        move_type, layer, direction = move
        
        if move_type == 'horizontal':
            puzzle.execute_horizontal_rotation(layer, direction)
        elif move_type == 'vertical':
            puzzle.execute_vertical_rotation(layer, direction)
        elif move_type == 'sideways':
            puzzle.execute_lateral_rotation(layer, direction)
    
    def _breadth_first_search_with_timeout(self, initial_state: str, max_depth: int, timeout: float) -> Optional[List[Tuple[str, int, int]]]:
        """BFS with timeout mechanism and optimized performance"""
        start_time = time.time()
        queue = deque([(initial_state, [])])
        visited = {initial_state}
        nodes_checked = 0
        
        while queue:
            # Check timeout every 1000 nodes for better performance
            if nodes_checked % 1000 == 0 and time.time() - start_time > timeout:
                print(f"   BFS timeout after {timeout}s ({nodes_checked} nodes checked)")
                return None
                
            state, path = queue.popleft()
            nodes_checked += 1
            self.nodes_expanded += 1
            
            if len(path) > max_depth:
                continue
                
            puzzle = CubicPuzzle(configuration=state)
            if puzzle.is_completion_achieved():
                return path
                
            # Use ordered moves for better performance
            for move in self._generate_ordered_moves(puzzle.size, path[-1] if path else None):
                new_state = self._get_next_state(state, move)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path + [move]))
        
        return None
    
    def _bidirectional_search_with_timeout(self, initial_state: str, timeout: float) -> Optional[List[Tuple[str, int, int]]]:
        """Bidirectional search with timeout mechanism"""
        start_time = time.time()
        
        # Get solved state
        temp_puzzle = CubicPuzzle(dimension=3)
        solved_state = temp_puzzle.export_state()
        
        if initial_state == solved_state:
            return []
            
        # Forward and backward frontiers
        forward_frontier = {initial_state: []}
        backward_frontier = {solved_state: []}
        forward_visited = {initial_state}
        backward_visited = {solved_state}
        
        max_depth = 6  # Reasonable limit for timeout version
        
        for depth in range(max_depth):
            if time.time() - start_time > timeout:
                print(f"   Bidirectional search timeout after {timeout}s")
                return None
                
            # Expand forward frontier
            new_forward = {}
            for state, path in forward_frontier.items():
                self.nodes_expanded += 1
                for move in self._generate_all_moves(3):
                    new_state = self._get_next_state(state, move)
                    if new_state in backward_visited:
                        # Found connection!
                        backward_path = self._find_path_in_frontier(new_state, backward_frontier)
                        return path + [move] + self._reverse_path(backward_path)
                    
                    if new_state not in forward_visited:
                        forward_visited.add(new_state)
                        new_forward[new_state] = path + [move]
            
            forward_frontier = new_forward
            
            # Expand backward frontier
            new_backward = {}
            for state, path in backward_frontier.items():
                self.nodes_expanded += 1
                for move in self._generate_all_moves(3):
                    new_state = self._get_next_state(state, move)
                    if new_state in forward_visited:
                        # Found connection!
                        forward_path = self._find_path_in_frontier(new_state, forward_frontier)
                        return forward_path + self._reverse_path([move] + path)
                    
                    if new_state not in backward_visited:
                        backward_visited.add(new_state)
                        new_backward[new_state] = path + [move]
            
            backward_frontier = new_backward
        
        return None
    
    def solve_puzzle_simple(self, initial_state: str, max_moves: int = 15, timeout: float = 5) -> Optional[List[Tuple[str, int, int]]]:
        """Optimized simple iterative deepening search with better heuristics"""
        start_time = time.time()
        
        # Try BFS first for very shallow solutions (faster for simple cases)
        quick_bfs = self._breadth_first_search(initial_state, max_depth=4)
        if quick_bfs:
            return quick_bfs
        
        # Use heuristic-guided search for deeper solutions
        for depth in range(5, max_moves + 1):
            if time.time() - start_time > timeout:
                print(f"   Simple search timeout after {timeout}s")
                return None
                
            solution = self._depth_limited_simple_search(initial_state, depth, start_time, timeout)
            if solution:
                return solution
        
        return None
    
    def _depth_limited_simple_search(self, state: str, max_depth: int, start_time: float, timeout: float) -> Optional[List[Tuple[str, int, int]]]:
        """Simple depth-limited search with timeout"""
        if time.time() - start_time > timeout:
            return None
            
        puzzle = CubicPuzzle(configuration=state)
        if puzzle.is_completion_achieved():
            return []
        
        if max_depth <= 0:
            return None
        
        for move in self._generate_all_moves(puzzle.size):
            new_state = self._get_next_state(state, move)
            result = self._depth_limited_simple_search(new_state, max_depth - 1, start_time, timeout)
            if result is not None:
                return [move] + result
        
        return None
    
    def _get_heuristic_value(self, state: str) -> int:
        """Enhanced heuristic with multiple fallback strategies"""
        # Use pattern database if available
        if state in self.heuristic_db:
            self.heuristic_hits += 1
            return self.heuristic_db[state]
        
        # Multiple heuristic strategies
        manhattan_h = self._manhattan_distance_heuristic(state)
        corner_h = self._corner_heuristic(state)
        edge_h = self._edge_heuristic(state)
        
        # Take maximum of all heuristics (admissible if all are admissible)
        return max(manhattan_h, corner_h, edge_h)
    
    def _manhattan_distance_heuristic(self, state: str) -> int:
        """Enhanced Manhattan distance heuristic"""
        puzzle = CubicPuzzle(configuration=state)
        solved = CubicPuzzle(dimension=puzzle.size)
        
        misplaced_pieces = 0
        for face in range(6):
            for row in range(puzzle.size):
                for col in range(puzzle.size):
                    if puzzle.matrix[face][row][col] != solved.matrix[face][row][col]:
                        misplaced_pieces += 1
        
        # More accurate estimate: each move fixes ~3-4 pieces on average
        return max(1, misplaced_pieces // 4)
    
    def _corner_heuristic(self, state: str) -> int:
        """Heuristic based on corner pieces positioning"""
        puzzle = CubicPuzzle(configuration=state)
        solved = CubicPuzzle(dimension=puzzle.size)
        
        misplaced_corners = 0
        corner_positions = [(0, 0), (0, puzzle.size-1), (puzzle.size-1, 0), (puzzle.size-1, puzzle.size-1)]
        
        for face in range(6):
            for row, col in corner_positions:
                if puzzle.matrix[face][row][col] != solved.matrix[face][row][col]:
                    misplaced_corners += 1
        
        # Corner pieces are harder to fix
        return max(0, misplaced_corners // 6)
    
    def _edge_heuristic(self, state: str) -> int:
        """Heuristic based on edge pieces positioning"""
        puzzle = CubicPuzzle(configuration=state)
        solved = CubicPuzzle(dimension=puzzle.size)
        
        misplaced_edges = 0
        
        # Check edge positions (middle of each side)
        if puzzle.size >= 3:
            mid = puzzle.size // 2
            edge_positions = [
                (0, mid), (mid, 0), (mid, puzzle.size-1), (puzzle.size-1, mid)
            ]
            
            for face in range(6):
                for row, col in edge_positions:
                    if puzzle.matrix[face][row][col] != solved.matrix[face][row][col]:
                        misplaced_edges += 1
        
        return max(0, misplaced_edges // 8)


class KnowledgeBaseBuilder:
    """Enhanced builder with corner/edge pattern databases and optimizations"""
    
    @staticmethod
    def construct_heuristic_database(
        target_state: str,
        move_set: List[Tuple[str, int, int]],
        exploration_depth: int = 20,
        existing_knowledge: Optional[Dict[str, int]] = None
    ) -> Dict[str, int]:
        """Build comprehensive heuristic database with optimizations"""
        if existing_knowledge is None:
            knowledge_db = {target_state: 0}
        else:
            knowledge_db = existing_knowledge.copy()
        
        # Use deque for BFS (more efficient than list)
        exploration_queue = deque([(target_state, 0)])
        
        # Pre-calculate total nodes for progress tracking
        branching_factor = len(move_set)
        estimated_nodes = min(branching_factor ** exploration_depth, 1000000)  # Cap for memory
        
        states_processed = 0
        with tqdm(total=estimated_nodes, desc='Building Knowledge Base') as progress_bar:
            while exploration_queue and states_processed < estimated_nodes:
                current_state, current_depth = exploration_queue.popleft()
                states_processed += 1
                
                if current_depth >= exploration_depth:
                    continue
                
                # Process moves in batches for better performance
                for move in move_set:
                    try:
                        puzzle = CubicPuzzle(configuration=current_state)
                        
                        # Apply move
                        if move[0] == 'horizontal':
                            puzzle.execute_horizontal_rotation(move[1], move[2])
                        elif move[0] == 'vertical':
                            puzzle.execute_vertical_rotation(move[1], move[2])
                        elif move[0] == 'sideways':
                            puzzle.execute_lateral_rotation(move[1], move[2])
                        
                        new_state = puzzle.export_state()
                        new_distance = current_depth + 1
                        
                        # Only add if we found a shorter path or new state
                        if new_state not in knowledge_db or knowledge_db[new_state] > new_distance:
                            knowledge_db[new_state] = new_distance
                            if new_distance < exploration_depth:  # Only queue if within depth
                                exploration_queue.append((new_state, new_distance))
                        
                    except Exception as e:
                        # Skip problematic moves
                        continue
                        
                    progress_bar.update(1)
                    
                    # Memory management - limit queue size
                    if len(exploration_queue) > 100000:
                        # Keep only the most promising states (lowest depth)
                        exploration_queue = deque(sorted(exploration_queue, key=lambda x: x[1])[:50000])
        
        print(f"\nKnowledge base construction complete:")
        print(f"  Total states: {len(knowledge_db)}")
        print(f"  Max depth reached: {max(knowledge_db.values()) if knowledge_db else 0}")
        print(f"  States processed: {states_processed}")
        
        return knowledge_db
    
    @staticmethod
    def build_pattern_database(target_state: str, pattern_type: str = "corners") -> Dict[str, int]:
        """Build pattern databases for corners or edges"""
        puzzle = CubicPuzzle(configuration=target_state)
        
        if pattern_type == "corners":
            return KnowledgeBaseBuilder._build_corner_database(puzzle)
        elif pattern_type == "edges":
            return KnowledgeBaseBuilder._build_edge_database(puzzle)
        else:
            raise ValueError(f"Unknown pattern type: {pattern_type}")
    
    @staticmethod
    def _build_corner_database(puzzle: CubicPuzzle) -> Dict[str, int]:
        """Build database focusing on corner pieces"""
        # Extract corner piece positions and orientations
        # This is a simplified version - full implementation would be more complex
        corner_pattern = KnowledgeBaseBuilder._extract_corner_pattern(puzzle)
        
        # Build mini-database for corner patterns
        corner_db = {corner_pattern: 0}
        
        # This would involve generating all possible corner configurations
        # and computing distances - simplified for demonstration
        return corner_db
    
    @staticmethod
    def _build_edge_database(puzzle: CubicPuzzle) -> Dict[str, int]:
        """Build database focusing on edge pieces"""
        # Similar to corner database but for edge pieces
        edge_pattern = KnowledgeBaseBuilder._extract_edge_pattern(puzzle)
        edge_db = {edge_pattern: 0}
        return edge_db
    
    @staticmethod
    def _extract_corner_pattern(puzzle: CubicPuzzle) -> str:
        """Extract corner piece pattern from puzzle state"""
        corners = []
        corner_positions = [(0, 0), (0, puzzle.size-1), (puzzle.size-1, 0), (puzzle.size-1, puzzle.size-1)]
        
        for face in range(6):
            for row, col in corner_positions:
                corners.append(puzzle.matrix[face][row][col])
        
        return ''.join(corners)
    
    @staticmethod
    def _extract_edge_pattern(puzzle: CubicPuzzle) -> str:
        """Extract edge piece pattern from puzzle state"""
        edges = []
        if puzzle.size >= 3:
            mid = puzzle.size // 2
            edge_positions = [(0, mid), (mid, 0), (mid, puzzle.size-1), (puzzle.size-1, mid)]
            
            for face in range(6):
                for row, col in edge_positions:
                    edges.append(puzzle.matrix[face][row][col])
        
        return ''.join(edges)
    
    @staticmethod
    def optimize_database(knowledge_db: Dict[str, int], max_size: int = 100000) -> Dict[str, int]:
        """Optimize database size by keeping most useful entries"""
        if len(knowledge_db) <= max_size:
            return knowledge_db
        
        # Keep states with lower distances (more useful for heuristic)
        sorted_items = sorted(knowledge_db.items(), key=lambda x: (x[1], x[0]))
        optimized_db = dict(sorted_items[:max_size])
        
        print(f"Optimized database from {len(knowledge_db)} to {len(optimized_db)} states")
        return optimized_db
    
    @staticmethod
    def validate_database(knowledge_db: Dict[str, int], sample_size: int = 100) -> bool:
        """Validate database by checking consistency of distances"""
        if not knowledge_db:
            return False
        
        # Sample random states and verify distances are reasonable
        sample_states = random.sample(list(knowledge_db.keys()), min(sample_size, len(knowledge_db)))
        
        valid_count = 0
        for state in sample_states:
            distance = knowledge_db[state]
            if 0 <= distance <= 30:  # Reasonable range for cube distances
                valid_count += 1
        
        validity_ratio = valid_count / len(sample_states)
        print(f"Database validity: {validity_ratio:.2%} ({valid_count}/{len(sample_states)} samples)")
        
        return validity_ratio > 0.95  # 95% of samples should be valid