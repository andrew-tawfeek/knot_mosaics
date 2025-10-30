# Function Dependency Tree for `wild_mosaics.py`

**LAST UPDATED OCTOBER 30TH, 2025**


This document illustrates the complete dependency tree of all functions and methods within `wild_mosaics.py`, showing which functions call which other functions.

---

## Table of Contents
- [Class: Tile](#class-tile)
- [Class: Mosaic](#class-mosaic)
- [Standalone Functions](#standalone-functions)
- [Complete Dependency Graph](#complete-dependency-graph)

---

## Class: Tile

### Methods

#### `__init__(self, N)`
**Dependencies:** None  
**Description:** Constructor for Tile objects. Initializes tile properties based on tile number.

#### `exitPath(self, direction)`
**Dependencies:**
- `flatten()` (external, from SageMath)

**Description:** Given a direction of entry, returns the exit direction.

#### `show(self, resolution=5)`
**Dependencies:**
- `line()` (external, from SageMath)
- `arc()` (external, from SageMath)

**Description:** Returns a graphical representation of the tile.

#### `isGoing(self, direction)`
**Dependencies:**
- `flatten()` (external)

**Description:** Checks if a tile has a connection in the specified direction.

#### `zoom(self, onlyUpDown=False)`
**Dependencies:** None  
**Description:** Expands a tile into a 3x3 matrix of tiles (isotopy equivalent).

#### `orient(self, direction)`
**Dependencies:**
- `flatten()` (external)

**Description:** Assigns an orientation to a tile.

---

## Class: Mosaic

### Methods

#### `__init__(self, mosaic_matrix)`
**Dependencies:**
- `matrix()` (external, from SageMath)

**Description:** Constructor for Mosaic objects.

#### `__repr__(self)`
**Dependencies:** None  
**Description:** Returns string representation of the mosaic.

#### `show(self, resolution=5)`
**Dependencies:**
- `Tile.__init__()` (instantiates Tile objects)
- `Tile.show()`
- `graphics_array()` (external, from SageMath)

**Description:** Displays a graphical representation of the entire mosaic.

#### `matrix(self)`
**Dependencies:** None  
**Description:** Returns the matrix representation of the mosaic.

#### `directions(self, i, j)`
**Dependencies:**
- `Tile.__init__()`
- `flatten()` (external)

**Description:** Returns the connection directions of a specific tile at position (i,j).

#### `isSuitablyConnected(self)`
**Dependencies:**
- `Tile.__init__()`
- `Tile.isGoing()`

**Description:** Checks if all tiles in the mosaic are properly connected to their neighbors.

#### `zoom(self, onlyUpDown=False)`
**Dependencies:**
- `Tile.__init__()`
- `Tile.zoom()`
- `Mosaic.__init__()` (creates new Mosaic)
- `floor()` (external)

**Description:** Zooms the entire mosaic by replacing each tile with a 3x3 equivalent.

#### `findCrossings(self)`
**Dependencies:** None  
**Description:** Returns a list of coordinates containing crossing tiles (9 or 10).

#### `numCrossings(self)`
**Dependencies:**
- `Mosaic.findCrossings()`

**Description:** Returns the count of crossing tiles.

#### `exitPath(self, i, j, direction)`
**Dependencies:**
- `Tile.__init__()`
- `Tile.exitPath()`
- `flatten()` (external)

**Description:** Given a tile position and entry direction, returns the exit tile and direction.

#### `shift(self, i, j, dictionary=False)`
**Dependencies:**
- `Mosaic.isSuitablyConnected()`
- `Tile.__init__()`

**Description:** Returns the coordinates of adjacent tiles connected to tile (i,j).

#### `walk(self, crossing, direction, pathList=False, tangent=False)`
**Dependencies:**
- `Mosaic.findCrossings()`
- `Tile.__init__()`
- `Mosaic.shift()`
- `opposite()` (standalone function)

**Description:** Walks from a crossing in a given direction until reaching another crossing.

#### `arcList(self)`
**Dependencies:** None (unimplemented stub)  
**Description:** Intended to return all arcs in the mosaic (currently not implemented).

#### `strandOf(self, tile, direction=None, direction_tracking=False, verbose=False)`
**Dependencies:**
- `Tile.__init__()`
- `flatten()` (external)
- `opposite()` (standalone function)
- `random.choice()` (external)
- `Mosaic.exitPath()`

**Description:** Traces a complete strand starting from a given tile.

#### `strandMatrix(self)`
**Dependencies:**
- `Tile.__init__()`
- `matrix()` (external)

**Description:** Returns a matrix showing the number of strands at each tile position.

#### `strands(self)`
**Dependencies:**
- `Mosaic.strandMatrix()`
- `Mosaic.strandOf()`

**Description:** Returns all distinct strands in the mosaic.

#### `numComponents(self)`
**Dependencies:**
- `Mosaic.isSuitablyConnected()`
- `Mosaic.strands()`

**Description:** Returns the number of connected components (strands) in the mosaic.

#### `localFrames(self)`
**Dependencies:**
- `Mosaic.findCrossings()`
- `Mosaic.shift()`

**Description:** Returns the tiles above/below each crossing.

#### `planarDiagramCode(self)`
**Dependencies:** None (unimplemented stub)  
**Description:** Intended to generate planar diagram code for Sage compatibility.

#### `flip(self)`
**Dependencies:**
- `Mosaic.__init__()`

**Description:** Flips the mosaic upside-down while maintaining connectivity.

#### `potential_tiles(self, i, j)`
**Dependencies:**
- `Mosaic.directions()`
- `Tile.__init__()`
- `flatten()` (external)

**Description:** Returns a list of valid tile numbers that can be placed at position (i,j).

---

## Standalone Functions

### `opposite(direction)`
**Dependencies:** None  
**Description:** Returns the opposite direction (up↔down, left↔right).

### `random_mosaic(dimension, suitably_connected=True, num_crossings=-1, num_components=-1)`
**Dependencies:**
- `Mosaic.__init__()`
- `Mosaic.potential_tiles()`
- `Mosaic.findCrossings()`
- `Mosaic.numComponents()`
- `random_matrix()` (external, from SageMath)
- `choice()` (external)
- `matrix()` (external)
- `ZZ` (external, from SageMath)
- `GF()` (external, from SageMath)

**Description:** Generates a random mosaic with specified properties.

### `tangleConstructor(value, flip=False)`
**Dependencies:**
- `Mosaic.__init__()`
- `ZZ` (external)
- `diagonal_matrix()` (external, from SageMath)

**Description:** Constructs a tangle mosaic for a given value.

**Helper Function (nested):**
- `jordan_block_modified(eigenvalue, size, sparse=False, flip=False)` - Creates a modified Jordan block matrix

### `tangleJoin(tangle_list)`
**Dependencies:**
- `tangleConstructor()`
- `Mosaic.__init__()`
- `matrix()` (external)
- `block_matrix()` (external, from SageMath)

**Description:** Joins two tangles together into a single mosaic.

**Helper Function (nested):**
- `tangleConnector(n, m, direction)` - Creates a connecting strand between tangles

---

## Complete Dependency Graph

Below is a hierarchical view of the complete dependency relationships:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL DEPENDENCIES                        │
│  (SageMath built-ins: matrix, flatten, graphics_array, line, arc,  │
│   floor, random_matrix, ZZ, GF, diagonal_matrix, block_matrix,     │
│   Python: random.choice)                                            │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         STANDALONE FUNCTIONS                         │
└─────────────────────────────────────────────────────────────────────┘
│
├─ opposite()
│  └─ No dependencies
│
├─ tangleConstructor(value, flip)
│  ├─ Mosaic.__init__()
│  └─ jordan_block_modified() [nested helper]
│
├─ tangleJoin(tangle_list)
│  ├─ tangleConstructor()
│  ├─ Mosaic.__init__()
│  └─ tangleConnector() [nested helper]
│
└─ random_mosaic(dimension, ...)
   ├─ Mosaic.__init__()
   ├─ Mosaic.potential_tiles()
   ├─ Mosaic.findCrossings()
   └─ Mosaic.numComponents()

┌─────────────────────────────────────────────────────────────────────┐
│                            CLASS: Tile                               │
└─────────────────────────────────────────────────────────────────────┘
│
├─ __init__(N)
│  └─ No internal dependencies
│
├─ exitPath(direction)
│  └─ flatten() [external]
│
├─ show(resolution)
│  └─ line(), arc() [external]
│
├─ isGoing(direction)
│  └─ flatten() [external]
│
├─ zoom(onlyUpDown)
│  └─ No internal dependencies
│
└─ orient(direction)
   └─ flatten() [external]

┌─────────────────────────────────────────────────────────────────────┐
│                          CLASS: Mosaic                               │
└─────────────────────────────────────────────────────────────────────┘
│
├─ __init__(mosaic_matrix)
│  └─ matrix() [external]
│
├─ __repr__()
│  └─ No dependencies
│
├─ matrix()
│  └─ No dependencies
│
├─ show(resolution)
│  ├─ Tile.__init__()
│  ├─ Tile.show()
│  └─ graphics_array() [external]
│
├─ directions(i, j)
│  ├─ Tile.__init__()
│  └─ flatten() [external]
│
├─ isSuitablyConnected()
│  ├─ Tile.__init__()
│  └─ Tile.isGoing()
│
├─ zoom(onlyUpDown)
│  ├─ Tile.__init__()
│  ├─ Tile.zoom()
│  ├─ Mosaic.__init__()
│  └─ floor() [external]
│
├─ findCrossings()
│  └─ No internal dependencies
│
├─ numCrossings()
│  └─ Mosaic.findCrossings()
│
├─ exitPath(i, j, direction)
│  ├─ Tile.__init__()
│  ├─ Tile.exitPath()
│  └─ flatten() [external]
│
├─ shift(i, j, dictionary)
│  ├─ Mosaic.isSuitablyConnected()
│  │  ├─ Tile.__init__()
│  │  └─ Tile.isGoing()
│  └─ Tile.__init__()
│
├─ walk(crossing, direction, pathList, tangent)
│  ├─ Mosaic.findCrossings()
│  ├─ Tile.__init__()
│  ├─ Mosaic.shift()
│  │  ├─ Mosaic.isSuitablyConnected()
│  │  └─ Tile.__init__()
│  └─ opposite() [standalone]
│
├─ arcList()
│  └─ Not implemented
│
├─ strandOf(tile, direction, direction_tracking, verbose)
│  ├─ Tile.__init__()
│  ├─ flatten() [external]
│  ├─ opposite() [standalone]
│  ├─ random.choice() [external]
│  └─ Mosaic.exitPath()
│     ├─ Tile.__init__()
│     ├─ Tile.exitPath()
│     └─ flatten() [external]
│
├─ strandMatrix()
│  ├─ Tile.__init__()
│  └─ matrix() [external]
│
├─ strands()
│  ├─ Mosaic.strandMatrix()
│  │  ├─ Tile.__init__()
│  │  └─ matrix() [external]
│  └─ Mosaic.strandOf()
│     ├─ Tile.__init__()
│     ├─ flatten() [external]
│     ├─ opposite() [standalone]
│     └─ Mosaic.exitPath()
│
├─ numComponents()
│  ├─ Mosaic.isSuitablyConnected()
│  │  ├─ Tile.__init__()
│  │  └─ Tile.isGoing()
│  └─ Mosaic.strands()
│     ├─ Mosaic.strandMatrix()
│     └─ Mosaic.strandOf()
│
├─ localFrames()
│  ├─ Mosaic.findCrossings()
│  └─ Mosaic.shift() [called twice]
│     ├─ Mosaic.isSuitablyConnected()
│     └─ Tile.__init__()
│
├─ planarDiagramCode()
│  └─ Not implemented
│
├─ flip()
│  └─ Mosaic.__init__()
│
└─ potential_tiles(i, j)
   ├─ Mosaic.directions()
   │  ├─ Tile.__init__()
   │  └─ flatten() [external]
   ├─ Tile.__init__()
   └─ flatten() [external]

```

---

## Dependency Levels (Bottom-Up)

### Level 0: No Internal Dependencies
- `opposite()`
- `Tile.__init__()`
- `Tile.zoom()`
- `Mosaic.__init__()`
- `Mosaic.__repr__()`
- `Mosaic.matrix()`
- `Mosaic.findCrossings()`

### Level 1: Depends only on Level 0
- `Tile.exitPath()` → uses `flatten()` only
- `Tile.show()` → uses external graphics only
- `Tile.isGoing()` → uses `flatten()` only
- `Tile.orient()` → uses `flatten()` only
- `Mosaic.numCrossings()` → uses `Mosaic.findCrossings()`
- `Mosaic.flip()` → uses `Mosaic.__init__()`

### Level 2: Depends on Level 0-1
- `Mosaic.directions()` → `Tile.__init__()`, `flatten()`
- `Mosaic.show()` → `Tile.__init__()`, `Tile.show()`
- `Mosaic.isSuitablyConnected()` → `Tile.__init__()`, `Tile.isGoing()`
- `Mosaic.exitPath()` → `Tile.__init__()`, `Tile.exitPath()`
- `Mosaic.strandMatrix()` → `Tile.__init__()`
- `Mosaic.zoom()` → `Tile.__init__()`, `Tile.zoom()`, `Mosaic.__init__()`

### Level 3: Depends on Level 0-2
- `Mosaic.shift()` → `Mosaic.isSuitablyConnected()`, `Tile.__init__()`
- `Mosaic.potential_tiles()` → `Mosaic.directions()`, `Tile.__init__()`
- `Mosaic.strandOf()` → `Tile.__init__()`, `Mosaic.exitPath()`, `opposite()`

### Level 4: Depends on Level 0-3
- `Mosaic.walk()` → `Mosaic.findCrossings()`, `Mosaic.shift()`, `Tile.__init__()`, `opposite()`
- `Mosaic.strands()` → `Mosaic.strandMatrix()`, `Mosaic.strandOf()`
- `Mosaic.localFrames()` → `Mosaic.findCrossings()`, `Mosaic.shift()`

### Level 5: Depends on Level 0-4
- `Mosaic.numComponents()` → `Mosaic.isSuitablyConnected()`, `Mosaic.strands()`
- `random_mosaic()` → `Mosaic.__init__()`, `Mosaic.potential_tiles()`, `Mosaic.findCrossings()`, `Mosaic.numComponents()`

### Level 6: Depends on Level 0-5
- `tangleJoin()` → `tangleConstructor()`, `Mosaic.__init__()`

---

## Key Observations

1. **Most Depended Upon Functions:**
   - `Tile.__init__()` - Called by nearly every Mosaic method
   - `Mosaic.__init__()` - Used to create new Mosaic instances
   - `flatten()` - External function used throughout for list processing
   - `opposite()` - Standalone utility function used in strand tracing

2. **Most Complex Dependencies:**
   - `random_mosaic()` - Depends on 4 different Mosaic methods
   - `Mosaic.numComponents()` - Deep dependency chain through strands
   - `Mosaic.walk()` - Complex logic with multiple method calls

3. **Independent Functions:**
   - `opposite()` - No internal dependencies
   - `Tile.__init__()` - Foundation of the Tile class
   - `Mosaic.findCrossings()` - Simple matrix scanning

4. **Unimplemented Stubs:**
   - `Mosaic.arcList()`
   - `Mosaic.planarDiagramCode()`

---

## Notes

- All external dependencies are from SageMath (mathematical computation system) or Python's standard library
- The code implements mathematical concepts from knot theory and mosaic theory
- Circular dependencies are avoided through careful design
- Helper functions are nested within their parent functions where appropriate
