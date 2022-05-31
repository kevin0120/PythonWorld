import argparse
import os
from typing import Callable

# https://blog.csdn.net/qq_41629756/article/details/105689494

from importlib import import_module


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ImportError(f"{dotted_path} doesn't look like a module path")

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError(f'Module "{module_path}" does not define a "{class_name}" attribute/class')


def lazy_load_command(import_path: str) -> Callable:
    """Create a lazy loader for command"""
    _, _, name = import_path.rpartition('.')

    def command(*args, **kwargs):
        func = import_string(import_path)
        return func(*args, **kwargs)

    command.__name__ = name

    return command


def add(args):
    r = args.x + args.y
    print('x + y = ', r)


def sub(args):
    r = args.x - args.y
    print('x - y = ', r)


if __name__ == '__main__':
    print(os.environ)
    parser = argparse.ArgumentParser(prog='PROG')

    subparsers = parser.add_subparsers(dest='subcommand', metavar="GROUP_OR_COMMAND")
    subparsers.required = True

    # subparsers = parser.add_subparsers(help='sub-command help')
    # 添加子命令 add
    parser_a = subparsers.add_parser('add', help='add help')

    parser_a.add_argument('-x', type=int, default=5, help='x value')
    parser_a.add_argument('-y', type=int, default=5, help='y value')
    parser_a.add_argument('-b', action='store_true')

    # 设置默认函数
    # parser_a.set_defaults(func=add)
    parser_a.set_defaults(func=lazy_load_command('pythontool.conf.command.hello.add'))

    # 添加子命令 sub
    parser_s = subparsers.add_parser('sub', help='sub help')
    parser_s.add_argument('-x', type=int, help='x value')
    parser_s.add_argument('-y', type=int, help='y value')
    # 设置默认函数
    # parser_s.set_defaults(func=sub)
    parser_s.set_defaults(func=lazy_load_command('pythontool.conf.command.hello.sub'))
    args = parser.parse_args()
    # 执行函数功能
    args.func(args)
