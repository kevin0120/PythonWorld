import io
import os
import sys

from pythontool.conf.configration.configuration import conf


def show_config():
    """Show current application configuration"""
    with io.StringIO() as output:
        conf.write(output)
        code = output.getvalue()
        print(code)


a = 5

if __name__ == '__main__':
    print(sys.path)
    print(globals())
    print(locals())
    print("world###########################################################")
    print(os.environ)
    show_config()
