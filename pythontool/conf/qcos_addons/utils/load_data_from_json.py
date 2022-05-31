# -*- coding:utf-8 -*-
import json


def load_data_from_json(file_name: str) -> dict:
    '''
    加载json文件为dict
    '''
    f = open(file_name, encoding='utf-8')
    return json.load(f)
