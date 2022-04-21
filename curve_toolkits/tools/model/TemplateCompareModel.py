# -*- coding: utf-8 -*-
from typing import List

import pandas as pd
from tools.model.online_tmpl import get_online_templates
from tools.model.local_tmpl import get_local_templates
from tools.model.TemplateRenderModel import TemplateRenderModel
from jsoncomparison import Compare, NO_DIFF
from tools.utils.params import param_to_float
import json


def do_compare(local_tmpl, online_tmpl):
    # TODO: 实现模板和参数的对比
    try:
        local_data = json.loads(local_tmpl)
        local_data.update({
            'curve_param': param_to_float(local_data.get('curve_param'))
        })
        online_data = json.loads(online_tmpl)
        online_data.update({
            'curve_param': param_to_float(online_data.get('curve_param'))
        })
        diff = Compare().check(json.dumps(local_data), json.dumps(online_data))
        is_diff = diff != NO_DIFF
        return is_diff, diff
    except Exception as e:
        return True, {'error': str(e)}


class TemplateCompareModel(TemplateRenderModel):
    def __init__(self):
        super().__init__(
            index_column='编号',
            template_columns=['在线', '本地'],
            extra_columns=['差异', '差异详情']
        )

    def load_local_templates(self):
        local = get_local_templates()
        self.load_templates(local, '本地')

    def load_online_templates(self):
        online = get_online_templates()
        self.load_templates(online, '在线')

    def compare_templates(self):
        templates = self.templates
        for bolt in templates.index:
            is_diff, diff_detail = do_compare(
                templates['本地'].get(bolt),
                templates['在线'].get(bolt)
            )
            templates.loc[bolt, '差异'] = '差异' if is_diff else '一致'
            templates.loc[bolt, '差异详情'] = json.dumps(diff_detail)

    def get_table_content(self, columns: List[str] = None) -> pd.DataFrame:
        result = super(TemplateCompareModel, self).get_table_content(['编号', '本地', '在线', '差异'])
        is_loaded = lambda x: '已加载' if not pd.isnull(x) else '未加载'
        result['本地'] = result['本地'].map(is_loaded)
        result['在线'] = result['在线'].map(is_loaded)
        return result
