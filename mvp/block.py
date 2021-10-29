class Block:

    def __init__(self):
        self.pos = [0, 0]

    def to_tex(self, pos: list) -> str:
        raise NotImplementedError
