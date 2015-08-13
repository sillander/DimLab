# This class manages the game, that is, moving around dimensions in the labyrinth.

import GUI
import Labyrinth
import geometry as geo

import pygame
import pygame.time
import sys

FPS = 60 # nice and smooth babe

class Animation:
    """very simple animation class.
    Animations are used to determine if the player is free to move or not,
    and if not to compute the progress (0<=p<1) of the current motion, for graphical purposes."""
    def __init__(self, initialpos, motion):
	"create an animation with given initial position and motion"
        self.i = 0     # current frame
        self.n = FPS/3 # maximum number of frames
        self.dim, self.mov = motion
        self.pos = initialpos

    def iterate(self):
	"""computes state after one iteration, and returns the animation to use afterwards.
	Basically, this returns either self or None."""
        self.i+=1
        if self.i >= self.n:
            return None
        return self

    def completion(self):
        'returns completion (between 0 and 1)'
        return float(self.i)/self.n


class Player:
    """Player class: handles position, motion and animation. 
    This is mostly a placeholder to keep these three together.
    Not that this class does not have a move procedure, and relies on modification
    of its internal arguments to update its position."""
    def __init__(self, position):
        self.pos = position   # sort of a public variable
	self.motion = None    # current state of motion of the Player (direction and amplitude of motion)
	self.animation = None # animation state (determines if OK to move)

    # self-explanatory:
    def get_motion(self):
        return self.motion
    def set_motion(self, dimension, move):
        self.motion = (dimension, move)
    def stop(self):
        self.motion = None

    # main player method
    def animate(self):
	"""iterate on the player's state during a frame: iterate on the animation if any;
	if none and there is an existing motion, return the next motion to apply."""
        if self.animation:
            self.animation = self.animation.iterate()
            return None
        # if no animation, not currently moving
        if self.motion:
            self.animation = Animation(list(self.pos), self.motion)
            return self.motion
        # else
        return None


class MotionManager:
    """Motion Manager: handles the various keyboard events related to motion,
    and color choice and filtering. The default is keyset is for the GCW-Zero."""
    def __init__(self, player, ndim):
        self.player = player
	# Default is the GCW-Zero Standard
        # classic 2D motion
        self.motions = {pygame.K_LEFT:(0,-1),
                        pygame.K_RIGHT:(0,1),
                        pygame.K_UP:(1,-1),
                        pygame.K_DOWN:(1,1)}
        # color dimensions motion
        self.cmotions = {pygame.K_TAB:-1,
                         pygame.K_BACKSPACE:+1}
        # color switching button
        self.colorswitch = {pygame.K_LCTRL:+1,   # A
                            pygame.K_LALT:-1}    # B
        # filter switching button
        self.filterswitch = pygame.K_SPACE # X
	# rotation button
	self.rotatebutton = pygame.K_LSHIFT # Y 
        self.ndim = ndim
        self.cdim = 2
	self.torotate = False
        self.filtering = False

    def keyup(self, key):
        'a key was lifted (cancel current motion, if key is current motion)'
        motion = self.motions.get(key, None)
        if (not motion) and self.ndim>2: # check for color motion
            incr = self.cmotions.get(key, None)
            if incr:
                motion = (self.cdim, incr)
        # if a motion was specified, check if actual motion change
        if motion:
            if motion == self.player.get_motion():
                self.player.stop()
                return
        # else, check if filter button
        if key == self.filterswitch:
            self.filtering = False

    def keydown(self, key):
        'a key was pressed (change motion)'
        motion = self.motions.get(key, None)
        if (not motion) and self.ndim>2:
            incr = self.cmotions.get(key, None)
            if incr:
                motion = (self.cdim, incr)
        if motion:
            self.player.set_motion(*motion)
            return
        if self.ndim < 3:
            return # nothing much to do here (no color change possible!)
        # else: (if not a motion key)
        cchange = self.colorswitch.get(key, None)
        if cchange:
            self.cdim = self.cdim + cchange
            if self.cdim < 2:
                self.cdim = self.ndim-1
            elif self.cdim >= self.ndim:
                self.cdim = 2
            return
        # else, check if filter button
        if key == self.filterswitch:
            self.filtering = True
	# else, check the rotation button
	if key == self.rotatebutton:
	    self.torotate = True

