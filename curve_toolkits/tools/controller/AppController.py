# -*- coding:utf-8 -*-
import os

from .CurveAnalysisController import CurveAnalysisController
from .CurveCompareController import CurveCompareController
from .GenTmplController import GenTmplController
from PyQt5 import QtWidgets  # import PyQt5 widgets
import sys
from ..view import window as main_window
from .TemplateCompareController import TemplateCompareController
from tools.model.Storage.WorkspaceModel import workspace_model
from ..view.Pages.CurveAnalysisPage import CurveAnalysisPage
from ..view.Pages.CurveComparePage import CurveComparePage
from ..view.Pages.TemplateGeneratePage import TemplateGeneratePage


class AppController:

    def __init__(self):
        # Create the application object
        self.app = QtWidgets.QApplication(sys.argv)

        # Create the form object
        self.window = main_window.ToolKitWindow()
        self.init_workspace()

        self.template_compare_controller = TemplateCompareController(self.window)
        curses_cache_path = os.path.join(workspace_model.workspace, 'cache')
        self.gen_tmpl_controller = GenTmplController(TemplateGeneratePage(
            self.window.ui.template_generate_tab,
            self.window,
            cache_path=curses_cache_path
        ))
        self.curve_compare_controller = CurveCompareController(CurveComparePage(
            self.window.ui.curve_compare_tab,
            self.window,
            cache_path=curses_cache_path
        ))
        self.curve_analysis_controller = CurveAnalysisController(CurveAnalysisPage(
            self.window.ui.curve_analysis_tab,
            self.window,
            cache_path=curses_cache_path
        ))

        self.connect_signals()

    def run_app(self):
        # Show form
        self.window.qt_instance.show()

        # Run the program
        sys.exit(self.app.exec())

    def connect_signals(self):
        window = self.window
        ui = window.ui
        ### tab 1 模板对比
        ui.open_btn.clicked.connect(self.template_compare_controller.load_bolt_list)
        ui.load_btn.clicked.connect(self.template_compare_controller.load_online_template)
        ui.load_local_btn.clicked.connect(self.template_compare_controller.load_local_template)
        ui.compare_btn.clicked.connect(self.template_compare_controller.do_compare)
        window.compare_items_table.row_clicked_signal.connect(self.template_compare_controller.set_viewing_template)

    def init_workspace(self):
        workspace_model.set_working_dir()
