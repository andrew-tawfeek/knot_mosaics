# An implementation of mosaic theory into SageMath.

class Tile():
    def __init__(self,N):
        self.tile = N
        self.orientation = []
        if (N == 0):
            self.numConnectionPoints = 0
            self.connectionDirections = []
        if (N in [1,2,3,4,5,6]):
            self.numConnectionPoints = 2
            if (N==1):
                self.connectionDirections = ['left','down']
            if (N==2):
                self.connectionDirections = ['right','down']
            if (N==3):
                self.connectionDirections = ['up','right']
            if (N==4):
                self.connectionDirections = ['left','up']
            if (N==5):
                self.connectionDirections = ['left','right']
            if (N==6):
                self.connectionDirections = ['up','down']
        if (N in [7,8,9,10]):
            self.numConnectionPoints = 4
            self.connectionDirections = ['up','down','left','right']
    def show(self, resolution = 5):
        T_0 = line([(0,0),(1,0)], axes = False, xmin = 0, xmax = 1, ymin = 0, ymax = 1, frame = True, ticks=[[],[]], thickness=0).plot()
        T_1 = arc((0,0), 1, sector=(0,pi/2), axes = False, xmin = 0, xmax = 2, ymin = 0, ymax = 2, frame = True, ticks=[[],[]], thickness=resolution).plot()
        T_2 = arc((0,0), 1, sector=(0,pi), axes = False, xmin = -2, xmax = 0, ymin = 0, ymax = 2, frame = True, ticks=[[],[]], thickness=resolution).plot()
        T_3 = arc((0,0), 1, sector=(pi,2*pi), axes = False, xmin = -2, xmax = 0, ymin = -2, ymax = 0, frame = True, ticks=[[],[]], thickness=resolution).plot()
        T_4 = arc((0,0), 1, sector=(pi,2*pi), axes = False, xmin = 0, xmax = 2, ymin = -2, ymax = 0, frame = True, ticks=[[],[]], thickness=resolution).plot()
        T_5 = line([(0,1), (1,1)], axes = False, xmin = 0, xmax = 1, ymin = 0, ymax = 2, frame = True, ticks=[[],[]], thickness=resolution).plot()
        T_6 = line([(1,0), (1,1)], axes = False, xmin = 0, xmax = 2, ymin = 0, ymax = 1, frame = True, ticks=[[],[]], thickness=resolution).plot()
        T_7 = T_1 + arc((2,2), 1, sector=(pi,2*pi), axes = False, xmin = 0, xmax = 2, ymin = 0, ymax = 2, frame = True, ticks=[[],[]], thickness=resolution).plot()
        T_8 = arc((0,2), 1, sector=(2*pi/3,2*pi), axes = False, xmin = 0, xmax = 2, ymin = 0, ymax = 2, frame = True, ticks=[[],[]], thickness=resolution).plot() + arc((2,0), 1, sector=(pi,pi/2), axes = False, xmin = 0, xmax = 2, ymin = 0, ymax = 2, frame = True, ticks=[[],[]], thickness=resolution).plot()
        T_9 = line([(0,1), (2,1)], axes = False, xmin = 0, xmax = 2, ymin = 0, ymax = 2, frame = True, ticks=[[],[]], thickness=resolution).plot() + line([(1,0), (1,.6)], axes = False, xmin = 0, xmax = 2, ymin = 0, ymax = 2, frame = True, ticks=[[],[]], thickness=resolution).plot() + line([(1,1.4), (1,2)], axes = False, xmin = 0, xmax = 2, ymin = 0, ymax = 2, frame = True, ticks=[[],[]], thickness=resolution).plot()
        T_10 = line([(1,2), (1,0)], axes = False, xmin = 0, xmax = 2, ymin = 0, ymax = 2, frame = True, ticks=[[],[]], thickness=resolution).plot() + line([(0,1), (.6,1)], axes = False, xmin = 0, xmax = 2, ymin = 0, ymax = 2, frame = True, ticks=[[],[]], thickness=resolution).plot() + line([(1.4,1), (2,1)], axes = False, xmin = 0, xmax = 2, ymin = 0, ymax = 2, frame = True, ticks=[[],[]], thickness=resolution).plot()

        if (self.tile==0):
            return T_0
        if (self.tile==1):
            return T_1
        if (self.tile==2):
            return T_2
        if (self.tile==3):
            return T_3
        if (self.tile==4):
            return T_4
        if (self.tile==5):
            return T_5
        if (self.tile==6):
            return T_6
        if (self.tile==7):
            return T_7
        if (self.tile==8):
            return T_8
        if (self.tile==9):
            return T_9
        if (self.tile==10):
            return T_10

    def isGoing(self, direction):
        # e.g. Tile(6).isGoing('up') returns True but Tile(6).isGoing('left') returns False
        # This is good for checking suitable connectivity later
        return direction in self.connectionDirections
    def zoom(self, onlyUpDown = False):
        # Every tile becomes 3x3 matrix
        # TODO: Later, iterate this with an input "amount"
        N = self.tile
        if (N==0):
            return [[0,0,0],[0,0,0],[0,0,0]]
        if (N==1):
            return [[0,0,0],[5,1,0],[0,6,0]]
        if (N==2):
            return [[0,0,0],[0,2,5],[0,6,0]]
        if (N==3):
            return [[0,6,0],[0,3,5],[0,0,0]]
        if (N==4):
            return [[0,6,0],[5,4,0],[0,0,0]]
        if (N==5):
            return [[0,0,0],[5,5,5],[0,0,0]]
        if (N==6):
            return [[0,6,0],[0,6,0],[0,6,0]]
        if (N==7):
            return [[0,3,1],[1,0,3],[3,1,0]]
        if (N==8):
            return [[2,4,0],[4,0,2],[0,2,4]]
        if (N==9):
            if onlyUpDown == True: # twists to center a 10-tile instead
                return [[2,8,1],[7,10,7],[3,8,4]]
            return [[0,6,0],[5,9,5],[0,6,0]]
        if (N==10):
            return [[0,6,0],[5,10,5],[0,6,0]]
    def orient(self, direction):
        # Assigns an orientation to a tile
        assert direction in self.connectionDirections #returns error if orientation not possible
        self.orientation = self.orientation + [direction]

