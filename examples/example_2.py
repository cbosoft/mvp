from mvp import Visualiser
import mvp.layers as nn


def conv_block(*args):
    return [
        nn.Conv1d(*args),
        nn.ReLU('ReLU'),
        nn.MaxPool1d(2)
    ]


def linear_block(out_f, mid_f=None):
    if mid_f is None: mid_f = out_f
    return [
        nn.Linear(mid_f),
        nn.ReLU(),
        nn.Linear(mid_f, out_f),
        nn.Sigmoid()
    ]


with Visualiser('example_2.png') as net:
    A = net.add_node_1d(1, 25, name='Input A')
    a1 = net.apply_layer_to(conv_block(1, 5, 3), A, group='Conv A1')
    a2 = net.apply_layer_to(conv_block(5, 10, 3), a1, group='Conv A2', name='AF')

    B = net.add_node_1d(1, 25, name='Input B')
    b1 = net.apply_layer_to(conv_block(1, 5, 3), B, group='Conv B1')
    b2 = net.apply_layer_to(conv_block(5, 10, 3), b1, group='Conv B2', name='BF')

    assert a2.size_unscaled[1] == b2.size_unscaled[1]
    C = net.add_node_1d(a2.size_unscaled[1], a2.size_unscaled[2]+b2.size_unscaled[2])
    net.connect(b2, C)
    net.connect(a2, C)
    c1 = net.apply_layer_to(conv_block(C.size_unscaled[1], 1, 3), C, group='Conv C1')
    out = net.apply_layer_to(linear_block(50, 25), c1, name='Output', group='Linear')
