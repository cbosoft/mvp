class TreeNode:

    def __init__(self, parent=None):
        self.parent = parent
        self.children = []

    @property
    def siblings(self):
        return tuple() if not self.parent else tuple(self.parent.children)

    def get_siblings_and_cousins(self):
        root = self.get_root()
        level = self.get_level()
        rv = root.get_all_children_at_level(level)
        return rv

    def get_all_children_at_level(self, level: int):
        if level != self.get_level():
            rv = []
            for child in self.children:
                rv.extend(child.get_all_children_at_level(level))
            return rv
        return [self]

    def get_root(self):
        if self.parent:
            return self.parent.get_root()
        return self

    def add_child(self, child):
        self.children.append(child)
        self.children = sorted(self.children)
        child.parent = self

    def get_level(self) -> int:
        if self.parent is None:
            return 0
        else:
            return 1 + self.parent.get_level()

    def _gen(self):
        yield self

        for child in self.children:
            for node in child:
                yield node

    def __iter__(self):
        return self._gen()