class Mosaic():
    def __init__(self,mosaic_matrix): #Takes input matrix or list of lists (array)
        self.matrixRepresentation = matrix(mosaic_matrix)
        self.size = len(self.matrixRepresentation.rows())
        #attributes/properties of object go here
    def __repr__(self):
        # This representation is announced upon construction. Comment out later, here for testing.
        return f"Mosaic of dimension {self.size}."
    def show(self, resolution = 5):
        # Letting W = Mosaic(M) for a matrix M then running W.show() outputs a graphic for the mosaic
        return graphics_array([[x.show() for x in row] for row in [list(map(Tile,row)) for row in [list(x) for x in self.matrixRepresentation]]]).show(figsize=[resolution, resolution])
    def matrix(self):
        # Letting W = Mosaic(M) for a matrix M, and doing W.matrix() returns the matrix representation of the mosaic
        return self.matrixRepresentation
    def directions(self,i,j):
        # Letting W = Mosaic(M) for a matrix M, doing W.directions(i,j) returns the connection points
        # of the (i,j)th tile, where (0,0) is the tile in the upper-left (matrix notation, indexed at 0)
        M = self.matrixRepresentation
        directions = Tile(M[i][j]).connectionDirections
        return directions
    def isSuitablyConnected(self):
        # As above, for W = Mosaic(M), doing W.isSuitablyConnected() returns either True/False based on connectivity
        M = self.matrixRepresentation
        for i in range(self.size):
            for j in range(self.size):
                if Tile(M[i][j]).isGoing('up'):
                    if i == 0:
                        return False
                    elif not Tile(M[i-1][j]).isGoing('down'):
                        return False
                if Tile(M[i][j]).isGoing('left'):
                    if j == 0:
                        return False
                    elif not Tile(M[i][j-1]).isGoing('right'):
                        return False
                if Tile(M[i][j]).isGoing('right'):
                    if j == self.size-1:
                        return False
                    elif not Tile(M[i][j+1]).isGoing('left'):
                        return False
                if Tile(M[i][j]).isGoing('down'):
                    if i == self.size-1:
                        return False
                    elif not Tile(M[i+1][j]).isGoing('up'):
                        return False
        return True

    # If onlyUpDown = True, then all 9 tiles are replaced by twisted 10 tiles (isotopy equivalent)
    def zoom(self, onlyUpDown = False):
        # Zooms by 3x, replaces each tile by a 3x3 isotopy equivalent tile
        # Usage is W.zoom() fro W = Mosaic(M)
        M = self.matrixRepresentation
        M_tensored = [[Tile(x).zoom(onlyUpDown) for x in row] for row in [list(x) for x in list(M)]]
        A = [] # The below code unwraps inner 3x3 subtiles
        for n in range(len(M_tensored)*3):
            A = A + [[x[n%3] for x in M_tensored[floor(n/3)]]] #Euclidean division, n = floor(n/3)*3 + n%3
        B = [] # The below code unwraps inner 1x3 subtiles
        for row in A:
            tupe = []
            for tuple in row:
                tupe = tupe + tuple
            B = B + [tupe]
        return Mosaic(B)
    def findCrossings(self):
        # Returns a list of the coordinates (i,j) in the matrix of crossings, i.e. 9/10 tiles
        M = self.matrixRepresentation
        n = self.size
        M_rows = [list(x) for x in M.rows()]
        crossing_coord = []
        for i in range(n):
            row_crossings = [j for j, x in enumerate(M_rows[i]) if x == 9 or x == 10]
            crossing_coord += [(i,j) for j in row_crossings]
        return crossing_coord
    def numCrossings(self):
        return len(self.findCrossings())
        
    def shift(self,i,j, dictionary = False):
        # Setting 'dictionary = True' allows a dictionary return of tile directions
        assert self.isSuitablyConnected() == True # prevents indexing issues
        M = self.matrixRepresentation
        directions = Tile(M[i][j]).connectionDirections
        directions_dict = dict()
        
        if 'up' in directions:
            directions_dict['up'] = (i-1,j)
        if 'down' in directions:
            directions_dict['down'] = (i+1,j)
        if 'left' in directions:
            directions_dict['left'] = (i,j-1)
        if 'right' in directions:
            directions_dict['right'] = (i,j+1)

        if dictionary == True:
            return directions_dict
        else:
            return list(directions_dict.values())

    def walk(self, crossing, direction, pathList = False, tangent = False):
        #assert #NEED TO ENSURE NO HYPERBOLIC TILES
        # Given a crossing and direction (up/down/left/right), returns crossing reached and orientation demanded
        # W.walk(W.walk(crossing, direction)[0],W.walk(crossing, direction)[1]) #is actually just the identity, returns crossing, direction, as expected
        all_crossings = self.findCrossings() # list of crossings (i,j)
        assert crossing in all_crossings # error prevention
        M = self.matrixRepresentation
        (pos_x, pos_y) = crossing # CAREFUL: pos_x, pos_y are row, col -- not Cartesian coords!
        (prev_x, prev_y) = crossing
        # Start at the indicated crossing tile (i,j), goes direction
        
        if direction == 'up':
            pos_x -= 1
        if direction == 'down':
            pos_x += 1
        if direction == 'left':
            pos_y -= 1
        if direction == 'right':
            pos_y += 1

        path = [(prev_x, prev_y), (pos_x, pos_y)]
        # Continue walking until reaching another crossing
        while len(Tile(M[pos_x][pos_y]).connectionDirections) == 2: # If it's a two way street, keep going
            accessible_coords = self.shift(pos_x,pos_y)
            accessible_coords.remove((prev_x, prev_y)) # only one possibility after this
            (prev_x, prev_y) = (pos_x, pos_y)
            (pos_x, pos_y) = accessible_coords[0]
            path += [(pos_x, pos_y)]

        if prev_x < pos_x: # i.e. entered from higher tile
            incidence = 'up'
        if prev_x > pos_x:
            incidence = 'down'
        if prev_y < pos_y:
            incidence = 'left'
        if prev_y > pos_y:
            incidence = 'right'
        
        if pathList == True:
            return path
        elif tangent == True:
            return (pos_x, pos_y), opposite(incidence)
        else:
            return (pos_x, pos_y), incidence
    def arcList(self):
        # run walk on each crossing and with condition pathList = True
        # remove duplicates in nice manner
        pass
            
        # TODO: create graph based on crossing! each vertex should have degree 4, i.e. 4-regular!
        # This is a singular knot representation, nearly, but orientations indicate knot
        # Perhaps for  fun output a directed graph of this sort for visualization.

    def strandOf(self, crossing, direction = 'up'):
        # Returns strand of a single provided crossing.
        # Orientation at crossign defaults to 'up' unless otherwise indicated.
        crossings = self.findCrossings()
        assert crossing in crossings
        
        initial = crossing
        initial_direction = direction
        strandPath = self.walk(initial, direction, pathList = True)
        position, direction = self.walk(initial, direction, tangent = True)

        while position != initial: 
            strandPath += self.walk(position, direction, pathList = True)[1:] # Drops off repeated start (time = 0)
            position, direction = self.walk(position, direction, tangent = True)
            if position == initial:  # This prevent stopping the while loop if initial crossing approached orthogonally
                if strandPath[-2] != self.shift(initial[0],initial[1],dictionary = True)[opposite(initial_direction)]:
                    strandPath += self.walk(position, direction, pathList = True)[1:]
                    position, direction = self.walk(position, direction, tangent = True)
                else:
                    return strandPath[:-1] # Used to remove duplicate starting/ending position

    def localFrames(self):
        # Returns the tile above/below (as a pair) each crossing in the mosaic
        return [(self.shift(crossing[0],crossing[1],True)['up'], self.shift(crossing[0],crossing[1],True)['right']) for crossing in self.findCrossings()] 
    
    def strands(self):
        # Returns all strands (applies only when multiple connected components).
        crossings = self.findCrossings() #every crossing should visited twice...
        
        
        pass #TOOD.
        
        # check missed crossings after... for x in all_crossings, if x not in strand_list... add to list corresp. to new knot
        # WARNING: does this tell you when two knots are linked? what does this do for hopf?
        # Perhaps could be used primarily for orienting, i.e. Sage Links compatibility

    def numComponents(self):
        assert self.isSuitablyConnected() == True #knot has to be connected up
        # TODO: it does a full walk, checks off each crossing that appears, and etc.
        # This is not sufficient -- e.g. things that don't have crossings



        pass

    def planarDiagramCode(self):
        #TODO: This output is what's needed for compatibility with Links package in Sage
        # https://doc.sagemath.org/html/en/reference/knots/sage/knots/link.html
        pass

    def flip(self):
        # Flips the mosaic upside-down while maintaining tile connections
        M = self.matrixRepresentation
        flipped_matrix = M[::-1,:] # flips entire matrix upside down
        for i in range(self.size): # all this fixes the fact that tiles need to be interchanged with their upside-down counterparts
            for j in range(self.size):
                if flipped_matrix[i,j] == 1:
                    flipped_matrix[i,j] = 4
                elif flipped_matrix[i,j] == 2:
                    flipped_matrix[i,j] = 3
                elif flipped_matrix[i,j] == 3:
                    flipped_matrix[i,j] = 2
                elif flipped_matrix[i,j] == 4:
                    flipped_matrix[i,j] = 1
                elif flipped_matrix[i,j] == 7:
                    flipped_matrix[i,j] = 8
                elif flipped_matrix[i,j] == 8:
                    flipped_matrix[i,j] = 7
        return Mosaic(flipped_matrix)

    def potential_tiles(self, i, j):
    # outputs a LIST of potential tile insertions based on the up-down/left-right open connections
    # around the (i,j)th tile

        necessary_connections = []
        
        top_boundary = False
        bottom_boundary = False
        left_boundary = False
        right_boundary = False

        boundary_tile = False

        #above
        if i == 0: # above is boundary
            top_boundary = True # it isn't allowed to go up in this case
        elif self.directions(i-1, j) == []: # if the tile above is a blank tile, (i,j) cannot go up
            top_boundary = True
        elif 'down' in self.directions(i-1, j): # if the tile above contains a downward connection, (i,j) goes up
            necessary_connections += ['up']
        else:
            top_boundary = True

        if i == self.size-1: #below is the mosaic boundary
            bottom_boundary = True
        elif 'up' in self.directions(i+1, j): # if the tile below contains an upward connection
            necessary_connections += ['down']

        if j == 0: # left is boundary
            left_boundary = True
        elif 'right' in self.directions(i, j-1):
            necessary_connections += ['left']
        elif self.directions(i, j-1) == []: # if the tile to the left is a blank tile, (i,j) cannot go left
            left_boundary = True
        else:
            left_boundary = True

        if j == self.size-1: # right is boundary
            right_boundary = True
        elif 'left' in self.directions(i, j+1): 
            necessary_connections += ['right']
        
        #return necessary_connections
        tile_set =  [tile_num for tile_num in range(0,11) if set(necessary_connections).issubset(set(Tile(tile_num).connectionDirections))]

        if top_boundary == True:
            tile_set = [tile for tile in tile_set if tile != 3 and tile != 4 and tile != 6 and tile != 7 and tile != 8 and tile != 9 and tile != 10] #removes tiles that go up

        if bottom_boundary == True:
            tile_set = [tile for tile in tile_set if tile != 1 and tile != 2 and tile != 6 and tile != 7 and tile != 8 and tile != 9 and tile != 10]

        if left_boundary == True:
            tile_set = [tile for tile in tile_set if tile != 1 and tile != 4 and tile != 5 and tile != 7 and tile != 8 and tile != 9 and tile != 10]
        
        if right_boundary == True:
            tile_set = [tile for tile in tile_set if tile != 2 and tile != 3 and tile != 5 and tile != 7 and tile != 8 and tile != 9 and tile != 10]
        
        if top_boundary == True or bottom_boundary == True or left_boundary == True or right_boundary == True:
            boundary_tile = True

        if necessary_connections == [] and boundary_tile == False:
            tile_set = [0]

        return tile_set

