import os
import subprocess as sp
import tempfile


def clean_key(key):
    key = key.replace('_', ' ')
    return key


def pts2tikz(pts, *args, **kws) -> str:
    cmd = '\\draw'
    if kws:
        cmd += '[' + ','.join(args) + ','.join([f'{clean_key(k)}={v}' for k, v in kws.items()]) + ']'
    return cmd + ' ' + '--'.join([f'({xi}, {yi})' for xi, yi in pts]) + ';'


def runsh(command: str):
    proc = sp.run(command, shell=True, stderr=sp.PIPE, stdout=sp.PIPE)
    if proc.returncode:
        print(proc.stdout.decode())
        print(proc.stderr.decode())
        exit(1)


def compile_tex(tex: str, out_fn: str, latex_command='xelatex', output_tex_too=False, convert='convert'):
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
            runsh(f'{convert} -density 384 "{pdf_fn}" -quality 100 -alpha remove "{result_fn}"')
        runsh(f'cp "{result_fn}" "{out_fn}"')
        if output_tex_too:
            runsh(f'cp "{tex_fn}" "{out_fn[:-4]}.tex"')
