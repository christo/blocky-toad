import pygame

from Terrain import Terrain


class Block:

    def __init__(self, colour, terrain):
        super().__init__()
        self.colour = colour
        self.terrain = terrain
        self.passables = [Terrain.HOPPABLE, Terrain.GOAL, Terrain.FATAL]

    def draw(self, surface, r):
        pygame.draw.rect(surface, self.colour, r)

    def is_passable(self):
        return self.terrain in self.passables
