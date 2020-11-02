from Vehicle import Vehicle


class VehicleSpec:
    """a kind template for making vehicles"""
    def __init__(self, colour, width, scale, rideable, chain_length=1) -> None:
        super().__init__()
        self.colour = colour
        self.width = width
        self.scale = scale
        self.rideable = rideable
        self.chain_length = chain_length

