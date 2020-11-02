import string

from Block import Block
from Spawn import Spawn


class Level:
    def __init__(self) -> None:
        super().__init__()
        self.block_chars = {}
        self.spawn_chars = {}
        self.start = ''
        self.time = 60

    def block(self, ch, block):
        self.check_whitespace(ch)
        self.block_chars[ch] = block
        return self

    def spawn(self, ch, vehicle, speed, respawn):
        self.check_whitespace(ch)
        self.spawn_chars[ch] = (vehicle, speed, respawn)
        return self

    def start(self, ch):
        self.check_whitespace(ch)
        self.start = ch
        return self

    def timer(self, seconds):
        self.time = seconds
        return self

    def read(self, level_definition) -> dict:
        """
        Reads a 2d level layout string and builds the level based on the registered block, spawn, etc.



        :param level_definition: the string that defines the level
        :return: the level definition dict
        """
        lev = {"level": [[Block]], "spawns": [Spawn], "start": (0, 0), "time": self.time}
        y = 0
        for line in level_definition.splitlines():
            x = 0
            blocks = []
            for ch in line:
                if ch not in string.whitespace:
                    try:
                        blocks.append(self.block_chars[ch])
                    except IndexError:
                        try:
                            sp3 = self.spawn_chars[ch]
                            spawn = Spawn(sp3[0], (x, y), sp3[1], sp3[2])
                            lev["spawns"].append(spawn)
                        except IndexError:
                            if self.start == ch:
                                lev["start"] = (x, y)
                            else:
                                # panic
                                print("mama!")
                                raise ValueError
                x = x + 1
            if len(blocks) > 0:
                lev["level"].append(blocks)
                y = y + 1
        return lev

    @staticmethod
    def check_whitespace(ch):
        if ch in ' \n\t\v\b\r':
            print("cannot redefine whitespace")
            raise ValueError
