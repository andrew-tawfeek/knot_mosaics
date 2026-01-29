# An implementation of mosaic theory into SageMath.

import random

# Tile configuration data - defines connection directions for each tile type
TILE_CONNECTIONS = {
    0: [],
    1: ['left', 'down'],
    2: ['right', 'down'],
    3: ['up', 'right'],
    4: ['left', 'up'],
    5: ['left', 'right'],
    6: ['up', 'down'],
    7: [['down', 'left'], ['up', 'right']],
    8: [['down', 'right'], ['left', 'up']],
    9: [['down', 'up'], ['left', 'right']],
    10: [['left', 'right'], ['down', 'up']],
}

# Tiles that have 4 connection points (2 strands)
FOUR_POINT_TILES = {7, 8, 9, 10}

# Crossing tiles
CROSSING_TILES = {9, 10}

# Zoom mappings for each tile type (3x3 matrix representation)
TILE_ZOOM_MAPS = {
    0: [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    1: [[0, 0, 0], [5, 1, 0], [0, 6, 0]],
    2: [[0, 0, 0], [0, 2, 5], [0, 6, 0]],
    3: [[0, 6, 0], [0, 3, 5], [0, 0, 0]],
    4: [[0, 6, 0], [5, 4, 0], [0, 0, 0]],
    5: [[0, 0, 0], [5, 5, 5], [0, 0, 0]],
    6: [[0, 6, 0], [0, 6, 0], [0, 6, 0]],
    7: [[0, 3, 1], [1, 0, 3], [3, 1, 0]],
    8: [[2, 4, 0], [4, 0, 2], [0, 2, 4]],
    9: [[0, 6, 0], [5, 9, 5], [0, 6, 0]],
    10: [[0, 6, 0], [5, 10, 5], [0, 6, 0]],
}

# Special zoom for tile 9 with onlyUpDown option
TILE_9_UP_DOWN_ZOOM = [[2, 8, 1], [7, 10, 7], [3, 8, 4]]

# Tiles that connect in each direction
TILES_GOING_UP = {3, 4, 6, 7, 8, 9, 10}
TILES_GOING_DOWN = {1, 2, 6, 7, 8, 9, 10}
TILES_GOING_LEFT = {1, 4, 5, 7, 8, 9, 10}
TILES_GOING_RIGHT = {2, 3, 5, 7, 8, 9, 10}


def opposite(direction):
    """Returns the opposite direction."""
    direction_opposites = {
        'up': 'down',
        'down': 'up',
        'left': 'right',
        'right': 'left',
    }
    assert direction in direction_opposites
    return direction_opposites[direction]


class Tile:
    def __init__(self, N):
        self.tile = N
        self.orientation = []
        connections = TILE_CONNECTIONS.get(N, [])

        if N == 0:
            self.numConnectionPoints = 0
            self.numStrands = 0
            self.isCrossing = False
            self.connectionDirections = []
        elif N in range(1, 7):
            self.numConnectionPoints = 2
            self.numStrands = 1
            self.isCrossing = False
            self.connectionDirections = connections
        elif N in FOUR_POINT_TILES:
            self.numConnectionPoints = 4
            self.numStrands = 2
            self.isCrossing = N in CROSSING_TILES
            self.connectionDirections = connections

    def exitPath(self, direction):
        """Given a direction of entry, returns the exit direction."""
        assert direction in flatten(self.connectionDirections)

        if self.numStrands == 1:
            if direction == self.connectionDirections[0]:
                return self.connectionDirections[1]
            return self.connectionDirections[0]
        elif self.numStrands == 2:
            for strand in self.connectionDirections:
                if direction in strand:
                    return strand[1] if strand[0] == direction else strand[0]

    def show(self, resolution=5):
        """Returns a graphical representation of the tile."""
        plot_params = {
            'axes': False,
            'frame': True,
            'ticks': [[], []],
            'thickness': resolution
        }

        T_0 = line([(0, 0), (1, 0)], xmin=0, xmax=1, ymin=0, ymax=1, thickness=0, **{k: v for k, v in plot_params.items() if k != 'thickness'}).plot()
        T_1 = arc((0, 0), 1, sector=(0, pi/2), xmin=0, xmax=2, ymin=0, ymax=2, **plot_params).plot()
        T_2 = arc((0, 0), 1, sector=(0, pi), xmin=-2, xmax=0, ymin=0, ymax=2, **plot_params).plot()
        T_3 = arc((0, 0), 1, sector=(pi, 2*pi), xmin=-2, xmax=0, ymin=-2, ymax=0, **plot_params).plot()
        T_4 = arc((0, 0), 1, sector=(pi, 2*pi), xmin=0, xmax=2, ymin=-2, ymax=0, **plot_params).plot()
        T_5 = line([(0, 1), (1, 1)], xmin=0, xmax=1, ymin=0, ymax=2, **plot_params).plot()
        T_6 = line([(1, 0), (1, 1)], xmin=0, xmax=2, ymin=0, ymax=1, **plot_params).plot()
        T_7 = T_1 + arc((2, 2), 1, sector=(pi, 2*pi), xmin=0, xmax=2, ymin=0, ymax=2, **plot_params).plot()
        T_8 = (arc((0, 2), 1, sector=(2*pi/3, 2*pi), xmin=0, xmax=2, ymin=0, ymax=2, **plot_params).plot() +
               arc((2, 0), 1, sector=(pi, pi/2), xmin=0, xmax=2, ymin=0, ymax=2, **plot_params).plot())
        T_9 = (line([(0, 1), (2, 1)], xmin=0, xmax=2, ymin=0, ymax=2, **plot_params).plot() +
               line([(1, 0), (1, .6)], xmin=0, xmax=2, ymin=0, ymax=2, **plot_params).plot() +
               line([(1, 1.4), (1, 2)], xmin=0, xmax=2, ymin=0, ymax=2, **plot_params).plot())
        T_10 = (line([(1, 2), (1, 0)], xmin=0, xmax=2, ymin=0, ymax=2, **plot_params).plot() +
                line([(0, 1), (.6, 1)], xmin=0, xmax=2, ymin=0, ymax=2, **plot_params).plot() +
                line([(1.4, 1), (2, 1)], xmin=0, xmax=2, ymin=0, ymax=2, **plot_params).plot())

        tile_plots = {
            0: T_0, 1: T_1, 2: T_2, 3: T_3, 4: T_4, 5: T_5,
            6: T_6, 7: T_7, 8: T_8, 9: T_9, 10: T_10
        }
        return tile_plots.get(self.tile)

    def isGoing(self, direction):
        """Check if tile has a connection in the given direction.

        e.g. Tile(6).isGoing('up') returns True but Tile(6).isGoing('left') returns False.
        This is useful for checking suitable connectivity.
        """
        return direction in flatten(self.connectionDirections)

    def zoom(self, onlyUpDown=False):
        """Returns 3x3 matrix representation of the tile for zooming."""
        N = self.tile
        if N == 9 and onlyUpDown:
            # Twists to center a 10-tile instead
            return TILE_9_UP_DOWN_ZOOM
        return TILE_ZOOM_MAPS.get(N)

    def orient(self, direction):
        """Assigns an orientation to a tile."""
        assert direction in flatten(self.connectionDirections)
        self.orientation = self.orientation + [direction]


class Mosaic:
    def __init__(self, mosaic_matrix):
        """Takes input matrix or list of lists (array)."""
        self.matrixRepresentation = matrix(mosaic_matrix)
        self.size = len(self.matrixRepresentation.rows())

    def __repr__(self):
        return f"Mosaic of dimension {self.size}."

    def show(self, resolution=5):
        """Outputs a graphic for the mosaic."""
        M = self.matrixRepresentation
        tile_rows = [[Tile(x).show() for x in list(row)] for row in M]
        return graphics_array(tile_rows).show(figsize=[resolution, resolution])

    def matrix(self):
        """Returns the matrix representation of the mosaic."""
        return self.matrixRepresentation

    def directions(self, i, j):
        """Returns the connection points of the (i,j)th tile.

        Position (0,0) is the tile in the upper-left (matrix notation, indexed at 0).
        """
        M = self.matrixRepresentation
        return flatten(Tile(M[i][j]).connectionDirections)

    def isSuitablyConnected(self):
        """Checks if all tile edges connect properly."""
        M = self.matrixRepresentation
        for i in range(self.size):
            for j in range(self.size):
                tile = Tile(M[i][j])

                if tile.isGoing('up'):
                    if i == 0 or not Tile(M[i-1][j]).isGoing('down'):
                        return False

                if tile.isGoing('left'):
                    if j == 0 or not Tile(M[i][j-1]).isGoing('right'):
                        return False

                if tile.isGoing('right'):
                    if j == self.size - 1 or not Tile(M[i][j+1]).isGoing('left'):
                        return False

                if tile.isGoing('down'):
                    if i == self.size - 1 or not Tile(M[i+1][j]).isGoing('up'):
                        return False
        return True

    def zoom(self, onlyUpDown=False):
        """Zooms by 3x, replaces each tile by a 3x3 isotopy equivalent tile.

        If onlyUpDown=True, all 9 tiles are replaced by twisted 10 tiles (isotopy equivalent).
        """
        M = self.matrixRepresentation
        M_tensored = [[Tile(x).zoom(onlyUpDown) for x in list(row)] for row in list(M)]

        # Unwrap inner 3x3 subtiles
        A = []
        for n in range(len(M_tensored) * 3):
            # Euclidean division: n = floor(n/3)*3 + n%3
            A.append([x[n % 3] for x in M_tensored[floor(n / 3)]])

        # Unwrap inner 1x3 subtiles
        B = []
        for row in A:
            flat_row = []
            for subtuple in row:
                flat_row += subtuple
            B.append(flat_row)

        return Mosaic(B)

    def findCrossings(self):
        """Returns a list of coordinates (i,j) in the matrix of crossings (9/10 tiles)."""
        M = self.matrixRepresentation
        n = self.size
        M_rows = [list(x) for x in M.rows()]
        crossing_coord = []

        for i in range(n):
            row_crossings = [j for j, x in enumerate(M_rows[i]) if x in CROSSING_TILES]
            crossing_coord += [(i, j) for j in row_crossings]

        return crossing_coord

    def numCrossings(self):
        """Returns the number of crossings in the mosaic."""
        return len(self.findCrossings())

    def exitPath(self, i, j, direction):
        """Given a tile (i,j) and direction of entry, returns the next tile and exit direction."""
        M = self.matrixRepresentation
        assert direction in flatten(Tile(M[i][j]).connectionDirections)

        T = Tile(M[i][j])
        exit_dir = T.exitPath(direction)

        next_positions = {
            'up': ((i - 1, j), 'up'),
            'down': ((i + 1, j), 'down'),
            'left': ((i, j - 1), 'left'),
            'right': ((i, j + 1), 'right'),
        }
        return list(next_positions[exit_dir])

    def shift(self, i, j, dictionary=False):
        """Returns coordinates of adjacent connected tiles.

        Setting 'dictionary=True' returns a dict mapping directions to tile coordinates.
        """
        assert self.isSuitablyConnected()
        M = self.matrixRepresentation
        N = Tile(M[i][j])
        directions = N.connectionDirections

        def shifter(direction):
            directions_dict = {}
            if 'up' in directions:
                directions_dict['up'] = (i - 1, j)
            if 'down' in directions:
                directions_dict['down'] = (i + 1, j)
            if 'left' in directions:
                directions_dict['left'] = (i, j - 1)
            if 'right' in directions:
                directions_dict['right'] = (i, j + 1)
            return directions_dict

        if N.tile not in FOUR_POINT_TILES:
            directions_dict = shifter(directions)
        else:
            # Directions is a list of lists here, for each strand
            directions_dict = [shifter(strand_directions) for strand_directions in directions]

        if dictionary:
            return directions_dict
        return list(directions_dict.values())

    def walk(self, crossing, direction, pathList=False, tangent=False):
        """Given a crossing and direction, returns crossing reached and orientation demanded.

        W.walk(W.walk(crossing, direction)[0], W.walk(crossing, direction)[1])
        is actually just the identity, returns (crossing, direction) as expected.
        """
        all_crossings = self.findCrossings()
        assert crossing in all_crossings

        M = self.matrixRepresentation
        # CAREFUL: pos_x, pos_y are row, col -- not Cartesian coords!
        (pos_x, pos_y) = crossing
        (prev_x, prev_y) = crossing

        # Move in the indicated direction
        direction_deltas = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1),
        }
        dx, dy = direction_deltas[direction]
        pos_x += dx
        pos_y += dy

        path = [(prev_x, prev_y), (pos_x, pos_y)]

        # Continue walking until reaching another crossing
        while len(Tile(M[pos_x][pos_y]).connectionDirections) == 2:
            accessible_coords = self.shift(pos_x, pos_y)
            accessible_coords.remove((prev_x, prev_y))
            (prev_x, prev_y) = (pos_x, pos_y)
            (pos_x, pos_y) = accessible_coords[0]
            path.append((pos_x, pos_y))

        # Determine incidence direction
        if prev_x < pos_x:
            incidence = 'up'
        elif prev_x > pos_x:
            incidence = 'down'
        elif prev_y < pos_y:
            incidence = 'left'
        else:
            incidence = 'right'

        if pathList:
            return path
        elif tangent:
            return (pos_x, pos_y), opposite(incidence)
        return (pos_x, pos_y), incidence

    def arcList(self):
        """Run walk on each crossing and with condition pathList=True, remove duplicates."""
        # TODO: Create graph based on crossings - each vertex should have degree 4 (4-regular)
        # This is a singular knot representation; orientations indicate knot
        pass

    def strandOf(self, tile, direction=None, direction_tracking=False, verbose=False):
        """Traces a complete strand through the mosaic starting from the given tile.

        Returns empty list if tile is empty (0 tile).
        """
        tile_type = Tile(self.matrixRepresentation[tile[0]][tile[1]]).tile
        if tile_type == 0:
            return []

        if direction is None:
            directions = flatten(Tile(self.matrixRepresentation[tile[0]][tile[1]]).connectionDirections)
            direction = opposite(random.choice(directions))

        start_tile = tile
        start_direction = direction
        path = []

        tile, direction = self.exitPath(start_tile[0], start_tile[1], opposite(start_direction))
        path.append((tile, direction))

        # Keep track of initial direction to handle 2-strand tile starting points
        while not (tile == start_tile and direction == start_direction):
            tile, direction = self.exitPath(tile[0], tile[1], opposite(direction))
            path.append((tile, direction))

        if verbose:
            direction_tracking = True
            for step in path:
                print(f"Went {step[1]} into tile {step[0]}.")

        if direction_tracking:
            return path
        return [tile for tile, direction in path]

    def strandMatrix(self):
        """Returns a matrix showing the number of strands at each position."""
        mosaic_matrix = self.matrixRepresentation
        dim = self.size
        M = matrix(dim, dim, 0)
        for i in range(dim):
            for j in range(dim):
                M[i, j] = Tile(mosaic_matrix[i, j]).numStrands
        return M

    def strandOrientationAt(self, tile, previous_tile):
        """Returns the induced orientation on a tile based on entering from previous_tile."""
        if previous_tile[0] < tile[0]:
            return 'down'
        elif previous_tile[0] > tile[0]:
            return 'up'
        elif previous_tile[1] < tile[1]:
            return 'right'
        return 'left'

    def strands(self):
        """Returns all strands (applies when there are multiple connected components)."""
        strand_list = []
        M = self.matrixRepresentation
        nonempty_tiles = M.nonzero_positions()
        nonvisited_strandMatrix = self.strandMatrix()

        for tile in nonempty_tiles:
            if nonvisited_strandMatrix[tile[0], tile[1]] > 0:
                strand = self.strandOf(tile)
                strand_list.append(strand)
                for strand_tile in strand:
                    nonvisited_strandMatrix[strand_tile[0], strand_tile[1]] -= 1

        # Remove potential duplicates
        for strand in strand_list:
            for other_strand in strand_list:
                if strand != other_strand and len(strand) == len(other_strand):
                    if sorted(strand) == sorted(other_strand):
                        strand_list.remove(other_strand)

        return strand_list

    def numComponents(self):
        """Returns the number of connected components in the mosaic."""
        assert self.isSuitablyConnected()
        return len(self.strands())

    def localFrames(self):
        """Returns the tile above/right (as pairs) for each crossing in the mosaic."""
        crossings = self.findCrossings()
        frames = []
        for crossing in crossings:
            shift_dict = self.shift(crossing[0], crossing[1], True)
            frames.append((shift_dict['up'], shift_dict['right']))
        return frames

    def planarDiagramCode(self):
        """Returns output compatible with SageMath Links package.

        TODO: Implement for https://doc.sagemath.org/html/en/reference/knots/sage/knots/link.html
        """
        pass

    def flip(self):
        """Flips the mosaic upside-down while maintaining tile connections."""
        M = self.matrixRepresentation
        flipped_matrix = M[::-1, :]

        # Map tiles to their upside-down counterparts
        flip_map = {1: 4, 4: 1, 2: 3, 3: 2, 7: 8, 8: 7}

        for i in range(self.size):
            for j in range(self.size):
                tile_val = flipped_matrix[i, j]
                if tile_val in flip_map:
                    flipped_matrix[i, j] = flip_map[tile_val]

        return Mosaic(flipped_matrix)

    def potential_tiles(self, i, j):
        """Returns a list of potential tile insertions based on surrounding connections.

        Checks up-down/left-right open connections around the (i,j)th tile.
        """
        necessary_connections = []
        top_boundary = False
        bottom_boundary = False
        left_boundary = False
        right_boundary = False
        boundary_tile = False

        # Check above
        if i == 0:
            top_boundary = True
        elif self.directions(i - 1, j) == []:
            top_boundary = True
        elif 'down' in self.directions(i - 1, j):
            necessary_connections.append('up')
        else:
            top_boundary = True

        # Check below
        if i == self.size - 1:
            bottom_boundary = True
        elif 'up' in self.directions(i + 1, j):
            necessary_connections.append('down')

        # Check left
        if j == 0:
            left_boundary = True
        elif 'right' in self.directions(i, j - 1):
            necessary_connections.append('left')
        elif self.directions(i, j - 1) == []:
            left_boundary = True
        else:
            left_boundary = True

        # Check right
        if j == self.size - 1:
            right_boundary = True
        elif 'left' in self.directions(i, j + 1):
            necessary_connections.append('right')

        # Find tiles that satisfy necessary connections
        tile_set = [
            tile_num for tile_num in range(11)
            if set(necessary_connections).issubset(set(flatten(Tile(tile_num).connectionDirections)))
        ]

        # Remove tiles that would go into boundaries
        if top_boundary:
            tile_set = [t for t in tile_set if t not in TILES_GOING_UP]
        if bottom_boundary:
            tile_set = [t for t in tile_set if t not in TILES_GOING_DOWN]
        if left_boundary:
            tile_set = [t for t in tile_set if t not in TILES_GOING_LEFT]
        if right_boundary:
            tile_set = [t for t in tile_set if t not in TILES_GOING_RIGHT]

        if top_boundary or bottom_boundary or left_boundary or right_boundary:
            boundary_tile = True

        # If no necessary connections and not on boundary, only allow empty tile
        if necessary_connections == [] and not boundary_tile:
            tile_set = [0]

        return tile_set


