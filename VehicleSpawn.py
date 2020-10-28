from Vehicle import Vehicle

# TODO: make vehicle spawning randomised


class VehicleSpawn:
    """a kind template for making vehicles"""
    def __init__(self, colour, width, vx, scale, rideable, chain_length=1) -> None:
        super().__init__()
        self.colour = colour
        self.width = width
        self.vx = vx
        self.scale = scale
        self.rideable = rideable
        self.chain_length = chain_length

    def spawn(self, location) -> Vehicle:
        return Vehicle(self, location)
