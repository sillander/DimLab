# Main GUI module, used to draw the maze, the player and the goal.

import geometry as geo

import pygame
import pygame.draw
pygame.init()
pygame.mouse.set_visible(False)



# parameters: these are kind of hard-coded (bad)
SCRW = 320
SCRH = 240
TILE = 40
BOTTOMMARGIN = 10
RIGHTMARGIN  = 10


# constants for the images and fonts (loaded once!)
GOALIMAGE = pygame.image.load("images/star.gif")
SELECTIMAGE = pygame.image.load("images/selection.gif")
VICTFONT = pygame.font.Font('orbitron.ttf', 40)
ROTAFONT = pygame.font.Font('orbitron.ttf', 13)

class GUI:
    "Main GUI class"
    def __init__(self, lab):
        'create a GUI with screen'
        self.lab = lab
        self.xdim = self.lab.size[0]
        self.ydim = self.lab.size[1]
        self.screen = pygame.display.set_mode((SCRW, SCRH))
        self.colorman = ColorMan(self.lab.size)
        # compute square dimensions for the grid
        w, h = self.xdim*TILE, self.ydim*TILE
        self.gridrect = pygame.Rect(SCRW/2-w/2, SCRH/2-h/2, w, h)
        # additional constants and attributes
        self.selectioncolor = [None, None, (255,0,0), (0,255,0), (0,0,255)]
        self.won = False # if True, victory mode
	self.rotation = 0 # current rotation state

    def draw(self, player, selection=2, usefilter=False):
	"""draw the full scene. The following parameters apply:
	* selection is the currently selected color (to display topright);
	* usefilter tells if all the other colors must be filtered."""
        self.screen.fill((0,0,0))
        # first, pre-compute filter
        if not usefilter:
            filter = (1,1,1)
        else:
            filter = [0,0,0]
            filter[selection-2] = 1
        # draw the rectangle
        pygame.draw.rect(self.screen, (255,255,255), self.gridrect, 4)
        for x in range(self.gridrect.left+TILE/2,self.gridrect.right,TILE/2):
            pygame.draw.line(self.screen, (255,255,255), (x,self.gridrect.bottom), (x, self.gridrect.top), 2)
        for y in range(self.gridrect.top+TILE/2,self.gridrect.bottom,TILE/2):
            pygame.draw.line(self.screen, (255,255,255), (self.gridrect.left,y), (self.gridrect.right,y))
        # draw all the tiles
        for x in range(1,self.xdim+1):
            for y in range(1,self.ydim+1):
                # draw tile
                fullpos = self.lab.fulluppermost(x, y, player.pos)
                color = self.colorman.getcolor(fullpos[2:], filter)
                if color != (0,0,0):
                    pygame.draw.rect(self.screen, color, self.gettilepos(x,y))

        # draw player and goal
        # draw the goal at good position (before, so it appears under the player)
        x,y = self.lab.goalpos[0:2]
        atgoalpos = self.lab.fulluppermost(x, y, player.pos)
        # basically, we can draw the goal iff no block is over it, iff fullpos < cpos for dimensions higher than 2,
        # and if the position is the same as the player (that's a lot of conditions, yeah!)
        drawgoal = True
        for dim in range(2, self.lab.ndim):
            if atgoalpos[dim] >= self.lab.goalpos[dim] or self.lab.goalpos[dim] != player.pos[dim]:
                drawgoal = False
                break
        if drawgoal:
            rect = self.gettilepos(x, y).move(TILE/2, TILE/2)
            self.screen.blit(GOALIMAGE,GOALIMAGE.get_rect(centerx=rect.left, centery=rect.top))

        # draw player
        pos = player.pos
        if player.animation:
            pos = player.animation.pos
        pos = self.gettilepos(pos[0], pos[1]).center
        color = self.colorman.getcolor(player.pos[2:], filter)
        if player.animation:
            # partial position feedback
            if player.animation.dim < 2:
                pos = list(pos) # modifiable type
                pos[ player.animation.dim ] += int( player.animation.mov * TILE * player.animation.completion() )
            # partial color feedback
            else:
                color = list(self.colorman.getcolor(player.animation.pos[2:], filter))
                addcomp = self.colorman.incomplete(player.animation.dim, player.animation.completion())
                color[player.animation.dim-2] += addcomp * player.animation.mov # -2 since we need to work in color dimensions
                color[player.animation.dim-2] = min(255, max(0, color[player.animation.dim-2])) # truncature
        # draw the player at correct position, and with good color (other position information, sorta)
        pygame.draw.circle(self.screen, color, pos, TILE/2)
        pygame.draw.circle(self.screen, (255,255,255), pos, TILE/2, 2)

        # finally, draw selection information in top right corner and rotation information bottom right corner
	# selection
        rect = SELECTIMAGE.get_rect(top=0,right=SCRW)
        s = pygame.Surface(size=(TILE, TILE))
        s.fill(self.selectioncolor[selection])
        self.screen.blit(s, rect)
        self.screen.blit(SELECTIMAGE, rect)
	# rotation
	text = "XYRGB" [:self.lab.ndim] # select only interesting letters
	beginning = self.rotation    # variable that detects the offset of marking frame 
	current = self.lab.ndim # special marker to detect begininning of marking frame
	roffset = RIGHTMARGIN # offset to the right for the current letter
	for letter in text[::-1]: # reverse text
		rlet = ROTAFONT.render(letter,1,(255,255,255))
		self.screen.blit(rlet, rlet.get_rect(right=SCRW-roffset,bottom=SCRH-BOTTOMMARGIN))
		roffset += (RIGHTMARGIN+rlet.get_rect().width)
		current -= 1
		if current == beginning:
		    beginning = roffset # marking starts here
	# draw frame (marking) for current XY dimensions
	# I apologize for this code (it was hard to write)
	if self.rotation < self.lab.ndim-1:
		lheight = rlet.get_rect().height
		pygame.draw.rect(self.screen,(255,255,255),
				pygame.Rect(SCRW-beginning+RIGHTMARGIN-4,
					SCRH-BOTTOMMARGIN-lheight-4,
					2*rlet.get_rect().height+RIGHTMARGIN,
					lheight+4), 2)
	else:
		lheight = rlet.get_rect().height
		rect = pygame.Rect(SCRW-beginning+RIGHTMARGIN-2,
				   SCRH-BOTTOMMARGIN-lheight-4,
				   rlet.get_rect().width+4,
				   lheight+4)
		pygame.draw.rect(self.screen, (255,255,255), rect, 2)
		pygame.draw.rect(self.screen, (255,255,255), 
				rect.move( (1-self.lab.ndim)*(rlet.get_rect().width+RIGHTMARGIN)-2,0), 2)

        # super-finally, if you won, make it known
        if self.won:
            text = VICTFONT.render("SUCCESS!", 1, (255,255,0))
            self.screen.blit(text, text.get_rect(center=(SCRW/2, SCRH/2)))
        # flip display
        pygame.display.flip()

    def gettilepos(self, x, y):
        'returns a Rect for the (x,y) position'
        x, y = self.gridrect.move((x-1)*TILE, (y-1)*TILE).topleft
        return pygame.Rect(x, y, TILE, TILE)


    # special animations
    def victory(self):
        self.won = True

    # internal (rotation info propagation)
    def rotate(self, forward=True):
	"Rotate the GUI: must be called as last operation when rotating"
	self.colorman.rotate(forward)
	self.rotation = (self.rotation+1) % self.lab.ndim
	# change x and y limits (note that the maze has already located)
	self.xdim = self.lab.size[0]
	self.ydim = self.lab.size[1]
        # compute square dimensions for the grid
        w, h = self.xdim*TILE, self.ydim*TILE
        self.gridrect = pygame.Rect(SCRW/2-w/2, SCRH/2-h/2, w, h)

class ColorMan:
    'Manages conversion between position in the color dimensions to actual on-screen color'
    def __init__(self, fulllims):
        self.ncdim = len(fulllims)-2 # number of color dimensions
        if self.ncdim > 3:
            raise NotImplemented('Sorry! No more than 5 dimensions are currently supported!')
    # compute the color step for every color (EDIT: every dimension, due to rotation!)
        self.colorstep = [255/clim for clim in fulllims]

    def getcolor(self, colorpos, filter=(1,1,1)):
        'returns the color for the given color position (pos[2:]), using given filter'
        color = [0, 0, 0]
        for i in range(self.ncdim):
            color[i] = self.colorstep[2+i] * colorpos[i] * filter[i]
        return tuple(color)

    def incomplete(self, dim, fraction):
        'returns the increment in color due to a given motion in direction dim, of current fraction'
        return int(fraction*self.colorstep[dim])

    # experimental
    def rotate(self, forward=True):
	"rotate the various vectors inside the color manager"
	self.colorstep = geo.rotate1(self.colorstep, forward)
