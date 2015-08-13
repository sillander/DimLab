# In this module, we define the basic n-D labyrinth structure.
# This file does not strictly impose a maximal number of dimensions, but stick to max 5.
# Also, it offers file parsing for labyrinth files.

# FORMAT OF A LABYRINTH CLASS
# A Labyrinth is described in terms of:
#  (1) the number (>2) of dimensions it uses, and its size in these dimensions.
#  (2) XY-grids, one for each multiplet of color dimensions in the size of the labyrinth (color dimension = not XY dimension)
# first line (header): "LAB ", then size of the lab in the various dimensions, separated by spaces.
# body:
# lines starting with "floor ", then the position of the 2D grid in color dimensions (integers separated by spaces)
# THEN: lines representing the grid. X and B to represent a block at the XY + color position, while * or G represents
#  the goal (there must be 1! goal position per file). Empty places can be filled with any character
# /!\ the number of lines cannot exceed the defined size in the Y dimension. Cases over the size in X dimension will be ignored.
# For examples, check the files in the labs folder, or the simplelab.txt file.


import geometry as geo

class Labyrinth:
    "Labyrinth class: describes a labyrinth in n dimensions"
    def __init__(self, size, blocks, goalpos):
        """Create a labyrinth of len(size) dimensions, with given blocks (as a list).
        The blocks list must be a list of tuples the same length as size, and such that
         1 <= blocks[i][j] <= size[j]  for all valid i, and 0 <= j < length(size)"""
        self.size = size
        self.ndim = len(self.size)
        self.blocks = {}
        for block in blocks:
            self.blocks[ tuple(block) ] = True
        self.goalpos = goalpos
        # check integrity
        for block in blocks:
            if len(block) != len(size):
                raise Exception('Wrong block size! (at block '+str(block)+')')
            if not self.iswithin(block):
                raise Exception('Block not within labyrinth! (at block '+str(block)+')')
        if not self.iswithin(goalpos):
            raise Exception('Goal is not within labyrinth!')
        if not self.isfree(goalpos):
            raise Exception('Block at goal position!')

    def isfree(self, pos):
        'determines if the n-dim position pos is free'
        return (not self.blocks.get(tuple(pos), False)) and self.iswithin(pos)

    def iswithin(self, pos):
        'determines if the position pos is within the labyrinth (not outside borders)'
        for i in range(self.ndim):
            if pos[i]<1 or pos[i]>self.size[i]:
                return False
        return True

    def uppermost1d(self, x, y, pos, dimension):
        """returns the value in given dimension (>= 2) of the uppermost tile to display at (x,y),
         given the player is at n-pos pos.
         Please note that 0 is a valid return value for this! (it is the color of the ground: black)"""
        # get real tile position
        tilepos = [x, y] + list(pos[2:])
        if self.isfree(tilepos):
            # in this case, find upmost lower tile that is free
            for upmost in range(tilepos[dimension]-1, 0, -1):
                tilepos[dimension] = upmost
                if not self.isfree(tilepos):
                    return upmost
            return 0 # not found
        else:
            # in this case, find upmost occupied tile in the pile
            for upmost in range(tilepos[dimension]+1, self.size[dimension]+1, 1):
                tilepos[dimension] = upmost
                if self.isfree(tilepos):
                    return upmost-1
            return self.size[dimension]

    def fulluppermost(self, x, y, pos):
        'returns the full position of the uppermost tile at given position'
        uppermost = list(self.size)
        uppermost[0:2] = [x,y]
        for dim in range(2,self.ndim):
            uppermost[dim] = self.uppermost1d(x, y, pos, dim)
        return uppermost


    # as of now, experimental
    def rotate(self,forward=True):
	"rotate this maze. If forward, the XY dimensions move forward in RGB. Else, backward."
	# modify blocks and size
	rotate1 = lambda block: geo.rotate1(block, forward)
	newblocks = {}
	for (block, value) in self.blocks.items():
		newblocks[ rotate1(block) ] = value
	self.blocks = newblocks
	self.size = rotate1(self.size)
	self.goalpos = rotate1(self.goalpos)

    @staticmethod
    def fromfile(filename):
        with open(filename, 'r') as ff:
            # read header
            header = ff.readline().split(' ')
            if header[0].lower() != 'lab':
                raise SyntaxError('Not a labyrinth file!')
            sizes = [int(size.strip('\n')) for size in header[1:]]
            if len(sizes)<2:
                raise Exception('Not enough dimensions! (1 given)')
            # now, read by squares
            blocks = []
            done = False
            goalpos = None
            # iteration specific variables
            cpos = None
            y = 1
            for line in ff.readlines(): # ignore first line
                line = line.strip(' \n').lower()
                if line.startswith('#') or not line:
                    continue
                if line == 'end':
                    break
                if line.startswith('floor '):
                    # new floor definition
                    cpos = [int(d) for d in line[6:].split(' ')]
                    y = 1 # reset line in floor
                elif cpos:
                    # we are now defining one line (given y) of the floor
                    if y > sizes[1]:
                        raise Exception('Invalid vertical position: '+str(y)+' (did you include too many lines?)')
                    for x in range(len(line)):
                        if line[x] in ['x', 'b']:
                            blocks.append(tuple( [x+1, y] + cpos ))
                        elif line[x] in ['g', '*']:
                            if goalpos:
                                raise Exception('Goalpos already defined! (previous: '+str(goalpos)+')')
                            goalpos = tuple([x+1,y] + cpos)
                    y += 1 # next line
                else:
                    raise Exception('Invalid line: "'+line+'"')
            # now, we've got the data: create a Labyrinth
            return Labyrinth(sizes, blocks, goalpos)



# Default: simple 3D lab (3x3x3)
Default = Labyrinth.fromfile('simplelab.txt')#Labyrinth((3,3,3,2), [(2,1,1,1), (2,2,1,1), (2,2,2,1), (2,3,3,1), (1,1,1,2), (2,3,1,1)],  (3,3,1,1))