def random_mosaic(dimension, suitably_connected=True, num_crossings=-1, num_components=-1, _depth=0):
    """Generates a random mosaic with optional constraints.

    Args:
        dimension: Size of the mosaic (n x n)
        suitably_connected: If True, ensures all tiles connect properly
        num_crossings: Required number of crossings (-1 for any)
        num_components: Required number of components (-1 for any)
    """
    # Prevent infinite recursion
    if _depth > 5000:
        raise ValueError("Could not generate mosaic satisfying constraints after 5000 attempts")

    # Generate base mosaic
    if suitably_connected:
        template = matrix(ZZ, dimension, dimension)
        for i in range(dimension):
            for j in range(dimension):
                template[i, j] = choice(Mosaic(template).potential_tiles(i, j))
        M = Mosaic(template)
    else:
        M = Mosaic(random_matrix(GF(11), dimension, dimension))

    # Check constraints (if given)
    crossing_validity = (num_crossings == -1) or (M.numCrossings() == num_crossings)
    component_validity = (num_components == -1) or (M.numComponents() == num_components)

    if crossing_validity and component_validity:
        return M
    return random_mosaic(dimension, suitably_connected, num_crossings, num_components, _depth + 1)


def tangleConstructor(value, flip=False):
    """Creates a rational tangle mosaic for the given value.

    Args:
        value: The tangle value (oo for infinity, 0, or any integer)
        flip: If True, presents the tangle upside down (necessary for longer tangles)
    """
    if value == oo:
        return Mosaic([[7]])
    if value == 0:
        return Mosaic([[8]])

    def jordan_block_modified(eigenvalue, size, sparse=False, flip=False):
        try:
            size = ZZ(size)
        except TypeError:
            raise TypeError(f"size of block needs to be an integer, not {size}")
        if size < 0:
            raise ValueError(f"size of block must be nonnegative, not {size}")

        block = diagonal_matrix([eigenvalue] * size, sparse=sparse)

        if flip:
            for i in range(size - 1):
                block[i, i + 1] = 1
            for i in range(size):
                if i > 0:
                    block[i, i - 1] = 3
            return block
        else:
            for i in range(size - 1):
                block[i, i + 1] = 4
            for i in range(size):
                if i > 0:
                    block[i, i - 1] = 2
            return block[::-1, :]

    if value > 0:
        return Mosaic(jordan_block_modified(10, value, flip=flip))
    if value < 0:
        return Mosaic(jordan_block_modified(9, -value, flip=flip))


