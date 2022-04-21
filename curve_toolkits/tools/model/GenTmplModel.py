# -*- coding: utf-8 -*-
import pandas as pd
from tools.model.TemplateRenderModel import TemplateRenderModel
from tools.model.local_tmpl import get_local_templates
from tools.utils.curve import template_dict_to_sdk_dict
from .Storage.BoltDataStorage import bolt_data_storage
from tools.model.Storage.TemplateCurvesStorage import template_curves_storage
import json
from sdk.sdk import doCACurveEncodeMultiple
from sdk.structs import clusterCStructure2Dict
from loguru import logger
from typing import List, Dict
from uuid import uuid3, NAMESPACE_DNS
from PyQt5.QtWidgets import QPushButton


def render_dict_to_df(dict_data, key_header='参数', value_header='值'):
    df = pd.DataFrame([dict_data]).T
    df.rename(columns={0: value_header}, inplace=True)
    result = df.reset_index()
    result.rename(columns={'index': key_header}, inplace=True)
    return result


def remove_curve_button(bolt, curve_file_name, on_click):
    t = QPushButton()

    def on_button_clicked():
        template_curves_storage.delete_curves(bolt, [curve_file_name])
        on_click()

    t.clicked.connect(on_button_clicked)
    t.setText('删除')
    return t


