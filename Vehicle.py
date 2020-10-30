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
    def __init__(self, spec, position, speed) -> None:
        super().__init__()
        self.spec = spec
        self.speed = speed
        self.pos = position

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        rideability = "rideable" if self.spec.rideable else "unrideable"
        sx = self.pos[X]
        sy = self.pos[Y]
        return "%s @ %1.2f->%1.2f,%1.2f" % (rideability, sx, sx + self.spec.width, sy)

    def draw(self, surface, pos_to_pixels, block_size, clip):
        """
        Draw ourself at given block size on surface using pos_to_pixels to convert position confined to clip rect
        """
        px = pos_to_pixels(self.pos)
        inset = round(-block_size * (1 - self.spec.scale))
        width = self.spec.width
        pixel_width = width * block_size
        for i in range(self.spec.chain_length):
            rect = Rect(px[X] + i * pixel_width, px[Y], width * block_size, block_size).inflate(inset, inset).clip(clip)
            pygame.draw.rect(surface, self.spec.colour, rect)

    def update(self, scene_width_blocks) -> bool:
        """
        Moves the vehicle, returning true iff it has disappeared off screen.
        """
        x = self.pos[0]
        x = x + self.speed * config.game_speed / 100
        self.pos = (x, self.pos[Y])
        w = self.total_width()
        going_left = self.speed < 0
        disappeared_off_left = (x + w < 0 and going_left)
        disappeared_off_right = (x > scene_width_blocks and not going_left)
        return not (disappeared_off_left or disappeared_off_right)

    def collides_with(self, other) -> bool:
        """Returns true only if other overlaps with the vehicle's current position."""
        # TODO make collision detection work better - used only for frog collision?
        return other[Y] == self.pos[Y] and self.pos[X] <= other[X] <= (self.pos[X] + self.total_width())

    def total_width(self) -> int:
        return self.spec.width * self.spec.chain_length

    def is_rideable(self) -> bool:
        return self.spec.rideable
