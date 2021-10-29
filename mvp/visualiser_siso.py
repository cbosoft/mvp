from .visualiser_base import VisualiserBase


class Visualiser_SISO(VisualiserBase):
    def position_nodes(self):
        spacing = 3
        for i, node in enumerate(self.nodes):
            node.pos = [i * spacing, 0]

    def position_edges(self):
        pass
