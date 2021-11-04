# MVP: ML Visualised using Python

![scrot1](https://github.com/cbosoft/mvp/blob/master/examples/example_1.png?raw=true)

I find it hard to think about complex topics if I can't visualise them. To aid in developing convolutional neural networks I needed something to visualise the model, so I wrote a python library to do just that.

This python library enables your design of ML models by giving you an accurate representation of the network. You build up the network as a series of blocks, in a similar manner as you might in `pytorch`. Define a basic block, consisting of some layers:

```python
import mvp.layers as nn

def linear_block(in_ch, out_ch, mid_ch):
    return [
        nn.Linear(in_ch, mid_ch),
        nn.ReLU(),
        nn.Linear(mid_ch, out_ch),
        nn.ReLU()
    ]
```

Initialise network visualiser, using the context manager syntax:

```
from mvp import Visualiser
with Visualiser('net.png') as net:
```

Define an input node:

```
    A = net.add_node(1, 5, 9, name='Input')
```

Then we apply our block of layers, and getting the next data node in return:

```
    B = net.apply_layer_to(linear_block(9, 50, 20), A, group='Linear1')
```

We have grouped the nodes involved in this block, and labelled it 'Linear1' - this helps with breaking up the network into larger, more manageable, chunks. We can apply another block of layers to the second data point:

```
    C = net.apply_layer_to(linear_block(50, 5, 20), B, group='Linear2', name='Output')
```

In this way we can build up a network from a series of layers, and at least one starting point.

Complete examples are given in the [examples](examples) dir.

## Backend
The diagrams are drawn in LaTeX+TikZ and therefore are easy to include in scientific papers if need be, or to tweak positions/colours/etc after-the-fact. Native output is in PDF format, but is converted (using imagemagick) to png or any other supported image format.

## Examples

[Example 1:](examples/example_1.py)

![scrot1](https://github.com/cbosoft/mvp/blob/master/examples/example_1.png?raw=true)

[Example 2:](examples/example_2.py)
![scrot2](https://github.com/cbosoft/mvp/blob/master/examples/example_2.png?raw=true)

[Example 3:](examples/example_3.py)
![scrot3](https://github.com/cbosoft/mvp/blob/master/examples/example_3.png?raw=true)
