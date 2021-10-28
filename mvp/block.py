class Block:

    @staticmethod
    def clean_key(key):
        key = key.replace('_', ' ')
        return key

    @classmethod
    def pts2tikz(cls, pts, **kws) -> str:
        cmd = '\\draw'
        if kws:
            cmd += '[' + ','.join([f'{cls.clean_key(k)}={v}' for k, v in kws.items()]) + ']'
        return cmd + ' ' + '--'.join([f'({xi}, {yi})' for xi, yi in pts]) + ';'

    def to_tex(self, pos: list) -> str:
        raise NotImplementedError
