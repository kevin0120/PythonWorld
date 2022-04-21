from functools import partial
from loguru import logger
import pandas as pd
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QPushButton, QTableWidget, QCheckBox, QTextBrowser
from PyQt5 import QtWidgets

from .Page import Page
from .. import notify, table
from ..Chart import Chart
from ..table import ToolkitTable


class TemplateGeneratePage(Page):
    """
        模板生成页面
    """

    def __init__(self, *args, cache_path='', **kwargs):
        super(TemplateGeneratePage, self).__init__(*args, **kwargs)

        charts = {
            'angle_torque': self.ui.findChild(QWebEngineView, name='webContentView_4'),
            'time_torque': self.ui.findChild(QWebEngineView, name='webContentView_5'),
            'time_angle': self.ui.findChild(QWebEngineView, name='webContentView_6'),
        }
        self.charts = {}
        for key, val in charts.items():
            c = Chart(val, key, cache_path)
            c.show()
            self.charts.update({key: c})

        self.open_workspace_btn: QPushButton = self.ui.findChild(QPushButton, name='open_workspace_btn')
        self.save_param_btn: QPushButton = self.ui.findChild(QPushButton, name='save_param_btn')
        self.add_curve_button: QPushButton = self.ui.findChild(QPushButton, name='add_curve_button')

        self.notify: notify.ToolkitNotify = notify.ToolkitNotify(self.ui.findChild(QTextBrowser, name='textLog_2'))
        self.template_curves_table: table.ToolkitTable = table.ToolkitTable(
            self.ui.findChild(QTableWidget, name='template_curves_table'))
        self.items_table: table.ToolkitTable = table.ToolkitTable(self.ui.findChild(QTableWidget, name='tableWidget_2'))
        self.params_table: table.ToolkitTable = table.ToolkitTable(
            self.ui.findChild(QTableWidget, name='tableParams_2'))
        self.bolt_params_table: table.ToolkitTable = table.ToolkitTable(
            self.ui.findChild(QTableWidget, name='bolt_params_table'))


    def connect_load_local_tmpl(self, handler):
        self.ui.findChild(QPushButton, name='load_local_tmpl_btn').clicked.connect(handler)

    def connect_gen_tmpl(self, handler):
        self.ui.findChild(QPushButton, name='gen_tmpl_btn').clicked.connect(handler)

    def connect_load_from_results(self, handler):
        self.ui.findChild(QPushButton, name='load_from_results_btn').clicked.connect(handler)

    def connect_set_viewing_template(self, handler):
        self.items_table.row_clicked_signal.connect(handler)

    def connect_params_data_changed(self, handler):
        self.params_table.cell_edited_signal.connect(handler)

    def connect_bolt_params_changed(self, handler):
        self.bolt_params_table.cell_edited_signal.connect(handler)

    def connect_open_workspace(self, handler):
        self.open_workspace_btn.clicked.connect(handler)

    def connect_save_param(self, handler):
        self.save_param_btn.clicked.connect(handler)

    def connect_add_curve(self, handler):
        self.add_curve_button.clicked.connect(handler)