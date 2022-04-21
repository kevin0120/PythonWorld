from typing import Dict, List

import pandas as pd

from tools.view.FileWriter import FileWriter
from tools.model.GenTmplModel import GenTmplModel
from tools.view.FileLoader import FileLoader
import json
from tools.model.Storage.TemplateCurvesStorage import template_curves_storage
from tools.controller.TemplateRenderController import TemplateRenderController
from ..model.Storage.WorkspaceModel import workspace_model
from ..utils.curve import select_curve_from_filesystem
from ..view.Pages.TemplateGeneratePage import TemplateGeneratePage
from ..view.window import ToolKitWindow
from tools.model import local_tmpl
from functools import partial
from tools.utils.result import parse_curve_params_from_results, choose_template_curves_from_result_file
import os
import platform
import subprocess
from os import path


class GenTmplController:
    def __init__(self, page: TemplateGeneratePage):
        self.page = page
        self._gen_tmpl_model = GenTmplModel()
        self.notify = self.page.notify
        self._template_render_controller = TemplateRenderController(
            self.page.items_table,
            self.page.params_table,
            self.page.charts,
            self._gen_tmpl_model,
            self.notify
        )
        self.load_curves_and_params_from_workspace()
        self.page.connect_add_curve(self.add_curve_to_template)
        self.page.connect_open_workspace(GenTmplController.open_workspace)
        self.page.connect_save_param(self.save_param_btn)
        self.page.connect_load_local_tmpl(self.load_local_template)
        self.page.connect_gen_tmpl(self.gen_bolt_tmpl)
        self.page.connect_load_from_results(self.load_curve_params_from_results)
        self.page.connect_set_viewing_template(self.set_viewing_template)
        self.page.connect_params_data_changed(self.params_data_changed)
        self.page.connect_bolt_params_changed(self.bolt_params_changed)

    @staticmethod
    def open_workspace(self):
        path = workspace_model.workspace
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    # 从工作空间加载曲线和参数
    def load_curves_and_params_from_workspace(self):
        try:
            self.notify.info('正在读取工作空间')
            self._gen_tmpl_model.load_workspace()
            self._template_render_controller.update_table_content()
        except Exception as e:
            self.notify.error(repr(e))

    def params_data_changed(self, data: List[Dict]):
        try:
            if len(data) != 2:
                return
            self._gen_tmpl_model.update_curve_param(data[0].get('value'), data[1].get('value'))
            self._template_render_controller.update_table_content()
        except Exception as e:
            self.notify.error(repr(e))

    def bolt_params_changed(self, data: List[Dict]):
        try:
            if len(data) != 2:
                return
            self._gen_tmpl_model.update_bolt_params(data[0].get('value'), data[1].get('value'))
            self._template_render_controller.update_table_content()
        except Exception as e:
            self.notify.error(repr(e))

    def save_param_btn(self):
        try:
            self._gen_tmpl_model.save_curve_param()
        except Exception as e:
            self.notify.error(repr(e))

    def gen_bolt_tmpl(self):
        try:
            self.notify.info('生成曲线模板')
            file_name = FileWriter().save_file("保存模板", "JSON Files (*.json)")
            if not file_name:
                return
            template = self._gen_tmpl_model.encode_templates()
            with open(file_name, "w") as f:
                vv = json.dumps(template, indent=4, sort_keys=True)
                f.write(vv)
        except Exception as e:
            self.notify.error(repr(e))

    def add_curve_to_template(self):
        try:
            bolt_number = self._gen_tmpl_model.current_bolt
            if bolt_number is None:
                raise Exception('没有选中的螺栓')
            file_name = select_curve_from_filesystem("加载{}曲线".format(bolt_number))
            self.notify.info("加载曲线文件: {}, 螺栓编号: {}".format(file_name, bolt_number))
            template_curves_storage.save_curve(bolt_number, file_name)
            self.load_curves_and_params_from_workspace()
            self.set_viewing_template(bolt_number)
        except Exception as e:
            self.notify.error(repr(e))

    def load_local_template(self):
        try:
            file_name = FileLoader().open_file(
                "加载本地模板文件", "All Files (*);;JSON Files (*.json)")
            local_tmpl.read_local_tmpl(file_name)
            self._gen_tmpl_model.load_local_templates()
            self._template_render_controller.update_table_content()
        except Exception as e:
            self.notify.error(repr(e))

    def set_viewing_template(self, bolt: str):
        try:
            self._template_render_controller.set_viewing_template(bolt)
            self.page.bolt_params_table.render_content(self._gen_tmpl_model.render_bolt_params_table)

            def on_delete(bolt_number):
                self.load_curves_and_params_from_workspace()
                self.set_viewing_template(bolt_number)

            self.page.template_curves_table.render_content(self._gen_tmpl_model.render_curves_table(
                partial(on_delete, self._gen_tmpl_model.current_bolt)
            ))
        except Exception as e:
            self.notify.error(repr(e))

    def load_curve_params_from_results(self):
        file_name = FileLoader().open_file(
            "选择结果文件",
            "All Files (*);;CSV Files (*.csv);;",
            initialFilter='CSV Files (*.csv)')
        results = pd.read_csv(file_name)
        self.notify.info('结果已读取')
        bolts_data = parse_curve_params_from_results(results)
        self.notify.info(f'检测到{len(bolts_data.keys())}个螺栓')
        dir = FileLoader().open_directory("选择曲线文件夹")
        for bolt, bolt_data in bolts_data.items():
            self.notify.info(f'正在添加螺栓{bolt}')
            entity_ids = choose_template_curves_from_result_file(results, bolt)
            curve_files = [path.join(dir, f'{entity_id}.csv') for entity_id in entity_ids]
            self._gen_tmpl_model.add_bolt(bolt_number=bolt, bolt_data=bolt_data, curve_files=curve_files)

        self.notify.info('螺栓添加完成')
        self.load_curves_and_params_from_workspace()
        pass
