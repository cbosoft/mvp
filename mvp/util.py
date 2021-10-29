import os
import subprocess as sp
import tempfile


def clean_key(key):
    key = key.replace('_', ' ')
    return key


def pts2tikz(pts, **kws) -> str:
    cmd = '\\draw'
    if kws:
        cmd += '[' + ','.join([f'{clean_key(k)}={v}' for k, v in kws.items()]) + ']'
    return cmd + ' ' + '--'.join([f'({xi}, {yi})' for xi, yi in pts]) + ';'


def runsh(command: str):
    proc = sp.run(command, shell=True, stderr=sp.PIPE, stdout=sp.PIPE)
    if proc.returncode:
        print(proc.stdout)
        print(proc.stderr)
        exit(1)


def compile_tex(tex: str, out_fn: str, latex_command='xelatex', output_tex_too=False):
    with tempfile.TemporaryDirectory() as d:
        os.chdir(d)
        tex_fn = 'dia.tex'
        result_fn = pdf_fn = tex_fn.replace('tex', 'pdf')
        with open(tex_fn, 'w') as f:
            f.write(tex)
        runsh(f'{latex_command} "{tex_fn}"')
        if out_fn[-3:] != 'pdf':
            ext = out_fn[-3:]
            result_fn = result_fn.replace('pdf', ext)
            runsh(f'convert -density 384 "{pdf_fn}" -quality 100 -alpha remove "{result_fn}"')
        runsh(f'cp "{result_fn}" "{out_fn}"')
        if output_tex_too:
            runsh(f'cp "{tex_fn}" "{out_fn[:-4]}.tex"')


class TreeNode:

    def __init__(self, parent=None):
        self.parent = parent
        self.children = []

    @property
    def siblings(self):
        return tuple() if not self.parent else tuple(self.parent.children)

    def get_siblings_and_cousins(self):
        root = self.get_root()
        level = self.get_level()
        rv = root.get_all_children_at_level(level)
        return rv

    def get_all_children_at_level(self, level: int):
        if level != self.get_level():
            rv = []
            for child in self.children:
                rv.extend(child.get_all_children_at_level(level))
            return rv
        return [self]

    def get_root(self):
        if self.parent:
            return self.parent.get_root()
        return self

    def add_child(self, child):
        self.children.append(child)
        self.children = sorted(self.children)
        child.parent = self

    def get_level(self) -> int:
        if self.parent is None:
            return 0
        else:
            return 1 + self.parent.get_level()

    def _gen(self):
        yield self

        for child in self.children:
            for node in child:
                yield node

    def __iter__(self):
        return self._gen()
