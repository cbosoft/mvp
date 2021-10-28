from .block import Block
from .data_block import DataBlock


class ActionBlock(Block):

    def __init__(self, name: str, width=2, colour='blue!50!white'):
        self.name = name
        self.width = width
        self.colour = colour

    def to_tex(self, pos: list, prev: DataBlock, next: DataBlock) -> str:
        x, y = pos
        x += self.width/2.
        pos[0] += self.width
        pt1, pt4 = prev.get_anchors()[1]
        pt2, pt3 = next.get_anchors(*pos)[0]
        tex = '\n' + self.pts2tikz([pt1, pt2, pt3, pt4, pt1], fill=self.colour, fill_opacity='0.5')
        tex += f'\\node[anchor=center] (foo) at ({x}, {y}) {{ {self.name} }} ;'
        return tex