import random

def random_mosaic(dimension, suitably_connected = True, num_crossings = -1):
    if num_crossings != -1:
        M = random_mosaic(dimension, suitably_connected = suitably_connected)
        while len(M.findCrossings()) != num_crossings:
            M = random_mosaic(dimension, suitably_connected = suitably_connected)
        return M

    if suitably_connected == False: # I have no clue why you would want this, but here you go
        return Mosaic(random_matrix(GF(11),dimension,dimension))

    elif suitably_connected == True:
        template = matrix(ZZ,dimension,dimension)
        for i in range(dimension):
            for j in range(dimension):
                template[i,j] = choice(Mosaic(template).potential_tiles(i,j))
        return Mosaic(template)








    # This code is embarassing, but if it's stupid and it works it's not stupid.
    # Good luck ever getting this to work for high dimension! Technically, you need luck. Like, a lot of it.
#    connect_check = False
#    while connect_check == False:
#        M = Mosaic(random_matrix(GF(11),dimension,dimension))
#        connect_check = M.isSuitablyConnected()
#    return M








def opposite(direction):
    assert direction in ['up','down','left','right']
    if direction == 'up':
        return 'down'
    if direction == 'down':
        return 'up'
    if direction == 'left':
        return 'right'
    if direction == 'right':
        return 'left'







    
