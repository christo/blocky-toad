# Blocky Toad

Frogger, except instead of a frog it's a toad and instead of a toad, it's a block. 

Tested with: Pygame 2.0 and Python 3.9

Thanks to all the people on the [OldSkoolCoder](https://github.com/oldskoolcoder/) Discord server.

## Instructions

Play the game with keys WASD or arrows, get the frogs to the goals before the time runs out.

The game is driven by the `config.py` script. You can change many things about the game in there including defining levels of arbitrary size. Look in that file for examples of the way levels are defined. You need to adhere to python syntax rules. 

## How to build

Install dependencies with pipenv by running the provided `install.sh` or if you know what you're doing... do that.

Note that in order to run on macos I needed to use pygame 2.0 which is currently in pre-release.

## TODO 

* some kind of random spawn rate - need maybe min and max of uniform range
