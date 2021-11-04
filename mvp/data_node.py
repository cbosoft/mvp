from .node_base import TreeNode
from .util import pts2tikz


class DataNode(TreeNode):

    SCALE = (0.1, 0.07, 0.1)
    # scale w, h, d
    IDX = 0

    def __init__(self, n, c, l, *, name=None, label_text_size='tiny', name_text_size='small'):
        super().__init__()
        self.size_unscaled = n, c, l
        self.size = [v*s for v, s in zip([n, l, c], self.SCALE)]
        self.pos = [0, 0]
        self.name = name
        self.path_id = 0
        self.idx = DataNode.IDX
        DataNode.IDX += 1
        self.label_text_size = label_text_size
        self.name_text_size = name_text_size

    def __lt__(self, other):
        return self.idx >= other.idx

    @property
    def ds(self):
        w, h, d = self.size
        return(2**0.5)*d/4

    def to_tex(self) -> str:
        x, y = self.pos
        w, h, d = self.size
        dx = dy = self.ds
        y -= h/2
        outline = [
            (x-dx, y-dy),
            (x-dx, y-dy+h),
            (x+dx, y+dy+h),
            (x+dx+w, y+dy+h),
            (x+dx+w, y+dy),
            (x-dx+w, y-dy),
            (x-dx, y-dy)
        ]
        inline1 = [
            (x-dx, y-dy+h),
            (x-dx+w, y-dy+h),
            (x+dx+w, y+dy+h)
        ]
        inline2 = [
            (x-dx+w, y-dx+h),
            (x-dx+w, y-dx)
        ]
        outline_tex = pts2tikz(outline, fill='white')
        inline_tex_1 = pts2tikz(inline1)
        inline_tex_2 = pts2tikz(inline2)
        tex = '\n'.join([outline_tex, inline_tex_1, inline_tex_2])
        if self.name:
            miny = min([y for _, y in outline])
            tex += f'\\node[anchor=north] (foo) at ({x+w/2}, {miny}) {{ \\{self.name_text_size} {self.name} }};'
        tex += f'\\node[anchor=south, rectangle, fill=white, fill opacity=0.5, text opacity=1, inner sep=1, outer sep=1] (foo) at ({x+dx+w/2}, {y+dy+h}) {{ \\{self.label_text_size} {self.get_label()} }};'
        return tex

    def get_anchors(self):
        x, y = self.pos
        w, h, d = self.size
        y -= h/2
        anchors_left = [(x, y+h), (x, y)]
        anchors_right = [(x+w, y+h), (x+w, y)]
        return anchors_left, anchors_right

    def get_label(self) -> str:
        w, h, d = self.size_unscaled
        return f'{int(w)}$\\times${int(h)}$\\times${int(d)}'


class DataNode1D(DataNode):

    def __init__(self, f, c, *, name=None):
        super().__init__(1, f, c, name=name)