# flip presents it as upside down, neccesary for longer tangles
def tangleConstructor(value, flip = False): #perhaps just make this a class
    if value == oo:
        return Mosaic([[7]])
    if value == 0:
        return Mosaic([[8]])

    def jordan_block_modified(eigenvalue, size, sparse=False, flip = False):
        try:
            size = ZZ(size)
        except TypeError:
            msg = "size of block needs to be an integer, not {0}"
            raise TypeError(msg.format(size))
        if size < 0:
            msg = "size of block must be nonnegative, not {0}"
            raise ValueError(msg.format(size))
        block = diagonal_matrix([eigenvalue] * size, sparse=sparse)
        if flip == True:
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
            return block[::-1,:]

    if value > 0:
        return Mosaic(jordan_block_modified(10, value, flip = flip))
    if value < 0:
        return Mosaic(jordan_block_modified(9, -value, flip = flip))







    
# Unfinished        
#def generalizedConnector(dim1, dim2, endpoint1, endpoint2, boundary1, boundary2):
    # Creates a connecting strand from endpoint1 to endpoint2 contained in a dim1 x dim2 mosaic
    # Endpoints need to be a tuple on the boundary of the mosaic
#    assert boundary1 in ['top','bottom','left','right']
#    assert boundary2 in ['top','bottom','left','right']

