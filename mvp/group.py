class Group:

    def __init__(self, name, contents, *, margin=(0.2, 0.5), colour='black!10!white', zorder=0,
                 label_pos='lower centre', skip: slice = None):
        self.name = name
        self.contents = contents
        self.margin = margin
        self.colour = colour
        self.zorder = zorder
        self.labelpos = label_pos
        self.skip = slice(0, -1) if not skip else skip

    def to_tex(self):
        mx, my = self.margin
        left = min([c.pos[0] for c in self.contents]) + mx
        right = max([c.pos[0]+c.size[0] for c in self.contents]) - mx
        top = max([c.pos[1]+c.size[1]/2+c.ds for c in self.contents[self.skip]]) + my
        bottom = min([c.pos[1]-c.size[1]/2-c.ds for c in self.contents[self.skip]]) - my - (0.1 if self.name else 0)
        rv = f'\\draw[{self.colour},ultra thick] ({left},{top}) rectangle ({right},{bottom});'
        if self.name:
            ypos, xpos = self.labelpos.split()
            anchor = ('north' if ypos == 'upper' else 'south') + {'centre': '', 'left': ' west', 'right': ' east'}[xpos]
            x = {'centre': (left + right) / 2, 'left': left, 'right': right}[xpos]
            y = {'upper': top, 'lower': bottom}[ypos]
            rv += f'\\node[anchor={anchor}] (foo) at ({x},{y}) {{ {self.name} }};'
        return rv
