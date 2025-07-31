import random
from typing import List, Optional, Tuple

class CubicPuzzle:
    """
    Advanced 3D puzzle manipulation engine for multi-dimensional cubic structures
    """
    
    def __init__(self, dimension: int = 3, palette: List[str] = None, configuration: str = None):
        """
        Initialize the cubic puzzle engine
        
        Args:
            dimension: Size of the cubic puzzle (default: 3x3x3)
            palette: Color scheme for puzzle faces 
            configuration: Serialized puzzle state for reconstruction
        """
        self.face_colors = palette or ['W', 'O', 'G', 'R', 'B', 'Y']
        
        if configuration:
            self._deserialize_state(configuration)
        else:
            self.size = dimension
            self._initialize_solved_state()
    
    def _deserialize_state(self, state_string: str) -> None:
        """Reconstruct puzzle from serialized state"""
        total_squares = len(state_string)
        self.size = int((total_squares / 6) ** 0.5)
        
        discovered_colors = []
        self.matrix = [[[]]]
        
        for idx, color_char in enumerate(state_string):
            if color_char not in discovered_colors:
                discovered_colors.append(color_char)
            
            self.matrix[-1][-1].append(color_char)
            
            # Handle matrix structure building
            current_row_full = len(self.matrix[-1][-1]) == self.size
            current_face_incomplete = len(self.matrix[-1]) < self.size
            more_data_remaining = idx < total_squares - 1
            
            if current_row_full and current_face_incomplete:
                self.matrix[-1].append([])
            elif current_row_full and not current_face_incomplete and more_data_remaining:
                self.matrix.append([[]])
        
        self.face_colors = discovered_colors
    
    def _initialize_solved_state(self) -> None:
        """Create a pristine solved puzzle configuration"""
        self.matrix = [
            [[color] * self.size for _ in range(self.size)] 
            for color in self.face_colors
        ]
    
    def restore_factory_settings(self) -> None:
        """Reset puzzle to original solved configuration"""
        self._initialize_solved_state()
    
    def is_completion_achieved(self) -> bool:
        """
        Verify if puzzle has reached solved state
        Returns True if all faces are monochromatic
        """
        for face_grid in self.matrix:
            face_colors = []
            uniform_rows = True
            
            for row in face_grid:
                if len(set(row)) == 1:
                    face_colors.append(row[0])
                else:
                    uniform_rows = False
                    break
            
            if not uniform_rows:
                return False
            
            if len(set(face_colors)) != 1:
                return False
        
        return True
    
    def export_state(self) -> str:
        """Generate serialized representation of current puzzle state"""
        return ''.join(
            color for face in self.matrix 
            for row in face for color in row
        )
    
    def randomize_configuration(self, min_operations: int = 5, max_operations: int = 100) -> None:
        """
        Apply random valid transformations to create solvable scrambled state
        
        Args:
            min_operations: Minimum number of random moves
            max_operations: Maximum number of random moves
        """
        operation_count = random.randint(min_operations, max_operations)
        
        available_transforms = [
            ('horizontal', 0), ('horizontal', 1),
            ('vertical', 0), ('vertical', 1),
            ('sideways', 0), ('sideways', 1)
        ]
        
        for _ in range(operation_count):
            transform_type, rotation_dir = random.choice(available_transforms)
            layer_index = random.randint(0, self.size - 1)
            
            if transform_type == 'horizontal':
                self.execute_horizontal_rotation(layer_index, rotation_dir)
            elif transform_type == 'vertical':
                self.execute_vertical_rotation(layer_index, rotation_dir)
            elif transform_type == 'sideways':
                self.execute_lateral_rotation(layer_index, rotation_dir)
    
    def display_configuration(self) -> None:
        """Render visual representation of current puzzle state"""
        indent = ' ' * (len(str(self.matrix[0][0])) + 2)
        
        # Top face
        top_display = '\n'.join(indent + str(row) for row in self.matrix[0])
        
        # Middle band (4 side faces)
        middle_display = '\n'.join(
            '  '.join(str(self.matrix[face_idx][row_idx]) for face_idx in range(1, 5))
            for row_idx in range(len(self.matrix[0]))
        )
        
        # Bottom face  
        bottom_display = '\n'.join(indent + str(row) for row in self.matrix[5])
        
        print(f'{top_display}\n\n{middle_display}\n\n{bottom_display}')
    
    def execute_horizontal_rotation(self, layer: int, clockwise: int) -> None:
        """
        Perform horizontal layer rotation
        
        Args:
            layer: Layer index to rotate
            clockwise: 0 for counter-clockwise, 1 for clockwise
        """
        if layer >= len(self.matrix[0]):
            print(f'ERROR: Layer {layer} exceeds puzzle bounds [0-{len(self.matrix[0])-1}]')
            return
        
        if clockwise not in [0, 1]:
            print('ERROR: Direction must be 0 (counter-clockwise) or 1 (clockwise)')
            return
        
        # Rotate middle band faces
        if clockwise == 0:  # Counter-clockwise
            (self.matrix[1][layer], self.matrix[2][layer], 
             self.matrix[3][layer], self.matrix[4][layer]) = (
                self.matrix[2][layer], self.matrix[3][layer],
                self.matrix[4][layer], self.matrix[1][layer]
            )
        else:  # Clockwise
            (self.matrix[1][layer], self.matrix[2][layer], 
             self.matrix[3][layer], self.matrix[4][layer]) = (
                self.matrix[4][layer], self.matrix[1][layer],
                self.matrix[2][layer], self.matrix[3][layer]
            )
        
        # Handle connected face rotations
        self._rotate_connected_face_horizontal(layer, clockwise)
    
    def _rotate_connected_face_horizontal(self, layer: int, clockwise: int) -> None:
        """Rotate faces connected to horizontal layer movement"""
        if layer == 0:  # Top layer
            if clockwise == 0:
                self.matrix[0] = [list(row) for row in zip(*reversed(self.matrix[0]))]
            else:
                self.matrix[0] = [list(row) for row in zip(*self.matrix[0])][::-1]
        elif layer == len(self.matrix[0]) - 1:  # Bottom layer
            if clockwise == 0:
                self.matrix[5] = [list(row) for row in zip(*reversed(self.matrix[5]))]
            else:
                self.matrix[5] = [list(row) for row in zip(*self.matrix[5])][::-1]
    
    def execute_vertical_rotation(self, column: int, upward: int) -> None:
        """
        Perform vertical column rotation
        
        Args:
            column: Column index to rotate
            upward: 0 for downward, 1 for upward
        """
        if column >= len(self.matrix[0]):
            print(f'ERROR: Column {column} exceeds puzzle bounds [0-{len(self.matrix[0])-1}]')
            return
        
        if upward not in [0, 1]:
            print('ERROR: Direction must be 0 (downward) or 1 (upward)')
            return
        
        # Rotate vertical column through faces
        for row_idx in range(len(self.matrix[0])):
            if upward == 0:  # Downward
                (self.matrix[0][row_idx][column], self.matrix[2][row_idx][column],
                 self.matrix[4][-row_idx-1][-column-1], self.matrix[5][row_idx][column]) = (
                    self.matrix[4][-row_idx-1][-column-1], self.matrix[0][row_idx][column],
                    self.matrix[5][row_idx][column], self.matrix[2][row_idx][column]
                )
            else:  # Upward
                (self.matrix[0][row_idx][column], self.matrix[2][row_idx][column],
                 self.matrix[4][-row_idx-1][-column-1], self.matrix[5][row_idx][column]) = (
                    self.matrix[2][row_idx][column], self.matrix[5][row_idx][column],
                    self.matrix[0][row_idx][column], self.matrix[4][-row_idx-1][-column-1]
                )
        
        # Handle connected face rotations
        self._rotate_connected_face_vertical(column, upward)
    
    def _rotate_connected_face_vertical(self, column: int, upward: int) -> None:
        """Rotate faces connected to vertical column movement"""
        if column == 0:  # Left column
            if upward == 0:
                self.matrix[1] = [list(row) for row in zip(*self.matrix[1])][::-1]
            else:
                self.matrix[1] = [list(row) for row in zip(*reversed(self.matrix[1]))]
        elif column == len(self.matrix[0]) - 1:  # Right column
            if upward == 0:
                self.matrix[3] = [list(row) for row in zip(*self.matrix[3])][::-1]
            else:
                self.matrix[3] = [list(row) for row in zip(*reversed(self.matrix[3]))]
    
    def execute_lateral_rotation(self, slice_idx: int, direction: int) -> None:
        """
        Perform lateral (side-to-side) slice rotation
        
        Args:
            slice_idx: Slice index to rotate
            direction: 0 for one direction, 1 for opposite
        """
        if slice_idx >= len(self.matrix[0]):
            print(f'ERROR: Slice {slice_idx} exceeds puzzle bounds [0-{len(self.matrix[0])-1}]')
            return
        
        if direction not in [0, 1]:
            print('ERROR: Direction must be 0 or 1')
            return
        
        # Rotate lateral slice through faces
        for pos in range(len(self.matrix[0])):
            if direction == 0:
                (self.matrix[0][slice_idx][pos], self.matrix[1][-pos-1][slice_idx],
                 self.matrix[3][pos][-slice_idx-1], self.matrix[5][-slice_idx-1][-pos-1]) = (
                    self.matrix[3][pos][-slice_idx-1], self.matrix[0][slice_idx][pos],
                    self.matrix[5][-slice_idx-1][-pos-1], self.matrix[1][-pos-1][slice_idx]
                )
            else:
                (self.matrix[0][slice_idx][pos], self.matrix[1][-pos-1][slice_idx],
                 self.matrix[3][pos][-slice_idx-1], self.matrix[5][-slice_idx-1][-pos-1]) = (
                    self.matrix[1][-pos-1][slice_idx], self.matrix[5][-slice_idx-1][-pos-1],
                    self.matrix[0][slice_idx][pos], self.matrix[3][pos][-slice_idx-1]
                )
        
        # Handle connected face rotations
        self._rotate_connected_face_lateral(slice_idx, direction)
    
    def _rotate_connected_face_lateral(self, slice_idx: int, direction: int) -> None:
        """Rotate faces connected to lateral slice movement"""
        if slice_idx == 0:  # Front slice
            if direction == 0:
                self.matrix[4] = [list(row) for row in zip(*reversed(self.matrix[4]))]
            else:
                self.matrix[4] = [list(row) for row in zip(*self.matrix[4])][::-1]
        elif slice_idx == len(self.matrix[0]) - 1:  # Back slice
            if direction == 0:
                self.matrix[2] = [list(row) for row in zip(*reversed(self.matrix[2]))]
            else:
                self.matrix[2] = [list(row) for row in zip(*self.matrix[2])][::-1]