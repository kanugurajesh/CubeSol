# 🧩 3D Rubik's Cube Visualizer & Solver

An advanced, interactive 3D Rubik's Cube simulator with intelligent solving capabilities, built with Three.js and modern web technologies.

## ✨ Key Features

### 🎮 Interactive 3D Experience
- **Immersive 3D Visualization**: Photorealistic cube rendering with smooth animations
- **Intuitive Controls**: Full keyboard support with standard cube notation (F, B, L, R, U, D, M)
- **Orbit Camera**: 360° viewing with zoom and pan capabilities
- **Real-time Animations**: Fluid face rotations with optimized performance

### 🧠 Intelligent Solving System
- **Advanced Algorithm**: Sophisticated solving engine that can solve any scrambled cube configuration
- **Move Optimization**: Smart sequence optimization to minimize solution length
- **Local Processing**: Lightning-fast solving without external dependencies
- **Progressive Display**: Real-time solution visualization as moves are executed

### 🎯 Smart Scrambling
- **Customizable Scrambles**: Configure scramble complexity with min/max move ranges
- **Intelligent Move Generation**: Avoids consecutive moves on same faces for realistic scrambles
- **Visual Feedback**: Progress tracking during scramble execution
- **Random Seed System**: Generates unique cube configurations every time

### 💡 Advanced Move Management
- **Move Tracking**: Complete history of all moves with undo functionality
- **Sequence Optimization**: Automatic cancellation of redundant moves (R R' = identity)
- **Double Move Handling**: Efficient processing of 180° rotations
- **State Management**: Robust cube state tracking and restoration

### 🎨 Modern UI/UX
- **Bootstrap Integration**: Clean, responsive interface design
- **Loading States**: Visual feedback during solving and scrambling operations
- **Tooltips & Hints**: Helpful guidance for keyboard shortcuts and controls
- **Modal Dialogs**: Elegant scramble configuration interface
- **Message System**: Clear status updates and notifications

### 🔧 Technical Excellence
- **Modular Architecture**: Well-organized ES6 modules for maintainability
- **Three.js Integration**: Leverages WebGL for high-performance 3D rendering
- **Memory Efficient**: Optimized cube representation and animation handling
- **Cross-browser Compatible**: Works seamlessly across modern web browsers

## 🚀 Getting Started

1. Open `index.html` in your web browser
2. Use keyboard controls to manipulate the cube:
   - **F/B**: Front/Back face rotations
   - **L/R**: Left/Right face rotations  
   - **U/D**: Up/Down face rotations
   - **M**: Middle layer rotation
   - **1/2**: Toggle between clockwise/counterclockwise
3. Click **Scramble** to randomize the cube
4. Click **Solve** to watch the intelligent algorithm solve it automatically
5. Use **Undo** to reverse moves or **Reset** to start fresh

## 🎪 Demo Capabilities

This visualizer demonstrates:
- **Complex Algorithm Implementation**: Showcases advanced cube-solving techniques
- **3D Graphics Programming**: Professional-grade WebGL rendering
- **Interactive Animation Systems**: Smooth, responsive user interactions
- **Mathematical Optimization**: Efficient move sequence reduction
- **Modern Web Development**: ES6 modules, async/await, and modern APIs

## 🏗️ Architecture

### 📊 Data Structures & Cube Representation

**Backend Core Engine** (`puzzle_engine.py`):

**Primary Data Structure:**
- **6-Face Matrix System**: `self.matrix[face][row][col]` - 3D array representing cube state
  - Face 0: Top (White)    - `self.matrix[0]`
  - Face 1-4: Sides        - `self.matrix[1-4]` (Orange, Green, Red, Blue)  
  - Face 5: Bottom (Yellow) - `self.matrix[5]`
  - Each face: 3×3 grid storing color characters

**Cube State Management:**
- **Color Palette**: `self.face_colors = ['W', 'O', 'G', 'R', 'B', 'Y']` - standardized color scheme
- **State Serialization**: Linear string format (54 characters total) for efficient storage/transmission
- **Factory Reset**: `_initialize_solved_state()` creates pristine solved configuration
- **State Validation**: `is_completion_achieved()` verifies monochromatic face completion

**Advanced Search Engine** (`search_algorithm.py`):

**State Space Representation:**
- **Knowledge Database**: `Dict[str, int]` mapping cube states to minimum solve distances
- **Move Cache**: `Dict[Tuple, str]` for O(1) state transition lookups
- **Visited States**: `Set` with depth-aware cycle detection for pruning
- **Solution Path**: `List[Tuple[str, int, int]]` storing move sequences

**Heuristic Systems:**
- **Pattern Database**: Pre-computed distances for corner/edge piece patterns
- **Manhattan Distance**: Misplaced piece counting for admissible heuristic
- **Corner/Edge Heuristics**: Specialized pattern recognition for complex states

**Frontend Visualizer** (`rubik.js`):

**3D Representation:**
- **Cubelet Array**: `cubesArray3D[x][y][z]` - 3×3×3 THREE.js mesh grid
- **Coordinate System**: Positions at (-1.1, 0, 1.1) with 1.1 unit spacing
- **Material Mapping**: 6 face materials per cubelet with selective visibility
- **World Position Tracking**: Real-time 3D coordinate resolution via `round()` function

**Geometric Operations:**
- **Matrix Transformations**: `THREE.Matrix4` for precise face rotations
- **Position Rounding**: Custom `round()` maps floating positions to discrete coordinates
- **Face Identification**: Position-based cubelet selection for layer operations

### 🎯 State Prediction & Move Engine Logic

**Core Move Engine** (`puzzle_engine.py`):

**Three Fundamental Operations:**
1. **Horizontal Rotations** (`execute_horizontal_rotation:139-183`):
   - **Layer Selection**: Targets horizontal slices (U/D layers)
   - **Matrix Permutation**: Cycles 4 side faces in clockwise/counter-clockwise order
   - **Connected Face Logic**: Automatically rotates top/bottom faces when edge layers move
   - **Boundary Validation**: Prevents invalid layer indices with error handling

2. **Vertical Rotations** (`execute_vertical_rotation:185-231`):
   - **Column Operations**: Processes vertical columns through front/back/top/bottom
   - **Complex Permutation**: Handles inverted coordinates for back face mappings
   - **Side Face Rotation**: Triggers left/right face rotations for edge columns
   - **Coordinate Transformation**: Maps 3D positions through multiple face transitions

3. **Lateral Rotations** (`execute_lateral_rotation:232-277`):
   - **Front/Back Operations**: Manages slices perpendicular to viewing direction
   - **Multi-face Coordination**: Coordinates top/left/right/bottom face transitions  
   - **Position Mapping**: Complex coordinate transformations for slice movements
   - **Face Dependency**: Automatic front/back face rotations for edge slices

**Advanced Search Algorithms** (`search_algorithm.py`):

**Multi-Algorithm Solver System:**
1. **Breadth-First Search** (`_breadth_first_search:60-82`):
   - **Optimal Solutions**: Guarantees shortest path for shallow scrambles (≤6 moves)
   - **Memory Intensive**: Stores all states at current depth level
   - **Early Termination**: Timeout mechanism prevents infinite exploration

2. **Bidirectional Search** (`_bidirectional_search:84-138`):
   - **Meet-in-Middle**: Searches from both solved and scrambled states
   - **Exponential Reduction**: O(b^(d/2)) complexity vs O(b^d) for BFS
   - **Frontier Management**: Maintains forward/backward exploration queues
   - **Connection Detection**: Identifies solution when frontiers intersect

3. **IDA* with Pattern Database** (`_ida_star_search:140-167`):
   - **Iterative Deepening**: Gradually increases search depth threshold
   - **Heuristic Pruning**: Uses pattern database for informed search
   - **Memory Efficient**: O(d) space complexity - stores only current path
   - **Admissible Heuristics**: Multiple heuristic strategies (Manhattan, corner, edge)

**State Prediction System:**

**Move Generation & Ordering** (`_generate_ordered_moves:206-243`):
- **Smart Prioritization**: Outer layer moves preferred (affect more pieces)
- **Inverse Move Avoidance**: Prevents immediate undo of previous operations
- **Heuristic Guidance**: Moves improving heuristic value get priority
- **Performance Optimization**: Reduces search tree branching factor

**Caching & Performance** (`_get_next_state:250-272`):
- **Dynamic Caching**: LRU-style cache with automatic size management
- **Cache Hit Tracking**: Performance metrics for optimization analysis
- **Memory Bounds**: Configurable cache limits prevent memory overflow
- **State Transitions**: Efficient cube state transformations with validation

**Frontend Animation Engine** (`rubik.js`, `motion.js`):

**3D Transformation System:**
- **Matrix Operations**: THREE.js Matrix4 transformations for precise rotations
- **Layer Selection**: Position-based cubelet identification using `round()` function
- **Smooth Interpolation**: Keyframe-based animation with configurable timing
- **Visual Prediction**: Real-time preview of move sequences during solution playback

### 🚀 Efficient Implementation Patterns

**Computational Efficiency:**
- **O(1) Face Rotations**: Matrix transformations enable constant-time face operations regardless of cube size
- **Branching Factor Optimization**: Smart move ordering reduces search tree from 18^d to ~8^d effective branches
- **Memory Management**: Dynamic cache sizing with LRU eviction prevents memory overflow
- **Lazy Evaluation**: State transitions computed only when needed, cached for reuse

**Data Structure Optimizations:**
- **Compact State Representation**: 54-character strings enable efficient hashing and storage
- **Pattern Database**: Pre-computed distances for O(1) heuristic lookups vs O(n²) calculation
- **Depth-Aware Pruning**: Visited state tracking with modulo-depth prevents infinite cycles
- **Bidirectional Frontiers**: Meet-in-middle reduces exponential search space by half

**Animation & Rendering:**
- **Position-Based Identification**: Smart `round()` function for precise cubelet identification (`rubik.js:83-94`)
- **Keyframe Interpolation**: Smooth animation transitions using linear interpolation (`motion.js:28-37`)
- **Selective Material Updates**: Only visible faces rendered, reducing GPU load
- **Matrix Premultiplication**: THREE.js transformations applied directly to avoid recalculation

**Algorithm Integration:**
- **Multi-Strategy Solving**: Adaptive algorithm selection based on scramble complexity
- **Move Optimization**: Advanced sequence reduction algorithms that eliminate redundant operations
- **Early Termination**: Timeout mechanisms prevent excessive computation on difficult states
- **Solution Caching**: Optimal paths stored for instant replay and analysis

### 📁 Module Organization

- **`main.js`**: Core application initialization and game loop
- **`rubik.js`**: 3D cube creation and face rotation mechanics  
- **`solutionService.js`**: Intelligent solving algorithm implementation
- **`scramble.js`**: Smart randomization and move generation
- **`api.js`**: Local move tracking and sequence optimization
- **`animations.js`**: Smooth face rotation animations with keyframe system
- **`motion.js`**: Keyframe and Motion classes for animation control
- **`sceneManager.js`**: THREE.js scene setup and rendering pipeline
- **`keyHandler.js`**: Keyboard input processing and move execution

## 🎯 Perfect For

- **Algorithm Visualization**: Demonstrates complex problem-solving techniques
- **3D Graphics Learning**: Shows advanced Three.js implementation patterns
- **Interactive Demos**: Engaging way to explore cube-solving algorithms
- **Educational Tools**: Visual learning aid for understanding cube mechanics
- **Portfolio Projects**: Showcases full-stack development skills

---

*Experience the fascinating world of algorithmic problem-solving with this cutting-edge 3D Rubik's Cube solver!*