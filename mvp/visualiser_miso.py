import networkx as nx

from .data_node import DataNode
from .visualiser_base import VisualiserBase


class Visualiser_MISO(VisualiserBase):

    def position_nodes(self):
        root = [n for n, deg in self._graph.out_degree() if not deg][0]
        self.graph2tree(root, 'down')
        spacing = 3
        for node in root:
            y = 0
            stt = 'alone'
            if node.parent:
                siblings_and_cousins = node.get_siblings_and_cousins()
                if len(siblings_and_cousins) > 1:
                    idx = siblings_and_cousins.index(node)
                    dys = [n.size[1] + 1.5 for n in siblings_and_cousins]
                    span = sum(dys)
                    cumu_dys = [dys[0]]
                    for dy in dys[1:]:
                        cumu_dys.append(cumu_dys[-1] + dy)
                    for i, dy in enumerate(dys):
                        cumu_dys[i] -= dy/2
                    y = cumu_dys[idx] - span/2
                    stt = f' many siblings {len(siblings_and_cousins)}'
                else:
                    y = node.parent.pos[1]
            print(y, stt)
            node.pos = [-node.get_level()*spacing, y]

    def position_edges(self):
        main_path = nx.dag_longest_path(self._graph)
        for node in self._graph.nodes:
            in_edges = self._graph.in_edges(node)
            if not in_edges:
                continue
            if len(in_edges) > 1:
                fract = 1 / len(in_edges)
                f = 0
                for edge in sorted(in_edges, key=lambda e: 1.0 if e[0] in main_path and e[1] in main_path else 0.0):
                    self._graph.edges[edge[0], edge[1]]['r_join_fract'] = f, f+fract
                    f += fract