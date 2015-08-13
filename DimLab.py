#!/usr/bin/env python2

# This game is a simple 5-dimension labyrinth experiment.
# OK, this sounds more neat than simple, really, and in truth it can be pretty disorienting.
# The appearance of this game is like totally lame, I know, but I'm more a programming enthusiast (and CS student,
# kindof), than anything near to a graphic artist. (I'm an engineer, actually, and I love math)

# If you are a PLAYER: everything you need to know is explained in the game. Actually, this game is destined to the
# GCW-ZERO console, so you might find the keyset pretty confusing (I know it is). Basically:
# arrows: arrows (moving on the [x,y] plane)
# A: LCTRL (switch color dimension)
# B: LALT  (switch color dimension, reverse)
# L (shoulder): BACKSPACE (backward in a color dimension)
# R (shoulder): TAB       (forward in a color dimension)
# X: SPACEBAR (filter other dimensions)

# If you are a PROGRAMMER, then please have mercy. I coded this very rapidly, so the structure, even though
# straightforward, is not optimal or anything. I'm sure I've done dozens of absolutely wrong Python no-no's (though I
# try to avoid it, sometimes the easy path is, well, easier).
# From a high-level standpoint, though, I admit things are simple. You can actually create a game for this without
# knowing any sort of code (even though it's not well documented, as I write these lines).
# Basically, the files are organized the following way:
# - 3 high-level modules, which have a one-argument load function expecting a file. These classes manage the various
#     modes of the game, and are namely: Text (display text), Image (display Image) and Game (start a labyrinth and
#     have fun). These classes manage themselves exits and all, so the game can be consecutive calls to load from these
#     modules. The file format are pretty standard, and are documented in the modules.
# - a Labyrinth module, which describes a labyrinth (obviously), and can create labyrinths from a given file. There is
#     not much to say here: go check it out if you want.
# - a GUI module, with a GUI class destined to the GAME ONLY. I've tried (although not very hard) to keep it as clean as
#     possible. Basically, it displays the labyrinth, and the symbols you see on the screen. That's all

# Thanks for reading this! Have fun (I hope) playing this demented game!


# high-level modules
import Game
import Text
import Image

import pickle
import sys, os



# MODULE DEFINITION PART

# Here, we define what a scenario file looks like.
# Basically, every line defines one screen to display, in the form:
# "T"|"I"|"L" " " <filename>
# where T,I,L are the etypes (you can also fully type the etypes as defined below:

# shortcuts: etypes
T = 'text'
I = 'image'
L = 'labyrinth'

ETYPES = {'T':T, 'I':I, 'L':L}
FOLDERS = {T:'texts', I:'images', L:'labs'}
MODULES = {T:Text, I:Image, L:Game}

import time
def start(scenario, settings={}):
    """Yet another load function: turn a list into a playable scenario"""
    for etype, filename in scenario:
        fullfile = os.path.join(FOLDERS[etype], filename)
        MODULES[etype].load( fullfile, settings )

def read_scenario(filename):
    'read a scenario from a file'
    scenario = []
    with open(filename, 'r') as ff:
        for line in ff:
            if line.startswith('#') or len(line.strip(' \n\t')) < 2:
                continue # empty line
            etype, fname = line.strip('\n').split(' ', 1)
            if etype not in [T,I,L]:
                etype = ETYPES[etype]
            scenario.append((etype, fname.strip(' \r\n\t')))
    return scenario


def load(filename, settings):
    """Load a scenario and start it, from given scenario file."""
    start( read_scenario(filename), settings ) # though call babe



# MAIN PROGRAM PART
if __name__ == '__main__':
    filename = 'scenario/default.txt'
    settings = {}
    if len(sys.argv) > 1:
	if sys.argv[1] == '-k':
	    settings["UseAzerty"] = True
	else:
            filename = sys.argv[1]
    if len(sys.argv) > 2:
	if sys.argv[2] == '-k':
	    settings["UseAzerty"] = True
    load(filename, settings)
    sys.exit(0)
