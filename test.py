from mvp import Visualiser, DataNode1D

with Visualiser('test.pdf') as mvp:
    i = mvp.add_node_1d(1, 100, name='InputA')
    i2 = mvp.add_node_1d(2, 50)
    i3 = mvp.add_node_1d(2, 50, name='Input B')
    i4 = mvp.add_node_1d(4, 30)
    f = mvp.add_node_1d(1, 100)
    o = mvp.add_node_1d(1, 10, name='Output')

    mvp.connect(i, i2, name='Conv1')
    mvp.connect(i2, f, name='Conv2')
    mvp.connect(i3, i4, name='foo')
    mvp.connect(i4, f, name='Conv3')
    mvp.connect(f, o, name='Linear')