class GCWZeroMotionManager(MotionManager):
    """Specific Motion Manager designed for the GCW-Zero."""

class AzertyMotionManager(MotionManager):
    """Specific Motion Manager whose keyset is for the AZERTY keyboard layout."""
    def __init__(self, player, ndim):
        MotionManager.__init__(self, player, ndim)
	# Note that, as a choice, we left the arrows and spacebar as set for GCW-Zero.
	# For the color dimensions, we will use the AZES keys (seems more logical)
	# color dimensions motion
        self.cmotions = {pygame.K_s:-1,
                         pygame.K_z:+1}
        # color switching button
        self.colorswitch = {pygame.K_e:+1,
                            pygame.K_a:-1}


class CustomMotionManager(MotionManager):
    """TODO: define this correctly using files and all."""





class Game:
    """Main Maze playing class. Manages animation and display of the maze.
    The settings control the keyset that is used."""
    def __init__(self, lab, settings={}):
        self.lab = lab
        self.gui = GUI.GUI(lab) # will display the maze
        # create player at initial pos (1,1,1,1,1,...)
        self.player = Player( [1] * lab.ndim )
	if settings.get("UseAzerty"):
	    self.motman = AzertyMotionManager(self.player, lab.ndim)
	else:
            self.motman = MotionManager(self.player, lab.ndim)
        self.toanimate = True
        self.running = False

    def start(self):
        'start this game'
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            # before all, check if the player has won:
            if not self.player.animation and tuple(self.player.pos) == self.lab.goalpos:
                self.victory()
            self.events()
	    # check if rotation is needed
	    if self.motman.torotate:
		self.rotate(True)
		self.motman.torotate = False
	    # manage motion and collision
            motion = self.player.animate()
            if motion:
                dim, mov = motion
                pos = list(self.player.pos)
                pos[dim] += mov
                if self.lab.isfree(pos):
                    self.player.pos = pos
                else:
                    self.player.animation = None
	    # draw all
            self.gui.draw(self.player,
			  selection=self.motman.cdim,
			  usefilter=self.motman.filtering)
            clock.tick(FPS)

    def events(self):
        'manage the events to create motion'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.KEYDOWN:
                if not self.toanimate:
                    self.running = False
                if event.key == pygame.K_RETURN: # [START]
                    self.stop()
		# FOR DEBUG ONLY
		if event.key == pygame.K_ESCAPE:
			self.running = False
                else:
                    self.motman.keydown(event.key)
            elif event.type == pygame.KEYUP:
                self.motman.keyup(event.key)

    def stop(self):
        'exit the game'
        sys.exit()

    def victory(self):
	'enter victory mode (when key is pressed, terminate the maze)'
        self.toanimate = False
        self.gui.victory()


    # experimental for now
    def rotate(self, forward=True):
	"Rotate the maze forward one dimension."
	rotate1 = lambda block: geo.rotate1(block, forward)
	self.lab.rotate(forward)
	self.player.pos = rotate1(self.player.pos)
	# also, change motion and animation motion (small utility for that)
	def update1(motion):
            "rotate a motion's direction"
	    if not motion:
		return motion
	    dim, n = motion
	    if forward:
		dim = (dim+1) % self.lab.ndim
	    else:
		dim = (dim-1 + self.lab.ndim) % self.lab.ndim
	    return (dim, n)
        self.player.motion = update1(self.player.motion)
	anim = self.player.animation
	if anim:
	    anim.dim, anim.mov = update1((anim.dim, anim.mov))
	# also, rotate the GUI (needed for color management)
	self.gui.rotate()






def load(filename, settings={}):
    """Load and start a labyrinth: the format of the labyrinth file is described in the Labyrinth module.
    The settings argument conditions the keyset used (default is GCW-Zero)."""
    lab = Labyrinth.Labyrinth.fromfile(filename)
    game = Game(lab, settings)
    game.start()
