import math

from .data_node import DataNode
from .util import pts2tikz


class Edge:

    def __init__(self, name='', colour='blue!50!white', text_size='footnotesize'):
        super().__init__()
        self.name = name
        self.colour = colour
        self.text_size = text_size

    def to_tex(self, l: DataNode, r: DataNode, *, r_pos_y=None, l_pos_y=None, **kws) -> str:
        x = (r.pos[0] + l.pos[0])*.5
        pt1, pt4 = l.get_anchors()[1]
        pt2, pt3 = r.get_anchors()[0]
        if r_pos_y:
            pt2 = pt2[0], r_pos_y[1]
            pt3 = pt3[0], r_pos_y[0]
        if l_pos_y:
            pt1 = pt1[0], l_pos_y[1]
            pt4 = pt4[0], l_pos_y[0]
        y = sum([pt1[1], pt2[1], pt3[1], pt4[1]])/4
        tex = '\n' + pts2tikz([pt1, pt2, pt3, pt4, pt1], fill=self.colour, fill_opacity='0.5')
        dx = pt2[0] - pt1[0]
        dy = (pt2[1] + pt3[1])*.5 - (pt1[1] + pt4[1])*.5
        angle = math.atan(dy/dx)*180/math.pi
        if dx < 0: angle += 180
        tex += f'\\node[anchor=center, rotate={angle}] (foo) at ({x}, {y}) {{ \\{self.text_size} {self.name} }} ;'
        return tex