#    template = matrix(ZZ,dim1,dim2)
    
    # it is irrelevant where you begin
#    y1,x1 = endpoint1
#    y2,x2 = endpoint2

#    if y1 == y2:
#        for x in range(min(x1,x2), max(x1,x2)+1):
#            template[y1,x] = 5 # horizontal strand
    
#    elif y1 < y2:
#        #the first tile is higher than the second in the mosaic
#            template[y1,x1] = 1 # down right


#    if x1 == x2:
#        for y in range(min(y1,y2), max(y1,y2)+1):
#           template[y,x1] = 6 # vertical strand

  

#    return Mosaic(template)







    
# takes in mosaics, TODO -- NEED TO ALLOW FULL LISTS LATER
def tangleJoin(tangle_list):
    #other one is transpose? need to write a mosaic "rotate/flip/refelect" method, maybe not now
    #issue is upon reflecting, tiles need to be flipped to their correct orientation
    #for now lets settle with a "flip" optional argument

    assert len(tangle_list) == 2 # only two tangles can be joined at the moment


    def tangleConnector(n,m, direction): # need to generalize for arb. dimension and specificying what connects where
        assert direction in ['bottom-right', 'top-left']
        if direction == 'bottom-right':
            row = [6] + [0 for i in range(m-1)]
            matrix_data = [row for i in range(n-1)] + [[4] + [0 for i in range(m-1)]]
            return matrix(matrix_data)
        elif direction == 'top-left':
            row = [0 for i in range(m)]
            matrix_data = [row for i in range(n-1)] + [[2] + [5 for i in range(m-1)]]
            return matrix(matrix_data)

    inner_tangle = tangleConstructor(tangle_list[0])
     
    for i in range(len(tangle_list)):
        block = block_matrix([[tangleConnector(tangleConstructor(tangle_list[1]).size,tangleConstructor(tangle_list[0]).size, 'top-left'),tangleConstructor(tangle_list[1]).matrix()],
                            [tangleConstructor(tangle_list[0], flip = True).matrix(),tangleConnector(tangleConstructor(tangle_list[0]).size,tangleConstructor(tangle_list[1]).size, 'bottom-right')]])

    return Mosaic(block)







