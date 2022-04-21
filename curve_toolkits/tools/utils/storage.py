from os import path
import os


def ensure_exist(path_name):
    if not path.exists(path_name):
        os.makedirs(path_name)
    return path_name
