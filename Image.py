# simple class to display an image (as the Text class does with text)
# The supported image formats are those that pygame uses.

import Text
import pygame

class Image(Text.Text):
    """Class that creates an image and waits for keypress.
    This uses the same techniques as described by Text, and thus inherits it for that purpose."""
    def __init__(self, image):
        Text.Text.__init__(self, '') # init with empty text (screen will be overwritten anyway)
        self.screen.fill((0,0,0))
        self.screen.blit(image, image.get_rect(left=0, top=0)) # this is default, I think (so kinda useless)
        pygame.display.flip()

def load(filename, settings=None):
    """Load the image described at filename, and display it fullscreen while waiting for keypress.
    The image formats accepted are those for the pygame.image.load function (see documentation).
    The settings argument will be ignored."""
    image = pygame.image.load(filename)
    imageo = Image(image)
    imageo.start()
