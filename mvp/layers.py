from typing import List

from .layer import Layer
from .data_node import DataNode


class Conv1d(Layer):

    def __init__(self, in_ch: int, out_ch: int, kernel: int, stride=1, padding=0, dilation=1, name=None):
        super().__init__(self.__class__.__name__ if name is None else name)
        self.in_ch: int = in_ch
        self.out_ch: int = out_ch
        self.kernel: int = kernel
        self.stride: int = stride
        self.padding: int = padding
        self.dilation: int = dilation

    def get_output_size(self, node: DataNode):
        n, c, l = node.size_unscaled
        assert c == self.in_ch, f'in {self.__class__.__name__}: {c} != {self.in_ch}'
        c = self.out_ch
        l = (l + 2*self.padding - self.dilation*(self.kernel - 1) - 1)//self.stride + 1
        return n, c, l

    def get_details(self) -> List[str]:
        return [f'${{\\rm kernel}} = {self.kernel}$', f'${{\\rm stride}} = {self.stride}$',
                f'${{\\rm padding}} = {self.padding}$', f'${{\\rm dilation}} = {self.dilation}$']


class MaxPool1d(Layer):

    def __init__(self, kernel, stride=None, padding=0, dilation=1, name=None):
        super().__init__('MaxPool1d' if name is None else name,
                         'red!20!white')
        if stride is None: stride = kernel
        self.kernel = kernel
        assert stride > 0
        self.stride = stride
        self.padding = padding
        self.dilation = dilation

    def get_output_size(self, node: DataNode):
        n, c, f = node.size_unscaled
        f = (f + 2*self.padding - self.dilation*(self.kernel - 1) - 1)//self.stride + 1
        return n, c, f

    def get_details(self) -> List[str]:
        return [f'${{\\rm kernel}} = {self.kernel}$', f'${{\\rm stride}} = {self.stride}$',
                f'${{\\rm padding}} = {self.padding}$', f'${{\\rm dilation}} = {self.dilation}$']


class Linear(Layer):

    def __init__(self, a, b=None, name=None):
        super().__init__('Linear' if name is None else name,
                         'green!50!white')
        if b is not None:
            self.in_f = a
            self.out_f = b
        else:
            self.in_f = None
            self.out_f = a

    def get_output_size(self, node: DataNode):
        n, c, l = node.size_unscaled
        if self.in_f:
            assert l == self.in_f, f'in {self.__class__.__name__}: {l} != {self.in_f}'
        return n, c, self.out_f

    def get_details(self) -> List[str]:
        inf = 'guess' if self.in_f is None else self.in_f
        return [f'${{\\rm n\\ input\\ features}} = {inf}$', f'${{\\rm n\\ output\\ features}} = {self.out_f}$']


class ReLU(Layer):

    def __init__(self, name=None):
        super().__init__('ReLU' if name is None else name,
                         colour='blue!10!white')

    def get_output_size(self, node: DataNode):
        return node.size_unscaled


class Sigmoid(Layer):

    def __init__(self, name=None):
        super().__init__('Sigmoid' if name is None else name,
                         colour='yellow!50!white')

    def get_output_size(self, node: DataNode):
        return node.size_unscaled


class LeakyReLU(Layer):

    def __init__(self, name=None):
        super().__init__('LeakyReLU' if name is None else name,
                         colour='orange!60!white')

    def get_output_size(self, node: DataNode):
        return node.size_unscaled
