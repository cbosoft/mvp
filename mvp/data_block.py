from .block import Block


class DataBlock(Block):

    SCALE = (0.07, 0.07, 0.07)
    # scale w, h, d

    def __init__(self, w, h, d, *, name=None):
        self.size = [v*s for v, s in zip([w, h, d], self.SCALE)]
        self.ppos = None
        self.name = name

    def to_tex(self, pos: list) -> str:
        x, y = pos
        self.ppos = [*pos]
        w, h, d = self.size
        dx = dy = (2**0.5)*d/4
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
        outline_tex = self.pts2tikz(outline, fill='white')
        inline_tex_1 = self.pts2tikz(inline1)
        inline_tex_2 = self.pts2tikz(inline2)
        tex = '\n'.join([outline_tex, inline_tex_1, inline_tex_2])
        pos[0] += w + dx
        if self.name:
            miny = min([y for _, y in outline])
            tex += f'\\node[anchor=north] (foo) at ({x+w/2}, {miny}) {{ {self.name} }};'
        return tex

    def get_anchors(self, x=None, y=None):
        if x is None:
            x, y = self.ppos
        w, h, d = self.size
        y -= h/2
        anchors_left = [(x, y+h), (x, y)]
        anchors_right = [(x+w, y+h), (x+w, y)]
        return anchors_left, anchors_right


class DataBlock1D(DataBlock):

    def __init__(self, f, c, *, name=None):
        super().__init__(1, c, f, name=name)
