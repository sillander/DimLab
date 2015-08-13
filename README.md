# DimLab
Dimensions Laboratory: explore mazes in more dimensions than you're used to!

This game is intended more as an experiment than a real game: it is not particularly fun to play, nor is it very rewarding. The goal is to try and stretch the player's mind to *more dimensions than just three* by the use of the *RGB colors*, which serve as auxiliary dimensions.

The game is intended to be *super light*, as to run on average-to-low performances platform (in particular, this game is intended for the GCW-Zero console). It is purely in *2D* (which can sound as a paradox) and runs on *Python 2*, with the gaming module *Pygame*.

The game can be started with the batch file *start.sh*, which also changes the game keyset to that of an AZERTY keyboard (for the moment, no other layout is supported, and no other language than English). This means the following keys are used:
- arrows to move on the XY plane
- A,E to decrease/increase the current color selection (explained in the game)
- S,Z to move backward/forward in the selected color
- Spacebar to filter out other colors
- Left Shift to use rotation (explained in the game)
- Return key to exit the game (referred to as START in the game)

As said before, this game is very basic, and the current version could be qualified as *very early alpha*. Further development might include:
1. A longer default scenario, which acually includes some full 5D (currently stops at 4)
2. Better command line options, and management for these (currently, hard-coded and ugly)
3. Better keyset support (just GCW and Azerty seems a bit short to me) (how about custom keyset?)
4. Better documentation, so that users can make mazes without having to read my comments
5. Multiplayer? Who knows?
6. Other languages (although, I must admit, this is absolutely not a priority)
 
That said, I'd like to thank all the people who supported me in this project, that is, the guys at Delta who canceled my flight so I could write code while waiting. You guys rock. Only not really.