#Were this to be implemented into a GNN...

#Nodes = mosaic tiles (with tile type as features)
#Edges = connections between adjacent tiles
#Graph structure captures the topological information




#class mosaics():
#    def __init__(self):
        # Refer to graphs Sage package...
        # https://www.geneseo.edu/knotmosaics/knot-table
        # https://github.com/andrew-tawfeek/knot-mosaics/blob/master/README.md
        # https://github.com/amheap/knot-mosaics/blob/master/pythonFiles/draw_knots.py

###############################

        
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

#hopfBig.shift(3,4, dictionary = True) # Returns directions of tiles *connected too*

# W = Mosaic([(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 2, 5, 5, 1, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 6, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 6, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0),(0, 2, 5, 5, 9, 5, 5, 10, 5, 5, 1, 0, 0, 0, 0),(0, 6, 0, 0, 6, 0, 0, 6, 0, 0, 6, 0, 0, 0, 0),(0, 6, 0, 0, 6, 0, 0, 3, 1, 0, 6, 0, 0, 0, 0),(0, 3, 5, 5, 10, 5, 1, 0, 3, 5, 10, 5, 5, 1, 0),(0, 0, 0, 0, 6, 0, 3, 1, 0, 0, 6, 0, 0, 6, 0),(0, 0, 0, 0, 6, 0, 0, 6, 0, 2, 4, 0, 0, 6, 0),(0, 0, 0, 0, 3, 5, 5, 10, 5, 4, 0, 2, 5, 4, 0),(0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 2, 4, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 6, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 3, 5, 5, 4, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)])
# W.strandOf((4,4), direction = 'right').count((4,4)) == 2
# This indicates the crossing was visited twice in the walk. Orthogonality check is done in the code during second pass-through.