from .data_node import DataNode
from .util import pts2tikz


class Layers:

    def __init__(self, name: str, colour='blue!50!white'):
        super().__init__()
        self.name = name
        self.colour = colour

    def to_tex(self, l: DataNode, r: DataNode, *, r_join_fract=None, **kws) -> str:
        x = (r.pos[0] + l.pos[0])*.5
        # y = (r.pos[1] + l.pos[1])*.5
        pt1, pt4 = l.get_anchors()[1]
        pt2, pt3 = r.get_anchors()[0]
        if r_join_fract:
            print(r_join_fract)
            ym = min([pt2[1], pt3[1]])
            span = abs(pt2[1] - pt3[1])
            pt2 = pt2[0], ym + span*r_join_fract[1]
            pt3 = pt3[0], ym + span*r_join_fract[0]
        y = sum([pt1[1], pt2[1], pt3[1], pt4[1]])/4
        tex = '\n' + pts2tikz([pt1, pt2, pt3, pt4, pt1], fill=self.colour, fill_opacity='0.5')
        tex += f'\\node[anchor=center] (foo) at ({x}, {y}) {{ {self.name} }} ;'
        return tex
