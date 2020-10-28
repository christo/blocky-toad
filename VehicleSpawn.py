from Vehicle import Vehicle

# TODO: make vehicle spawning randomised


class VehicleSpawn:
    """a kind template for making vehicles"""
    def __init__(self, colour, width, vx, scale, rideable) -> None:
        super().__init__()
        self.colour = colour
        self.width = width
        self.vx = vx
        self.scale = scale
        self.rideable = rideable

    def spawn(self, location) -> Vehicle:
        return Vehicle(self, location)
