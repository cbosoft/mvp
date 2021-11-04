from .layer import Layer
from .data_node import DataNode


class Conv1d(Layer):

    def __init__(self, in_ch, out_ch, kernel, stride=1, padding=0, dilation=1, name=None):
        super().__init__('Conv1d' if name is None else name)
        self.in_ch = in_ch
        self.out_ch = out_ch
        self.kernel = kernel
        self.stride = stride
        self.padding = padding
        self.dilation = dilation

    def get_output_size(self, node: DataNode):
        n, c, l = node.size_unscaled
        assert c == self.in_ch, f'{c} != {self.in_ch}'
        c = self.out_ch
        l = (l + 2*self.padding - self.dilation*(self.kernel - 1) - 1)//self.stride + 1
        return n, c, l


class MaxPool1d(Layer):

    def __init__(self, kernel, stride=None, padding=1, dilation=1, name=None):
        super().__init__('MaxPool1d' if name is None else name,
                         'red!20!white')
        if stride is None: stride = kernel
        self.kernel = kernel
        assert stride > 0
        self.stride = stride
        self.padding = padding
        self.dilation = dilation

    def get_output_size(self, node: DataNode):
        n, c, l = node.size_unscaled
        l = (l + 2*self.padding - self.dilation*(self.kernel - 1) - 1.0001)//self.stride + 1
        return n, c, l


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
            assert l == self.in_f, f'{l} != {self.in_f}'
        return n, c, self.out_f


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
