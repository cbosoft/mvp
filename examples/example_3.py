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


with Visualiser('example_3.png') as net:
    A = net.add_node_1d(1, 25, name='Input A')
    a1 = net.apply_layer_to(conv_block(1, 5, 3), A, group='Conv A1')
    a2 = net.apply_layer_to(conv_block(5, 10, 3), a1, group='Conv A2')

    net.group(A, A, a2, a2, name='Feature detector (A)', zorder=-1, colour=f'yellow!10!white', margin=(-0.3, 0.7), label_pos='upper right')

    B = net.add_node_1d(1, 25, name='Input B')
    b1 = net.apply_layer_to(conv_block(1, 5, 3), B, group='Conv B1')
    b2 = net.apply_layer_to(conv_block(5, 10, 3), b1, group='Conv B2')
    net.group(B, B, b2, b2, name='Feature detector (B)', zorder=-1, colour=f'blue!10!white', margin=(-0.3, 0.7), label_pos='lower right')

    assert a2.size_unscaled[1] == b2.size_unscaled[1]
    C = net.add_node_1d(a2.size_unscaled[1], a2.size_unscaled[2]+b2.size_unscaled[2])
    net.connect(b2, C, name='Concatenate features')
    net.connect(a2, C, name='Concatenate features')
    D = net.apply_layer_to(conv_block(C.size_unscaled[1], 1, 3), C, group='Conv C1')
    E = net.add_node(*D.size_unscaled)
    net.connect(D, E)
    e1 = net.apply_layer_to(conv_block(1, 1, 3), E, group='Conv E1')
    e2 = net.apply_layer_to(linear_block(100, 20), e1, group='Linear E2')
    F = net.add_node(*D.size_unscaled)
    net.connect(D, F)
    f1 = net.apply_layer_to(conv_block(1, 1, 3), F, group='Conv F1')
    f2 = net.apply_layer_to(linear_block(100, 20), f1, group='Linear F2')
