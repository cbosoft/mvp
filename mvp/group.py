class Group:

    def __init__(self, name, contents, *, margin=0.5, colour='black!10!white'):
        self.name = name
        self.contents = contents
        self.margin = margin
        self.colour = colour

    def to_tex(self):
        left = min([c.pos[0] for c in self.contents]) + self.margin
        right = max([c.pos[0]+c.size[0] for c in self.contents]) - self.margin
        top = max([c.pos[1]+c.size[1]/2+c.ds for c in self.contents]) + self.margin
        bottom = min([c.pos[1]-c.size[1]/2-c.ds for c in self.contents]) - self.margin
        rv = f'\\draw[fill={self.colour}] ({left},{top}) rectangle ({right},{bottom});'
        if self.name:
            rv += f'\\node[anchor=south] (foo) at ({left/2+right/2},{bottom}) {{ {self.name} }};'
        return rv
