import networkx as nx

from .visualiser_base import VisualiserBase
from .visualiser_siso import Visualiser_SISO
from .visualiser_miso import Visualiser_MISO

from .data_node import DataNode


class Visualiser(VisualiserBase):

    @property
    def order(self):
        n_in = len([n for n, deg in self._graph.in_degree() if deg == 0])
        n_out = len([n for n, deg in self._graph.out_degree() if deg == 0])
        return n_in, n_out

    def position_nodes(self):
        n_in, n_out = self.order
        if n_in == 1 and n_out == 1:
            Visualiser_SISO.position_nodes(self)
        elif n_in == 1 and n_out > 1:
            raise NotImplementedError
        elif n_in > 1 and n_out == 1:
            Visualiser_MISO.position_nodes(self)
        elif n_in > 1 and n_out > 1:
            raise NotImplementedError
        else:
            raise NotImplementedError

    def position_edges(self):
        n_in, n_out = self.order
        if n_in == 1 and n_out == 1:
            Visualiser_SISO.position_edges(self)
        elif n_in == 1 and n_out > 1:
            raise NotImplementedError
        elif n_in > 1 and n_out == 1:
            Visualiser_MISO.position_edges(self)
        elif n_in > 1 and n_out > 1:
            raise NotImplementedError
        else:
            raise NotImplementedError