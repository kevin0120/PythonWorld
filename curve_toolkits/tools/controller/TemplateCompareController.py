# -*- coding:utf-8 -*-

from tools.controller.TemplateRenderController import TemplateRenderController
from tools.model.TemplateCompareModel import TemplateCompareModel
from tools.view.FileLoader import FileLoader
from tools.model import online_tmpl, local_tmpl
from loguru import logger
from tools.model.AnalysisBoltsModel import AnalysisBoltsModel
from tools.view.window import ToolKitWindow


class TemplateCompareController:
    def __init__(self, window: ToolKitWindow):
        self.window: ToolKitWindow = window
        self._template_compare_model = TemplateCompareModel()
        self._analysis_bolts_model = AnalysisBoltsModel()
        self._template_render_controller = TemplateRenderController(
            self.item_table,
            self.param_table,
            self.curves_view,
            self._template_compare_model,
            self.window.notify_box
        )

    @property
    def param_table(self):
        return self.window.params_table

    @property
    def item_table(self):
        return self.window.compare_items_table

    @property
    def curves_view(self):
        return self.window.template_compare_charts

    def load_bolt_list(self):
        try:
            file_name = FileLoader().open_file(
                "打开编号文件",
                "All Files (*);;CSV Files (*.csv);;Excel Files (*.xlst)"
            )
            logger.info("打开编号文件: {}".format(file_name))
            bolts = self._analysis_bolts_model.read_analysis_bolts(file_name)
            self._template_compare_model.set_bolts(bolts)
            self._template_render_controller.update_table_content()
        except Exception as e:
            self.window.notify_box.error(repr(e))

    def load_local_template(self):
        try:
            file_name = FileLoader().open_file(
                "加载本地模板文件", "All Files (*);;JSON Files (*.json)")
            local_tmpl.read_local_tmpl(file_name)
            self._template_compare_model.load_local_templates()
            self._template_render_controller.update_table_content()
        except Exception as e:
            self.window.notify_box.error(repr(e))
            raise e

    def load_online_template(self):
        try:
            file_name = FileLoader().open_file(
                "加载在线模板文件", "All Files (*);;JSON Files (*.json)")
            online_tmpl.read_online_tmpl(file_name)
            self._template_compare_model.load_online_templates()
            self._template_render_controller.update_table_content()
        except Exception as e:
            self.window.notify_box.error(repr(e))

    def do_compare(self):
        try:
            window = self.window
            window.notify_box.info("开始比对模板")
            self._template_compare_model.compare_templates()
            self._template_render_controller.update_table_content()
            window.notify_box.info("模板比对已完成")
        except Exception as e:
            self.window.notify_box.error(repr(e))

    def set_viewing_template(self, bolt: str):
        self._template_render_controller.set_viewing_template(bolt)
