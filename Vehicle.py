import pygame
from pygame import Rect

import config

"""convenience component offsets for tuple coordinates"""
X = 0
Y = 1


class Vehicle:
    """
    Represents a truck, car, log, turtle or other moving object
    """
    def __init__(self, spawn, position) -> None:
        super().__init__()
        self.colour = spawn.colour
        self.width = spawn.width
        self.vx = spawn.vx
        self.scale = spawn.scale
        self.rideable = spawn.rideable
        self.pos = position
        self.initial_pos = position

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        rideability = "rideable" if self.rideable else "unrideable"
        sx = self.pos[X]
        sy = self.pos[Y]
        return "%s @ %1.2f->%1.2f,%1.2f" % (rideability, sx, sx + self.width, sy)

    def draw(self, surface, pos_to_pixels, size, clip):
        """
        Draw ourself at given block size on surface using pos_to_pixels to convert position confined to clip rect
        """
        px = pos_to_pixels(self.pos)
        inset = round(-size * (1 - self.scale))
        rect = Rect(px[X], px[Y], self.width * size, size).inflate(inset, inset).clip(clip)
        pygame.draw.rect(surface, self.colour, rect)

    def update(self, scene_width_blocks):
        """Moves the vehicle, resetting to original position once off-screen."""
        x = self.pos[0]
        x = x + self.vx * config.game_speed / 100
        self.pos = (x, self.pos[Y])
        if x + self.width < 0 or x - self.width > scene_width_blocks:
            self.pos = self.initial_pos

    def collides_with(self, other) -> bool:
        """Returns true only if other overlaps with the vehicle's current position."""
        return other[Y] == self.pos[Y] and self.pos[X] <= other[X] <= (self.pos[X] + self.width)