class GenTmplModel(TemplateRenderModel):
    def __init__(self):
        super().__init__(
            index_column='编号',
            template_columns=['本地'],
            extra_columns=['工艺类型', '参数', '曲线', '工厂代码']
        )

    @property
    def default_params(self):
        return {
            'angle_threshold': 0.075,
            'angle_up_limit_max': 11.0,
            'angle_up_limit_min': 3.0,
            'sampling_time': 0.02,
            'slope_threshold': 20.0,
            'threshold': 0.3,
            'torque_low_limit': 1.0,
            'torque_threshold': 2.5,
            'torque_up_limit_max': 28.0,
            'torque_up_limit_min': 22.0
        }

    def load_workspace(self):
        params = pd.DataFrame([], columns=['编号', '参数', '工艺类型'])
        for key, val in bolt_data_storage.load_bolt_data().items():
            bolt_data = json.loads(val)
            params = params.append({
                '编号': key,
                '参数': json.dumps(bolt_data.get('curve_param', None)),
                '工艺类型': bolt_data.get('craft_type')
            }, ignore_index=True)
        params = params.set_index('编号')
        self.update(params)
        curves = pd.DataFrame([], columns=['编号', '曲线'])
        for key, val in template_curves_storage.load_curves().items():
            # if not val or len(val) == 0:
            #     val = None
            curves = curves.append({
                '编号': key,
                '曲线': val
            }, ignore_index=True)
        curves = curves.set_index('编号')
        self.update(curves)
        # return

    def load_local_templates(self):
        templates = get_local_templates()
        # self.load_templates(local, '本地')
        params = pd.DataFrame([], columns=['编号', '参数', '工艺类型'])
        for k, template in templates.items():
            try:
                bolt = k.split('/')[0]
                curve_param = template.get('curve_param', None)
                craft_type = template.get('craft_type', None)
                if not bolt:
                    continue
                # template_cluster = template.get('template_cluster', None)
                params = params.append({
                    '编号': bolt,
                    '参数': json.dumps(curve_param),
                    '工艺类型': int(craft_type)
                }, ignore_index=True)
                bolt_data_storage.save_bolt_data(bolt, bolt_data={
                    'craft_type': int(craft_type),
                    'curve_param': curve_param
                })
            except Exception as e:
                logger.error(e)
                continue
        params = params.set_index('编号')
        self.update(params)

    def get_table_content(self, columns: List[str] = None) -> pd.DataFrame:
        if columns:
            return super().get_table_content(columns)
        result = super().get_table_content(['编号', '工艺类型', '参数', '曲线'])
        result['参数'] = result['参数'].map(
            lambda x: '已加载' if x and not (not isinstance(x, list) and pd.isnull(x)) else '未加载')
        result['曲线'] = result['曲线'].map(lambda x: len(x) if x and type(x) == list else 0)
        return result

    def get_curve_params(self, bolt: str, to_json=False):
        json_data = self.templates.loc[bolt, '参数']
        if pd.isnull(json_data):
            json_data = json.dumps(self.default_params)
        if to_json:
            return json_data
        if pd.isnull(json_data):
            json_data = '{}'
        data = json.loads(json_data)
        return render_dict_to_df(data)

    def get_curves(self, bolt: str):
        curve_files = self.templates.loc[bolt, '曲线']
        if not curve_files or (type(curve_files) != list and pd.isnull(curve_files)):
            return {}
        return template_curves_storage.read_curve_data(bolt, curve_files)

    def encode_templates(self):
        templates = {}
        for bolt, data in self.templates.iterrows():
            try:
                if pd.isnull(data['参数']) or not data['曲线']:
                    raise Exception('参数或曲线缺失')
                curves = list(map(template_dict_to_sdk_dict, self.get_curves(bolt).values()))
                if len(curves) == 0:
                    raise Exception('模板曲线为空')
                craft_type = data['工艺类型']
                if not craft_type or pd.isnull(craft_type):
                    raise Exception('未指定工艺类型')
                curve_mode = 0
                curve_param = json.loads(data['参数'])
                template, new_param = doCACurveEncodeMultiple(
                    bolt_number=bolt,
                    craft_type=craft_type,
                    mode=curve_mode,
                    curve_param=curve_param,
                    curve_meta_data=curves,
                    final_angles=list(map(lambda c: 0, curves)),
                    final_torques=list(map(lambda c: 0, curves))
                )
                template_dict = clusterCStructure2Dict(template)
                key = '{}/{}'.format(bolt, craft_type)
                template_name = '{}@@{}'.format(key, uuid3(NAMESPACE_DNS, key))
                templates.update({
                    template_name: {
                        'craft_type': craft_type,
                        'nut_no': bolt,
                        'curve_param': new_param,
                        'template_cluster': {
                            str(curve_mode): template_dict
                        }
                    }
                })
            except Exception as e:
                logger.error('螺栓{}模板生成错误：{}'.format(bolt, e))
                continue
        return templates

    @property
    def render_bolt_params_table(self):
        return render_dict_to_df({
            '工艺类型': self.get_current_row_data('工艺类型')
        })

    def render_curves_table(self, on_delete):
        curves = self.get_current_row_data('曲线')
        curves = curves if type(curves) == list else []
        return pd.DataFrame({
            '曲线': curves,
            '动作': list(map(lambda c: remove_curve_button(self.current_bolt, c, on_delete), curves))
        })

    def update_curve_param(self, key, value):
        params = self.get_current_row_data('参数')
        if pd.isnull(params):
            data = self.default_params
        else:
            data = json.loads(params)
        data[key] = float(value)
        self.set_current_row_data('参数', json.dumps(data))

    def update_bolt_params(self, key, value):
        if key == '工艺类型':
            self.set_current_row_data(key, int(value))  # fixme

    def save_curve_param(self):
        logger.info('保存修改的模板参数 螺栓编号: {}'.format(self.current_bolt))
        params = json.loads(self.get_curve_params(self.current_bolt, to_json=True))
        craft_type = int(self.get_current_row_data('工艺类型'))
        bolt_data_storage.save_bolt_data(self.current_bolt, bolt_data={
            'craft_type': craft_type,
            'curve_param': params
        })

    def add_bolt(self, bolt_number: str, bolt_data: Dict = None, curve_files: List[str] = None):
        """
        添加螺栓到本地工作空间
        """
        assert bolt_number, "螺栓编号不能为空"
        if not bolt_data:
            bolt_data = {
                'craft_type': 1,
                'curve_param': self.default_params
            }

        bolt_data_storage.save_bolt_data(bolt_number, bolt_data)
        if curve_files and len(curve_files) > 0:
            for file in curve_files:
                try:
                    template_curves_storage.save_curve(bolt_number, file)
                except Exception as e:
                    logger.error(e)


