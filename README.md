# Advanced Cubic Puzzle Solver

## Overview
An intelligent 3D puzzle solving system that employs adaptive search algorithms and machine learning techniques to find optimal solutions for cubic puzzles. The system features a sophisticated heuristic knowledge base and iterative deepening search capabilities.

## Architecture

### Core Components

**Puzzle Engine (`puzzle_engine.py`)**
- Advanced cubic puzzle manipulation framework
- Support for n×n×n puzzle configurations  
- Comprehensive transformation operations
- State serialization and reconstruction capabilities

**Search Algorithm (`search_algorithm.py`)**
- Adaptive search engine with iterative deepening
- Intelligent heuristic guidance system
- Knowledge base construction and management
- Optimal solution path finding

**Puzzle Runner (`puzzle_runner.py`)**
- Main execution pipeline and orchestration
- Interactive puzzle manipulation mode
- Knowledge base persistence and loading
- Configuration management system

## Features

### Intelligent Solving
- **Adaptive Search**: Uses iterative deepening A* algorithm for optimal solutions
- **Heuristic Guidance**: Precomputed knowledge base for intelligent move selection
- **Memory Efficient**: Linear space complexity with maximum performance

### Flexible Configuration
- **Custom Puzzle Sizes**: Support for any n×n×n cubic puzzle
- **Color Schemes**: Configurable palette for puzzle faces
- **State Import/Export**: Load specific puzzle configurations

### Interactive Operations
- **Manual Control**: Interactive mode for hands-on puzzle manipulation
- **Visual Display**: Clear console-based puzzle visualization
- **Real-time Feedback**: Instant validation and state checking

## Quick Start

### Basic Usage
```bash
python puzzle_runner.py
```

### Interactive Mode
```bash
python puzzle_runner.py --interactive
```

### Custom Configuration
```python
from puzzle_engine import CubicPuzzle

# Create custom puzzle
puzzle = CubicPuzzle(
    dimension=4,  # 4x4x4 puzzle
    palette=['R', 'G', 'B', 'Y', 'O', 'W']
)

# Load specific state
puzzle = CubicPuzzle(
    configuration="RRRGGGBBBYYOWWWRRRGGBBYYWWWOOORRRGGGBBBYYYWWWOOORRR"
)
```

## Configuration Parameters

```python
# System Configuration
EXPLORATION_DEPTH = 3     # Knowledge base depth (higher = better solving)
REBUILD_KNOWLEDGE = True  # Force knowledge base reconstruction  
DATABASE_FILE = 'knowledge_base.json'  # Knowledge persistence file
```

### Performance Tuning

| Depth Level | States Explored | Memory Usage | Solving Speed |
|-------------|-----------------|--------------|---------------|
| 3           | ~3,000         | Low          | Fast          |
| 5           | ~100,000       | Medium       | Optimal       |
| 7           | ~1,000,000+    | High         | Maximum       |

## Advanced Features

### Knowledge Base System
The system builds and maintains a comprehensive knowledge base mapping puzzle states to optimal solution distances:

```python
from search_algorithm import KnowledgeBaseBuilder

# Build custom knowledge base
knowledge_db = KnowledgeBaseBuilder.construct_heuristic_database(
    target_state=solved_state,
    move_set=all_possible_moves,
    exploration_depth=5
)
```

### Search Engine Customization
```python
from search_algorithm import AdaptiveSearchEngine

# Configure search parameters
search_engine = AdaptiveSearchEngine(
    knowledge_base=heuristic_db,
    depth_limit=25  # Maximum search depth
)

solution = search_engine.solve_puzzle(scrambled_state)
```

## Interactive Commands

When running in interactive mode:

| Command | Description | Example |
|---------|-------------|---------|
| `h <layer> <dir>` | Horizontal rotation | `h 0 1` |
| `v <layer> <dir>` | Vertical rotation | `v 1 0` |
| `s <layer> <dir>` | Sideways rotation | `s 2 1` |
| `show` | Display current state | `show` |
| `reset` | Reset to solved state | `reset` |
| `scramble` | Randomize puzzle | `scramble` |
| `quit` | Exit interactive mode | `quit` |

**Direction Values**: 0 = counter-clockwise/down, 1 = clockwise/up

## Implementation Details

### State Representation
The puzzle uses a 6-face matrix structure where each face is represented as an n×n grid:
- **Face 0**: Top
- **Face 1**: Left  
- **Face 2**: Front
- **Face 3**: Right
- **Face 4**: Back
- **Face 5**: Bottom

