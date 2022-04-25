import os
from os import path

if __name__ == "__main__":
    str = input("请输入：")
    print("你输入的内容是: ", str)

    _workspace = path.join(os.path.expanduser('~'), 'curve_toolkits/workspace')

    print(path.join(os.path.expanduser('~'), 'curve_toolkits/workspace'))

    template_curves_dir = path.join(_workspace, '111')
    if not path.exists(template_curves_dir):
        os.makedirs(template_curves_dir)
