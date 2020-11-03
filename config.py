from Block import Block
from Spawn import Spawn
from Terrain import Terrain
from VehicleSpec import VehicleSpec
from util import seq

# initial window size in pixels
width = 1000
height = 800

# can be toggled in game with F2, draws stuff all over the screen
debug_mode = False

# c64 palette from https://www.c64-wiki.com/wiki/Color
black = (0, 0, 0)
white = (255, 255, 255)
red = (136, 0, 0)
cyan = (170, 255, 238)
purple = (204, 68, 204)
green = (0, 204, 85)
blue = (0, 0, 170)
yellow = (238, 238, 119)
orange = (221, 136, 85)
brown = (102, 68, 0)
light_red = (255, 119, 119)
dark_grey = (51, 51, 51)
medium_grey = (119, 119, 119)
light_green = (170, 255, 102)
light_blue = (0, 136, 255)
light_grey = (187, 187, 187)

croc_colour = medium_grey  # TODO crocodile
frog_colour = light_green
fly_colour = light_grey  # bonus at endzone TODO fly

title_shadow = blue
title_fg = yellow
background = light_blue
border = black

game_name = "Blocky Toad"
byline = "by ChromoSundrift"
instructions = "hit the any key!"

# define the level's blocks
bush = Block(green, Terrain.BARRIER)
river = Block(blue, Terrain.FATAL)
path = Block(purple, Terrain.HOPPABLE)
road = Block(dark_grey, Terrain.HOPPABLE)
goal = Block(blue, Terrain.GOAL)

# define vehicles, including moving river objects
car = VehicleSpec(light_red, 1, 0.5, False)
bus = VehicleSpec(yellow, 2, 0.7, False)
log3 = VehicleSpec(brown, 3, 0.7, True)
log4 = VehicleSpec(brown, 4, 0.7, True)
log2 = VehicleSpec(brown, 2, 0.7, True)
turtles = VehicleSpec(red, 1, 0.8, True, 3)
road_train = VehicleSpec(medium_grey, 3, 0.7, False, 2)
bus2 = VehicleSpec(orange, 3, 0.7, False)


# define levels from blocks
slow_respawn = (7, 8)
slower_respawn = (9, 12)
fast_respawn = (2, 4)

# starting level_num, 0 is the first
start_level = 0
levels = [{
    "level": [
        seq(7, bush),
        [bush, goal, bush, goal, bush, goal, bush],
        seq(7, river),
        seq(7, river),
        seq(7, path),
        seq(7, road),
        seq(7, road),
        seq(7, path)
    ],
    "start": (3, 7),
    "spawns": [
        Spawn(bus, (9, 6), -2, slow_respawn),
        Spawn(car, (-1, 5), 4, fast_respawn),
        Spawn(log3, (-3, 2), 1, slow_respawn),
        Spawn(log4, (7, 3), -1, slow_respawn)
    ],
    "time": 60
}, {
    # this is the same layout as the original frogger
    "level": [
        seq(19, bush),
        [bush, goal, bush, bush, bush, goal, bush, bush, bush, goal, bush, bush, bush, goal, bush, bush,
         bush, goal, bush],
        seq(19, river),
        seq(19, river),
        seq(19, river),
        seq(19, river),
        seq(19, river),
        seq(19, path),
        seq(19, road),
        seq(19, road),
        seq(19, road),
        seq(19, road),
        seq(19, road),
        seq(19, road),
        seq(19, path)
    ],
    "start": (10, 14),
    "spawns": [
        Spawn(log4, (-4, 2), 1, slow_respawn),
        Spawn(log3, (20, 3), -1, slow_respawn),
        Spawn(log4, (-4, 4), 1.3, slow_respawn),
        Spawn(log2, (20, 5), -0.9, slow_respawn),
        Spawn(turtles, (-1, 6), 1.3, slow_respawn),
        Spawn(road_train, (-6, 8), 3, fast_respawn),
        Spawn(car, (20, 9), -3.3, fast_respawn),
        Spawn(bus, (20, 10), -2.3, slow_respawn),
        Spawn(bus, (20, 11), -2.3, slow_respawn),
        Spawn(car, (-1, 12), 4, fast_respawn),
    ],
    "time": 180
}, {
    "level": [
        seq(50, bush),
        seq(10, [bush, bush, goal, bush, bush]),
        seq(50, river),
        seq(50, river),
        seq(50, river),
        seq(50, river),
        seq(50, river),
        seq(50, path),
        seq(50, road),
        seq(50, road),
        seq(50, road),
        seq(50, road),
        seq(50, road),
        seq(50, path),
        seq(50, river),
        seq(50, river),
        seq(50, river),
        seq(50, river),
        seq(50, river),
        seq(50, path),
        seq(50, road),
        seq(50, road),
        seq(50, road),
        seq(50, road),
        seq(50, road),
        seq(50, path),
        seq(50, river),
        seq(50, river),
        seq(50, path),
        seq(50, road),
        seq(50, road),
        seq(50, road),
        seq(50, road),
        seq(50, road),
        seq(50, road),
        seq(50, road),
        seq(50, road),
        seq(50, path)
    ],
    "start": (25, 37),
    "spawns": [
        Spawn(log4, (-4, 2), 1, slow_respawn),
        Spawn(log3, (51, 3), -1, slow_respawn),
        Spawn(log4, (-4, 4), 1.3, slow_respawn),
        Spawn(turtles, (51, 5), -1.3, slow_respawn),
        Spawn(log4, (-4, 6), 0.9, slow_respawn),
        Spawn(road_train, (-6, 8), 3, fast_respawn),
        Spawn(car, (51, 9), -3.3, fast_respawn),
        Spawn(bus, (51, 10), -2.3, slow_respawn),
        Spawn(bus, (51, 11), -2.1, slow_respawn),
        Spawn(car, (-1, 12), 4, fast_respawn),
        Spawn(log3, (51, 14), -2, fast_respawn),
        Spawn(log3, (-3, 15), 2, fast_respawn),
        Spawn(turtles, (51, 16), -1.3, slow_respawn),
        Spawn(turtles, (-3, 17), 1.4, slow_respawn),
        Spawn(turtles, (53, 18), -1.5, slow_respawn),
        Spawn(car, (-1, 20), 5, slow_respawn),
        Spawn(road_train, (-6, 21), 3.2, slow_respawn),
        Spawn(road_train, (-6, 22), 1.2, slow_respawn),
        Spawn(bus, (51, 23), -2.1, slow_respawn),
        Spawn(bus, (51, 24), -2.4, slow_respawn),
        Spawn(log4, (-4, 26), 0.9, slower_respawn),
        Spawn(log4, (54, 27), -1.8, slow_respawn),
        Spawn(car, (-1, 29), 5, slow_respawn),
        Spawn(car, (-1, 30), 5, slow_respawn),
        Spawn(bus2, (-3, 31), 2.5, slow_respawn),
        Spawn(car, (-1, 32), 5.1, slow_respawn),
        Spawn(road_train, (56, 33), -3.3, slower_respawn),
        Spawn(car, (51, 34), -4.9, slower_respawn),
        Spawn(car, (51, 35), -4.8, slower_respawn),
        Spawn(car, (51, 36), -5.1, fast_respawn),
    ],
    "time": 360
}]

font_name = "PetMe64.ttf"
font_scale = 1.0

game_speed = 1.7
lives = 5

# game play area as measured in blocks (aka sprite size)
playfield_wb = 19
playfield_hb = 14

get_ready_timeout = 3000  # ms