### Movement Operations
Three primary transformation types:
1. **Horizontal Rotations**: Rotate horizontal slices affecting 4 side faces
2. **Vertical Rotations**: Rotate vertical columns through top/front/bottom/back
3. **Lateral Rotations**: Rotate side-to-side slices through all 6 faces

### Search Algorithm
The system employs **Iterative Deepening A*** with these key features:
- **Admissible Heuristics**: Never overestimate distance to solution
- **Optimal Solutions**: Guaranteed shortest move sequences
- **Memory Efficiency**: O(bd) space complexity vs O(b^d) for standard A*
- **Progressive Deepening**: Gradually increases search depth until solution found

### Heuristic Construction
Knowledge base built through **backward breadth-first search**:
1. Start from solved state (distance 0)
2. Apply all possible moves to generate new states
3. Record minimum distance for each discovered state
4. Continue until maximum depth reached
5. Results in lookup table: `state → minimum_moves_to_solve`

## Performance Optimization

### Memory Management
- **State Caching**: Efficient string-based state representation
- **Incremental Updates**: Extend existing knowledge bases rather than rebuild
- **Compressed Storage**: JSON serialization for persistent knowledge bases

### Search Optimization
- **Move Ordering**: Prioritize moves with better heuristic values
- **Pruning**: Eliminate obviously suboptimal paths early
- **Randomization**: Break ties randomly to avoid search bias

## Troubleshooting

### Common Issues

**Knowledge Base Not Found**
```bash
Error: knowledge_base.json not found
Solution: Set REBUILD_KNOWLEDGE = True to generate new database
```

**Memory Issues with Large Depths**
```bash
MemoryError: Cannot allocate array
Solution: Reduce EXPLORATION_DEPTH to 3-5 for standard systems
```

**Slow Solving Performance**
```bash
Search taking too long
Solution: Increase EXPLORATION_DEPTH for better heuristics
```

### Performance Tuning Tips
1. **Start Small**: Begin with EXPLORATION_DEPTH = 3
2. **Gradual Increase**: Increment depth as needed for harder puzzles  
3. **Cache Management**: Keep knowledge_base.json for faster startups
4. **Memory Monitoring**: Watch system resources with large knowledge bases

## Development

### Project Structure
```
puzzle-solver/
├── puzzle_engine.py      # Core puzzle mechanics
├── search_algorithm.py   # AI solving algorithms  
├── puzzle_runner.py      # Main application
├── knowledge_base.json   # Heuristic database (generated)
└── README.md            # Documentation
```

### Extending the System

**Custom Move Types**
```python
def custom_transformation(self, params):
    # Implement new transformation logic
    pass

# Register in move catalog
def generate_move_catalog(puzzle_size):
    standard_moves = [...]
    custom_moves = [('custom', i, j) for i in range(n) for j in range(2)]
    return standard_moves + custom_moves
```

**Alternative Heuristics**
```python
class CustomHeuristic:
    def evaluate(self, state):
        # Implement custom heuristic calculation
        return estimated_moves_to_solve
```

**Different Search Strategies**
```python
class AlternativeSearchEngine(AdaptiveSearchEngine):
    def solve_puzzle(self, state):
        # Implement alternative search algorithm
        pass
```

## Technical Specifications

### System Requirements
- **Python**: 3.7 or higher
- **Memory**: 512MB+ (varies with knowledge base size)  
- **Storage**: 10MB+ for knowledge base files
- **Dependencies**: `tqdm` for progress tracking

### Algorithmic Complexity
- **Time**: O(b^d) worst case, significantly better with heuristics
- **Space**: O(bd) for search, O(b^h) for knowledge base
- **Optimality**: Guaranteed optimal solutions with admissible heuristics

Where:
- `b` = branching factor (18 for 3×3×3 puzzle)
- `d` = solution depth  
- `h` = heuristic exploration depth

### Supported Puzzle Types
- **Standard**: 3×3×3 (Rubik's cube)
- **Mini**: 2×2×2 (Pocket cube)
- **Extended**: 4×4×4, 5×5×5, etc.
- **Custom**: Any n×n×n configuration

## License & Credits

This advanced cubic puzzle solver demonstrates sophisticated AI search techniques applied to combinatorial optimization problems. The system showcases practical applications of heuristic search, knowledge base construction, and iterative deepening algorithms.

**Key Innovations**:
- Adaptive search depth management
- Efficient state space exploration  
- Interactive puzzle manipulation interface
- Scalable knowledge base architecture

---

*For technical support or feature requests, please refer to the project documentation or submit an issue.*