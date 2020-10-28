# Blocky Toad

Frogger, except instead of a frog it's a toad and instead of a toad, it's a block. 

Tested with: Pygame 2.0 and Python 3.9

Shout outs to all the people on the [OldSkoolCoder](https://github.com/oldskoolcoder/) 
Discord server and thanks John for streaming the 6502 stuff.

The font used is _PetMe64_ from 
[KreativeKorp](https://www.kreativekorp.com/software/fonts/c64.shtml) 
and the license for it is included as per the terms therein. 

## Features

* Dynamic playfield rescaling
* Arbitrary sized and shaped levels
* Configuration-driven

## Instructions

Play the game with keys WASD or arrows, get the frogs to the goals before the time
runs out.

The game is driven by the `config.py` script. You can change many things about the
game in there including defining levels of arbitrary size (and shape!). Look in that
file for examples of the way levels are defined. You need to adhere to python syntax
rules or probably everything will break. 

## How to build

`Game.py` can be run if you already have pygame installed. If that doesn't work, 
read on. 

Install dependencies with pipenv by running the provided `install.sh` or if you 
know what you're doing... do that.

Note that in order to run on macos I needed to use pygame 2.0 which is currently
in pre-release which necessitates the pipenv `--pre` option.

Pull requests are encouraged!

## TODO 

* BUG: frog does not fall off rideable at edge of screen but gets stuck
* some kind of random spawn rate - need maybe min and max of uniform range
* finish defining the levels so the game can be finished
* add fly and other bonuses, maybe turtles etc.
