import tempfile
import os

from .data_block import DataBlock
from .action_block import ActionBlock


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

    def __init__(self, fn: str, *, output_tex_too=False):
        self.blocks = []
        self.fn = os.path.abspath(fn)
        self.output_tex_too = output_tex_too

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.draw()

    def add_block(self, block):
        if not self.blocks or isinstance(self.blocks[-1], ActionBlock):
            assert isinstance(block, DataBlock)
        else:
            assert isinstance(block, ActionBlock)
        self.blocks.append(block)
        return block

    def draw(self):
        tex = str(self.LATEX_HEAD)
        pos = [0, 0]
        for i, block in enumerate(self.blocks):
            if isinstance(block, DataBlock):
                btex = block.to_tex(pos)
            else:
                prv = self.blocks[i-1]
                nxt = self.blocks[i+1]
                btex = block.to_tex(pos, prv, nxt)
            tex = tex + '\n' + btex
        tex += '\n' + self.LATEX_TAIL

        with tempfile.TemporaryDirectory() as d:
            os.chdir(d)
            tex_fn = 'dia.tex'
            tex_out_fn = tex_fn.replace('tex', 'pdf')
            with open(tex_fn, 'w') as f:
                f.write(tex)
            self.runsh(f'{self.LATEX_COMMAND} "{tex_fn}"')
            if self.fn[-3:] != 'pdf':
                ext = self.fn[-4:]
                self.runsh(f'convert -density 384 "{tex_out_fn}" -quality 100 "{tex_out_fn}{ext}"')
                tex_out_fn = tex_out_fn + ext
            self.runsh(f'cp "{tex_out_fn}" "{self.fn}"')
            if self.output_tex_too:
                self.runsh(f'cp "{tex_fn}" "{self.fn[:-4]}.tex"')

    def runsh(self, command):
        print(command)
        os.system(command)
