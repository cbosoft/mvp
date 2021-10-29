import os

import networkx as nx

from .data_node import DataNode, DataNode1D
from .layers import Layers
from .util import compile_tex


class VisualiserBase:

    LATEX_HEAD = r'''
\documentclass{standalone}
\usepackage{tikz}

\begin{document}
  \begin{tikzpicture}
'''
    LATEX_TAIL = r'''
  \end{tikzpicture}
\end{document}
'''
    LATEX_COMMAND = 'xelatex --interaction=nonstopmode'

    def __init__(self, fn: str, *, output_tex_too=False):
        self.nodes = []
        self._graph = nx.DiGraph()
        self.fn = os.path.abspath(fn)
        self.output_tex_too = output_tex_too

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.draw()

    def graph2tree(self, ptr: DataNode, dir: str):
        edges = self._graph.in_edges(ptr) if dir == 'down' else self._graph.out_edges(ptr)
        for child, _ in edges:
            ptr.add_child(child)

        for child in ptr.children:
            self.graph2tree(child, dir)

    def add_node(self, *args, **kwargs):
        node = DataNode(*args, **kwargs)
        self._graph.add_node(node)
        self.nodes.append(node)
        return node

    def add_node_1d(self, *args, **kwargs):
        node = DataNode1D(*args, **kwargs)
        self._graph.add_node(node)
        self.nodes.append(node)
        return node

    def connect(self, a, b, **kwargs):
        self._graph.add_edge(a, b, layers=Layers(**kwargs), r_join_fract=(0, 1))

    def position_nodes(self):
        main_path = nx.dag_longest_path(self._graph)
        nodes_above = [*main_path]
        spacing = 3
        for i, block in enumerate(main_path):
            block.pos = [i * spacing, 0]

        in_nodes = [l for l, deg in self._graph.in_degree() if not deg]
        out_nodes = [l for l, deg in self._graph.out_degree() if not deg]
        for i, i_n in enumerate(in_nodes):
            for o_n in out_nodes:
                path = nx.shortest_path(self._graph, i_n, o_n)
                if all([node in main_path for node in path]):
                    continue
                path_on_main = len([n for n in path if n in main_path])
                path_not_on_main = len(path) - path_on_main
                n = len(main_path) - path_on_main
                x = n - path_not_on_main
                assert x >= 0
                for node in path:
                    if node not in main_path:
                        node.pos[0] = x * spacing
                        node.pos[1] = nodes_above[x].pos[1] - nodes_above[1].size[1] / 2 - node.size[1] / 2 - 0.75
                        nodes_above[x] = node
                        x += 1

    def position_edges(self):
        main_path = nx.dag_longest_path(self._graph)
        for node in self._graph.nodes:
            in_edges = self._graph.in_edges(node)
            print(in_edges)
            if not in_edges:
                continue
            if len(in_edges) > 1:
                fract = 1 / len(in_edges)
                f = 0
                for edge in sorted(in_edges, key=lambda e: 1.0 if e[0] in main_path and e[1] in main_path else 0.0):
                    self._graph.edges[edge[0], edge[1]]['r_join_fract'] = f, f+fract
                    f += fract

    def draw(self):
        tex = str(self.LATEX_HEAD)
        self.position_nodes()
        self.position_edges()
        drawn = []
        for edge in self._graph.edges:
            l, r = edge
            if l not in drawn:
                tex += '\n' + l.to_tex()
                drawn.append(l)
            layers = self._graph.edges[l, r]['layers']
            edge_data = dict(self._graph.edges[l, r])
            tex += '\n' + layers.to_tex(l, r, **edge_data)
            if r not in drawn and edge_data['r_join_fract'][0] < 0.01:
                tex += '\n' + r.to_tex()
                drawn.append(r)
        tex += '\n' + self.LATEX_TAIL
        compile_tex(tex, self.fn, self.LATEX_COMMAND, self.output_tex_too)
