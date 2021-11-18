from typing import List

from .data_node import DataNode


class Layer:

    def __init__(self, name='', colour='blue!50!white'):
        self.name = name
        self.colour = colour

    @property
    def edge_kwargs(self):
        return dict(
            name=self.name,
            colour=self.colour,
            details=self.get_details()
        )

    def __call__(self, inp):
        return self.get_output_size(inp)

    def get_output_size(self, node: DataNode):
        raise NotImplementedError

    def get_details(self) -> List[str]:
        return []
