from mvp import Visualiser, DataBlock1D, ActionBlock

with Visualiser('test.png') as mvp:
    mvp.add_block(DataBlock1D(1, 100, name='Input'))
    mvp.add_block(ActionBlock('Conv1'))
    mvp.add_block(DataBlock1D(2, 50))
    mvp.add_block(ActionBlock('Conv2'))
    mvp.add_block(DataBlock1D(1, 20, name='Features'))
    mvp.add_block(ActionBlock('Linear', colour='yellow!50!white'))
    mvp.add_block(DataBlock1D(1, 10, name='Output'))
