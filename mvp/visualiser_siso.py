from .visualiser_base import VisualiserBase


class Visualiser_SISO(VisualiserBase):
    def position_nodes(self):
        spacing_x = self.spacing[0]
        for i, node in enumerate(self.nodes):
            node.pos = [i * spacing_x, 0]

    def position_edges(self):
        pass
