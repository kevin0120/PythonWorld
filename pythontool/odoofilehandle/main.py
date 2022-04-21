

import compileall
import os

paths = [r'C:\workspace\odoo-enterprise', r'C:\workspace\sa_addons']


def _remove_path_py_file(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            ex = os.path.split(name)[1]
            fn, ap = os.path.splitext(ex)
            # print(fn, ap)
            if ap != '.py' or fn in ['__init__', '__manifest__', '__openerp__']:
                continue
            p = os.path.join(root, name)
            print(p)
            os.remove(p)


if __name__ == '__main__':
    for path in paths:
        compileall.compile_dir(path, force=True)
        _remove_path_py_file(path)
