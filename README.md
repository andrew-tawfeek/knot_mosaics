### CodeSpace Launch Instructions
Upon launching a CodeSpace, after it has finished building, run `sage -n jupyter --no-browser` in a new terminal window.

Then, when working in a Jupyter notebook, select the terminal to be an "Exisiting Jupyter Server" and paste in the 127.0.0.1 link (ending in a token) into the provided text-entry box.

# TODO:
- Convert over all knots into library of such in package
- Pull request into SageMath
- Write documentation for main python file


# Knot Mosaic Theory in SageMath

A comprehensive implementation of mosaic theory for knot and link diagrams in SageMath. This library provides tools for creating, manipulating, and analyzing knot mosaics using a grid-based tile system.

## Overview

Mosaic theory represents knots and links using a grid of standardized tiles, each containing specific curve segments that connect at the edges. This implementation provides 11 different tile types (numbered 0 - 10) that can be combined to form complete knot diagrams.

### Tile Types

- **Tile 0**: Empty tile with no connections
- **Tiles 1-6**: Two-connection tiles (curves, straight lines)
  - Tiles 1-4: Quarter-circle arcs connecting different edge combinations
  - Tile 5: Horizontal line segment
  - Tile 6: Vertical line segment
- **Tiles 7-10**: Four-connection crossing tiles
  - Tiles 7-8: Over/under crossings
  - Tiles 9-10: Crossing tiles with different orientations

## Features

### Core Classes

#### `Tile(N)`
Represents individual mosaic tiles with the following capabilities:
- Visual rendering with customizable resolution
- Connection point tracking and validation
- Orientation management
- Zoom functionality for detailed analysis

#### `Mosaic(mosaic_matrix)`
Represents complete knot diagrams as matrices of tiles:
- Matrix-based representation of knot diagrams
- Connectivity validation
- Visual rendering of complete mosaics
- Topological analysis tools

### Key Functionality

- **Visualization**: Generate high-quality graphics of individual tiles and complete mosaics
- **Connectivity Analysis**: Verify that tiles properly connect to form valid knot diagrams
- **Strand Tracing**: Follow individual strands through the mosaic
- **Crossing Detection**: Identify and analyze crossing points
- **Zoom Operations**: Create detailed 3x magnifications of mosaics
- **Random Generation**: Create random mosaics with specified properties

## Usage Examples

### Creating and Visualizing a Simple Mosaic

```python
# Create a simple trefoil knot mosaic
M = matrix([[0,2,1,0,0],
            [2,9,10,1,0],
            [3,10,9,10,1],
            [0,3,7,8,4],
            [0,0,3,4,0]])

W = Mosaic(M)
W.show()  # Display the mosaic
print(W.isSuitablyConnected())  # Check connectivity
```

### Working with Individual Tiles

```python
# Create and display a crossing tile
tile = Tile(9)
tile.show()

# Check tile properties
print(tile.connectionDirections)  # ['up', 'down', 'left', 'right']
print(tile.isGoing('up'))  # True
```

### Analyzing Knot Properties

```python
# Find crossings in the mosaic
crossings = W.findCrossings()
print(f"Number of crossings: {W.numCrossings()}")

# Trace individual strands
strand = W.strandOf((1,1), 'up')  # Start at crossing (1,1) going up
print(f"Strand path: {strand}")
```

### Advanced Operations

```python
# Create a zoomed version (3x magnification)
W_zoomed = W.zoom()
W_zoomed.show()

# Generate a random mosaic
random_knot = random_mosaic(5, suitably_connected=True, num_crossings=3)
random_knot.show()

# Flip a mosaic
W_flipped = W.flip()
W_flipped.show()
```

## Installation and Requirements

This library requires SageMath to be installed. The code uses SageMath's matrix operations, graphics capabilities, and mathematical functions.

### Running in SageMath

1. Start SageMath
2. Load the library: `load('wild_mosaics.py')`
3. Begin creating and analyzing mosaics

## Mathematical Background

Mosaic theory provides a discrete approach to knot theory where:
- Knots are represented on an n×n grid
- Each grid position contains one of 11 standardized tiles
- Tiles must connect properly at boundaries to form valid knot diagrams
- The system preserves topological properties of the represented knots

This representation is particularly useful for:
- Computational knot theory
- Knot enumeration and classification
- Educational purposes and visualization
- Algorithmic knot manipulation

## Advanced Features

### Strand Analysis
- `strandOf()`: Trace complete strand paths through the mosaic
- `walk()`: Follow paths between crossings
- `findCrossings()`: Locate all crossing points

### Topological Operations
- `zoom()`: Create detailed 3× magnifications
- `flip()`: Perform reflection operations
- Connectivity validation for ensuring proper knot structure

### Random Generation
Generate random mosaics with:
- Specified dimensions
- Guaranteed connectivity
- Controlled number of crossings

## Future Development

The codebase includes foundations for:
- Planar diagram code generation (for Sage Links compatibility)
- Multi-component link analysis
- Tangle operations and compositions
- Graph-theoretic representations of knot structure

## References

- Mosaic theory for knot representation
- SageMath mathematical software system
- Classical knot theory and topology

This implementation provides a robust foundation for computational knot theory research and education within the SageMath environment.
