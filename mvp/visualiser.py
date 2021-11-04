import os

import networkx as nx

from .data_node import DataNode, DataNode1D
from .edge import Edge
from .util import compile_tex
from .group import Group
from .layer import Layer


class Visualiser:

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
    CONVERT_COMMAND = 'convert'

    def __init__(self, fn: str, *, output_tex_too=False):
        self.nodes = []
        self.groups = []
        self._graph = nx.DiGraph()
        self.fn = os.path.abspath(fn)
        self.output_tex_too = output_tex_too
        self.spacing = (2, 3)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.draw()

    def graph2tree(self, ptr: DataNode, dir: str):
        edges = self._graph.in_edges(ptr) if dir == 'down' else self._graph.out_edges(ptr)
        for l, r in edges:
            ptr.add_child(l if dir == 'down' else r)

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
        self._graph.add_edge(a, b, layers=Edge(**kwargs), r_join_fract=(0, 1))

    def apply_layer_to(self, layer, node, group=None, **kwargs):
        if isinstance(layer, list):
            assert layer
            nodes = [node]
            for l in layer[:-1]:
                nodes.append(self.apply_layer_to(l, nodes[-1]))
            nodes.append(self.apply_layer_to(layer[-1], nodes[-1], **kwargs))
            if group is not None:
                self.group(*nodes, name=group)
            return nodes[-1]
        else:
            new = self.add_node(*layer(node), **kwargs)
            self.connect(node, new, **layer.edge_kwargs)
            return new

    def group(self, *nodes, name=None, **kwargs):
        self.groups.append(Group(name, nodes, **kwargs))

    def position_nodes(self):
        root = [n for n, deg in self._graph.out_degree() if not deg][0]
        self.graph2tree(root, 'down')
        spacing_x, spacing_y = self.spacing
        for node in root:
            y = 0
            if node.parent:
                siblings_and_cousins = node.get_siblings_and_cousins()
                if len(siblings_and_cousins) > 1:
                    idx = siblings_and_cousins.index(node)
                    dys = [n.size[1] + spacing_y for n in siblings_and_cousins]
                    span = sum(dys)
                    cumu_dys = [dys[0]]
                    for dy in dys[1:]:
                        cumu_dys.append(cumu_dys[-1] + dy)
                    for i, dy in enumerate(dys):
                        cumu_dys[i] -= dy/2
                    y = cumu_dys[idx] - span/2
                else:
                    y = node.parent.pos[1]
            node.pos = [-node.get_level()*spacing_x, y]

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

    def draw(self):
        tex = str(self.LATEX_HEAD)
        self.position_nodes()
        self.position_edges()
        for group in self.groups:
            tex += '\n' + group.to_tex()
        drawn = []
        for edge in self._graph.edges:
            l, r = edge
            if l not in drawn:
                tex += '\n' + l.to_tex()
                # drawn.append(l)
            layers = self._graph.edges[l, r]['layers']
            edge_data = dict(self._graph.edges[l, r])
            tex += '\n' + layers.to_tex(l, r, **edge_data)
            if r not in drawn and edge_data['r_join_fract'][0] < 0.01:
                tex += '\n' + r.to_tex()
                # drawn.append(r)
        tex += '\n' + self.LATEX_TAIL
        compile_tex(tex, self.fn, self.LATEX_COMMAND, self.output_tex_too, convert=self.CONVERT_COMMAND)
