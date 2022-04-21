from os import path
import os

from typing import List
from shutil import copyfile
from tools.utils.curve import is_curve_valid, read_file, curve_df_to_dict
from tools.utils.storage import ensure_exist
from .MixinStorage import MixinStorage


class TemplateCurvesStorage(MixinStorage):
    _sub_path = 'template_curves'

    def get_bolt_path(self, bolt_number: str):
        bolt_path = path.join(self.storage_dir, bolt_number.replace('/', '@'))
        return ensure_exist(bolt_path)

    def save_curve(self, bolt_number, curve_file, curve_name: str = None):
        if curve_file is None:
            raise Exception('曲线文件未指定，无法保存曲线')
        if bolt_number is None:
            raise Exception('螺栓编号未指定，无法保存曲线')
        if not is_curve_valid(curve_path=curve_file):
            raise Exception('{}不是可用曲线'.format(curve_file))
        copyfile(
            curve_file,
            path.join(
                self.get_bolt_path(bolt_number),
                path.basename(curve_file) if not curve_name else '{}.csv'.format(curve_name)
            )
        )

    @property
    def stored_bolts(self):
        return os.listdir(self.storage_dir)

    def bolt_curves(self, bolt: str):
        return os.listdir(self.get_bolt_path(bolt))

    def load_curves(self, bolts: List[str] = None):
        curves = {}
        for bolt in self.stored_bolts:
            if bolts and bolt not in bolts:
                continue
            curves[bolt] = self.bolt_curves(bolt)
        return curves

    def read_curve_data(self, bolt: str, files: List[str]):
        if type(files) != list:
            return {}
        base_path = self.get_bolt_path(bolt)
        curves = {}
        for file_name in files:
            try:
                full_path = path.join(base_path, file_name)
                curves_dict = curve_df_to_dict(read_file(full_path))
                curves[file_name] = curves_dict
            except KeyError as e:
                raise Exception('读取曲线数据失败:曲线没有需要的列{}，螺栓：{}，文件：{}'.format(e, bolt, file_name))
            except Exception as e:
                raise Exception('读取曲线数据失败:{}，螺栓：{}，文件：{}'.format(repr(e), bolt, file_name))
        return curves

    def delete_curves(self, bolt: str, files: List[str]):
        base_path = self.get_bolt_path(bolt)
        for curve in files:
            full_path = path.join(base_path, curve)
            os.remove(full_path)


template_curves_storage = TemplateCurvesStorage()
