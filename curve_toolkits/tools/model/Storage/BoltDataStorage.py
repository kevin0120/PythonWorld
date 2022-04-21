from os import path
import os

from typing import List
from .MixinStorage import MixinStorage
import json
from tools.utils.params import is_bolt_data_valid


class BoltDataStorage(MixinStorage):
    _sub_path = 'bolt_data'

    def save_bolt_data(self, bolt_number, bolt_data: dict):
        if bolt_data is None:
            raise Exception('曲线参数未指定，无法保存参数')
        if bolt_number is None:
            raise Exception('螺栓编号未指定，无法保存参数')
        if not is_bolt_data_valid(bolt_data):
            raise Exception('{}不是可用参数'.format(repr(bolt_data)))
        save_file = path.join(
            self.storage_dir,
            '{}.json'.format(bolt_number)
        )
        with open(save_file, 'w', encoding="utf8") as file:
            file.write(json.dumps(bolt_data, sort_keys=True, indent=4))

    @property
    def data_files(self):
        return os.listdir(self.storage_dir)

    @property
    def stored_bolts(self):
        files = os.listdir(self.storage_dir)
        return list(map(lambda f: path.splitext(f)[0], files))

    def load_bolt_data(self, bolts: List[str] = None):
        data = {}
        for file_name in self.data_files:
            bolt = path.splitext(file_name)[0]
            if bolts is not None and bolt not in bolts:
                continue
            with open(path.join(self.storage_dir, file_name), 'r') as file:
                data[path.splitext(file_name)[0]] = file.read()
        return data


bolt_data_storage = BoltDataStorage()
