import random

import pygame

from Vehicle import Vehicle


class Spawn:
    """
    Defines a point on the level map that emits Vehicles
    """

    def __init__(self, spec, location, speed, respawn) -> None:
        """
        Construct a Spawn point which emits vehicles of the given spec and speed at the given location
        on a random schedule specified by respawn.
        :param spec: definition of the vehicles emitted.
        :param location: block position tuple (x,y)[
        :param speed: horizontal velocity[
        :param respawn: tuple of min, max respawn seconds.
        """
        super().__init__()
        self.spec = spec
        self.location = location
        self.speed = speed
        self.respawn = respawn
        self.next_spawn = 0

    def update(self, vehicle_consumer):
        if pygame.time.get_ticks() > self.next_spawn:
            vehicle_consumer(Vehicle(self.spec, self.location, self.speed))
            self.reset()

    def reset(self):
        # set up random thingy
        self.next_spawn = pygame.time.get_ticks() + random.uniform(self.respawn[0], self.respawn[1]) * 1000

