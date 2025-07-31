import random
from typing import Dict, List, Tuple, Optional
from tqdm import tqdm
from puzzle_engine import CubicPuzzle

class AdaptiveSearchEngine:
    """
    Intelligent search engine using iterative deepening with adaptive heuristics
    """
    
    def __init__(self, knowledge_base: Dict[str, int], depth_limit: int = 20):
        """
        Initialize the search engine
        
        Args:
            knowledge_base: Precomputed heuristic lookup table
            depth_limit: Maximum search depth allowed
        """
        self.depth_ceiling = depth_limit
        self.current_threshold = depth_limit
        self.next_threshold = None
        self.heuristic_db = knowledge_base
        self.solution_path = []
    
    def solve_puzzle(self, initial_state: str) -> List[Tuple[str, int, int]]:
        """
        Find optimal solution for given puzzle state
        
        Args:
            initial_state: Serialized puzzle configuration
            
        Returns:
            List of moves to solve the puzzle
        """
        while True:
            found_solution = self._depth_limited_search(initial_state, 1)
            if found_solution:
                return self.solution_path
            
            self.solution_path = []
            self.current_threshold = self.next_threshold
        
        return []
    
    def _depth_limited_search(self, state: str, cost_so_far: int) -> bool:
        """
        Recursive depth-limited search with heuristic guidance
        
        Args:
            state: Current puzzle state
            cost_so_far: Cost to reach current state
            
        Returns:
            True if solution found, False otherwise
        """
        puzzle = CubicPuzzle(configuration=state)
        
        # Base cases
        if puzzle.is_completion_achieved():
            return True
        
        if len(self.solution_path) >= self.current_threshold:
            return False
        
        # Generate and evaluate all possible moves
        optimal_cost = float('inf')
        candidate_moves = None
        
        all_moves = self._generate_all_moves(puzzle.size)
        
        for move in all_moves:
            test_puzzle = CubicPuzzle(configuration=state)
            self._apply_move(test_puzzle, move)
            
            if test_puzzle.is_completion_achieved():
                self.solution_path.append(move)
                return True
            
            new_state = test_puzzle.export_state()
            heuristic_cost = self._get_heuristic_value(new_state)
            total_cost = cost_so_far + heuristic_cost
            
            if total_cost < optimal_cost:
                optimal_cost = total_cost
                candidate_moves = [(new_state, move)]
            elif total_cost == optimal_cost:
                if candidate_moves is None:
                    candidate_moves = [(new_state, move)]
                else:
                    candidate_moves.append((new_state, move))
        
        # Explore best candidate(s)
        if candidate_moves is not None:
            if self.next_threshold is None or optimal_cost < self.next_threshold:
                self.next_threshold = optimal_cost
            
            selected_move = random.choice(candidate_moves)
            self.solution_path.append(selected_move[1])
            
            if self._depth_limited_search(selected_move[0], cost_so_far + optimal_cost):
                return True
        
        return False
    
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
    
    def _get_heuristic_value(self, state: str) -> int:
        """Get heuristic value for given state"""
        return self.heuristic_db.get(state, self.depth_ceiling)


class KnowledgeBaseBuilder:
    """
    Builder for creating heuristic knowledge base through exhaustive exploration
    """
    
    @staticmethod
    def construct_heuristic_database(
        target_state: str,
        move_set: List[Tuple[str, int, int]],
        exploration_depth: int = 20,
        existing_knowledge: Optional[Dict[str, int]] = None
    ) -> Dict[str, int]:
        """
        Build comprehensive heuristic database through breadth-first exploration
        
        Args:
            target_state: Goal state (usually solved puzzle)
            move_set: All possible moves
            exploration_depth: Maximum depth to explore
            existing_knowledge: Previous knowledge base to extend
            
        Returns:
            Dictionary mapping states to minimum distance from goal
        """
        if existing_knowledge is None:
            knowledge_db = {target_state: 0}
        else:
            knowledge_db = existing_knowledge.copy()
        
        exploration_queue = [(target_state, 0)]
        
        # Calculate total nodes for progress tracking
        total_nodes = sum(len(move_set) ** (depth + 1) for depth in range(exploration_depth + 1))
        
        with tqdm(total=total_nodes, desc='Building Knowledge Base') as progress_bar:
            while exploration_queue:
                current_state, current_depth = exploration_queue.pop(0)
                
                if current_depth > exploration_depth:
                    continue
                
                for move in move_set:
                    puzzle = CubicPuzzle(configuration=current_state)
                    
                    if move[0] == 'horizontal':
                        puzzle.execute_horizontal_rotation(move[1], move[2])
                    elif move[0] == 'vertical':
                        puzzle.execute_vertical_rotation(move[1], move[2])
                    elif move[0] == 'sideways':
                        puzzle.execute_lateral_rotation(move[1], move[2])
                    
                    new_state = puzzle.export_state()
                    new_distance = current_depth + 1
                    
                    if new_state not in knowledge_db or knowledge_db[new_state] > new_distance:
                        knowledge_db[new_state] = new_distance
                    
                    exploration_queue.append((new_state, new_distance))
                    progress_bar.update(1)
        
        return knowledge_db