def tangleJoin(tangle_list):
    """Joins two tangles together.

    Note: Currently only supports joining exactly two tangles.
    """
    assert len(tangle_list) == 2

    def tangleConnector(n, m, direction):
        assert direction in ['bottom-right', 'top-left']

        if direction == 'bottom-right':
            row = [6] + [0 for _ in range(m - 1)]
            matrix_data = [row for _ in range(n - 1)] + [[4] + [0 for _ in range(m - 1)]]
            return matrix(matrix_data)
        elif direction == 'top-left':
            row = [0 for _ in range(m)]
            matrix_data = [row for _ in range(n - 1)] + [[2] + [5 for _ in range(m - 1)]]
            return matrix(matrix_data)

    tangle0 = tangleConstructor(tangle_list[0])
    tangle1 = tangleConstructor(tangle_list[1])
    tangle0_flipped = tangleConstructor(tangle_list[0], flip=True)

    block = block_matrix([
        [tangleConnector(tangle1.size, tangle0.size, 'top-left'), tangle1.matrix()],
        [tangle0_flipped.matrix(), tangleConnector(tangle0.size, tangle1.size, 'bottom-right')]
    ])

    return Mosaic(block)


def orientedGaussCode(M):
    """Generates oriented Gauss code for SageMath Link() compatibility.

    Returns the code in the format expected by SageMath's Link class.
    """
    def pick_starting_tile(M):
        """Ensures starting tile is not a crossing/hyperbolic tile."""
        strand_matrix = M.strandMatrix()
        for i in range(M.size):
            for j in range(M.size):
                if strand_matrix[i, j] == 1:
                    return (i, j)

    def crossing_handedness(tile_type, orientation_pair):
        """Determines the handedness (+1 or -1) of a crossing."""
        assert tile_type in CROSSING_TILES
        sorted_pair = sorted(orientation_pair)

        if tile_type == 9:
            if sorted_pair in [["right", "up"], ["down", "left"]]:
                return 1
            if sorted_pair in [["down", "right"], ["left", "up"]]:
                return -1
        elif tile_type == 10:
            if sorted_pair in [["left", "up"], ["down", "right"]]:
                return 1
            if sorted_pair in [["down", "left"], ["right", "up"]]:
                return -1

    def over_under(tile_type, orientation, numeric=False):
        """Determines if the strand goes over or under at a crossing."""
        assert tile_type in CROSSING_TILES

        if tile_type == 9:
            positioning = "under" if orientation in ["up", "down"] else "over"
        elif tile_type == 10:
            positioning = "over" if orientation in ["up", "down"] else "under"

        if numeric:
            return 1 if positioning == "over" else -1
        return positioning

    path = M.strandOf(pick_starting_tile(M))
    path = list(enumerate(path))

    crossings = M.findCrossings()
    appearances = []

    for c in crossings:
        for index, tile in path:
            if tile == c:
                # (tile_type, coord, index, previous_coord)
                appearances.append((M.matrixRepresentation[c], c, index, path[index - 1][1]))

    appearances.sort()

    orientations = []
    for appearance in appearances:
        tile, coord, index, prev_coord = appearance
        entrance = M.strandOrientationAt(coord, prev_coord)
        # (index, tile, coord, strand orientation, over/under)
        orientations.append((index, tile, coord, entrance, over_under(tile, entrance, numeric=True)))

    # Ensure crossings are in correct order
    crossings = list(dict.fromkeys([crossing for index, tile, crossing, orientation, positioning in orientations]))

    crossing_orientations = []
    for c in crossings:
        tile_type = M.matrixRepresentation[c]
        orientation_pair = [entrance for index, tile, crossing, entrance, positioning in orientations if crossing == c]
        crossing_orientations.append(crossing_handedness(tile_type, orientation_pair))

    orientations.sort()

    # Generate the filter (already ordered by traversal)
    code_filter = [
        (crossings.index(crossing) + 1) * positioning
        for index, tile, crossing, entrance, positioning in orientations
    ]

    # Format for Link() compatibility: [[traversal_code], handedness_list]
    return [[code_filter], crossing_orientations]


# Example code:
# M = matrix([[0,2,1,0,0],[2,9,10,1,0],[3,10,9,10,1],[0,3,7,8,4],[0,0,3,4,0]]); W = Mosaic(M);
# W.matrix()
# W.show()
# W.isSuitablyConnected()

# W = Mosaic(M).zoom()
# W.walk((4,7), 'right', pathList = True) # Putting 'True' provides the pathing

# hopf = Mosaic([[0,2,1,0],[2,9,10,1],[3,10,10,4],[0,3,4,0]]); hopfBig = hopf.zoom(); hopfBig.show(10)
# hopfBig.strandOf((4,4),'up')
# hopfBig.strandOf((4,4),'left')
# These are two different strands (knots) in the hopf! Going left/going right at the crossing determines what was taken.

# hopfBig.shift(3,4, dictionary = True) # Returns directions of tiles *connected to*

# W = Mosaic([(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),...])
# W.strandOf((4,4), direction = 'right').count((4,4)) == 2
# This indicates the crossing was visited twice in the walk.
