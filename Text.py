# A simple class, just like Game, to display text between labyrinths.
# Although this supports several lines (contrarily to pygame's defaults), it is still pretty basic, and lines
# should not be longer than 28 characters (for large characters only: you can go up to 40 I guess).
# Also, the number of displayable lines is limited (and is around 10). There is not explicit
# check for these format conditions, so it is expected of the user to check if the text looks good.

import sys
import pygame
pygame.init()


FPS = 60

SCRW = 320
SCRH = 240

SPACING = 6 # between lines
PARSPACING = 16 # paragraph spacing

FONT = pygame.font.Font('orbitron.ttf', 16)

class Text:
    """Manages full screen display of a doubly centered text."""
    def __init__(self, text):
	"display the text as full screen until input"
        self.texts = text.split('\n')
        self.screen = pygame.display.set_mode((SCRW, SCRH))
        # render these texts
        self.rtexts = []
        offset = 0 # to compensate the final spacing overflow
        incr = 0
        for txt in self.texts:
            if not txt.strip(' \r\n\t'):
                offset += PARSPACING
                continue
            rtxt = FONT.render(txt, 1, (255,255,255))
            self.rtexts.append((rtxt,offset))
            incr = (SPACING + rtxt.get_rect().height)
            offset += incr
        offset -= (incr-SPACING)
        # display these texts
        self.screen.fill((0,0,0))
        for text, toffset in self.rtexts:
            self.screen.blit(text, text.get_rect(centerx=SCRW/2, centery=SCRH/2+toffset-offset/2))
        pygame.display.flip()

    def start(self):
        "display the text and wait for events to happen"
        running = True
        clock = pygame.time.Clock()
        while running:
            # events management
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.stop()
                    else:
                        running = False
            # GUI management
            # actually, the GUI is good looking already :-p
            # FPS management
            clock.tick(FPS)

    def stop(self):
	"called internally: stop the game (pressed on START)"
        sys.exit()


def load(filename, settings={}):
    """Display a simple text file to be skipped upon keydown.
    The lines in the text should be neither too long (>28c) or too numerous (>10), as this will 
    make text overflow from the screen.
    The settings argument is, as of now, ignored."""
    with open(filename, 'r') as ff:
        text = Text(ff.read())
        text.start()
