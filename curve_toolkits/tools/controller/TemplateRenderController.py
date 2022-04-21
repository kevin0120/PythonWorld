# -*- coding: utf-8 -*-

from functools import partial

from PyQt5 import QtWidgets
from tools.model.curve_renderer import get_series_by_type, set_curves
from tools.model.TemplateRenderModel import TTemplateRenderModel
from tools.view.table import ToolkitTable
from tools.view.notify import ToolkitNotify
import pandas as pd
from PyQt5.QtWidgets import QPushButton


class TemplateRenderController:
    def __init__(self, item_table: ToolkitTable, param_table: ToolkitTable, curves_view: dict,
                 template_render_model: TTemplateRenderModel, notify: ToolkitNotify, action_handler=None):
        self.item_table = item_table
        self.param_table = param_table
        self.curves_view: dict = curves_view
        self._model = template_render_model
        self._action_handler = action_handler
        self.notify = notify

    def replace_action_button(self, data: pd.DataFrame) -> pd.DataFrame:
        result = data
        for idx, item in result.iterrows():
            t = QPushButton()
            f = partial(self._action_handler, item['编号'])
            t.clicked.connect(f)
            # t.setText('导入{}曲线'.format(item['编号']))
            t.setText('导入曲线')
            result.loc[idx, '动作'] = t
        return result

    def update_table_content(self):
        compare_result: pd.DataFrame = self._model.get_table_content()
        # col_names = compare_result.columns.values.tolist()
        d = compare_result
        # if '动作' in col_names:
        #     d = self.replace_action_button(compare_result)
        self.item_table.render_content(d)
        header = self.item_table.table_instance.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    def set_viewing_template(self, bolt: str):
        self.notify.info('正在查看螺栓：{}'.format(bolt))
        param_table = self.param_table
        self._model.set_current_bolt(bolt)
        params = self._model.render_curve_params
        param_table.render_content(params)
        curves = self._model.render_curves
        set_curves(curves)

        for curve_type, curve_view in self.curves_view.items():
            series = get_series_by_type(curve_type)
            curve_view.set_series(series)
