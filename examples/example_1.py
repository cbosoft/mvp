from mvp import Visualiser
import mvp.layers as nn


def conv_block(*args):
    return [
        nn.Conv1d(*args),
        nn.ReLU('ReLU'),
        nn.MaxPool1d(2)
    ]


def linear_block(in_f, out_f, mid_f=None):
    if mid_f is None: mid_f = out_f
    return [
        nn.Linear(in_f, mid_f),
        nn.ReLU(),
        nn.Linear(mid_f, out_f),
        nn.Sigmoid()
    ]


with Visualiser('example_1.png') as net:
    inp = net.add_node_1d(1, 25, name='Input')
    after_conv1 = net.apply_layer_to(conv_block(1, 5, 5), inp, group='Conv1')
    after_conv2 = net.apply_layer_to(conv_block(5, 15, 5), after_conv1, group='Conv2')
    out = net.apply_layer_to(linear_block(after_conv2.size_unscaled[-1], 50, 25), after_conv2, name='Output', group='Linear')
