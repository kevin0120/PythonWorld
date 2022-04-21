from functools import partial
from loguru import logger
import pandas as pd
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QPushButton, QTableWidget, QCheckBox
from PyQt5 import QtWidgets

from .Page import Page
from ..Chart import Chart
from ..table import ToolkitTable


class CurveComparePage(Page):
    """
        曲线对比页面
    """

    def __init__(self, *args, cache_path='', **kwargs):
        super(CurveComparePage, self).__init__(*args, **kwargs)
        self.add_curve_btn: QPushButton = self.ui.findChild(QPushButton, name='btnAddCurveToCompare')
        self.remove_curve_btn: QPushButton = self.ui.findChild(QPushButton, name='btnRemoveCurveFromCompare')
        self._table_headers = ['曲线', '对比']
        self.curves_table: ToolkitTable = ToolkitTable(
            self.ui.findChild(QTableWidget, name='curve_analysis_table_3'),
            headers=self._table_headers
        )
        self.curves = {}
        self.visible_curves = []
        charts = {
            'torque': self.ui.findChild(QWebEngineView, name='webContentView_13'),
            'angle': self.ui.findChild(QWebEngineView, name='webContentView_14'),
            'torque_rate': self.ui.findChild(QWebEngineView, name='webContentView_15'),
            'torque_rate_log': self.ui.findChild(QWebEngineView, name='webContentView_16'),
        }
        self.charts = {}
        for key, val in charts.items():
            c = Chart(val, key, cache_path)
            c.show()
            self.charts.update({key: c})

    @property
    def table_content(self):
        content = pd.DataFrame([])
        for name, data in self.curves.items():
            b = QCheckBox()
            f = partial(self._toggle_show_curve, name)
            b.clicked.connect(f)
            b.setStyleSheet("margin: 50% 50% 50% 50%;")
            content = content.append({
                '曲线': name,
                '对比': b,
            }, ignore_index=True)
        return content

    def _toggle_show_curve(self, curve_name):
        if curve_name in self.visible_curves:
            self.visible_curves.remove(curve_name)
            return
        self.visible_curves.append(curve_name)
        self.render_chart()

    def add_curve(self, name, curve_data):
        self.curves[name] = curve_data
        self.render_table()

    def connect_add_curve(self, handler):
        self.add_curve_btn.clicked.connect(handler)

    def connect_remove_curve(self, handler):
        self.remove_curve_btn.clicked.connect(handler)

    def render_table(self):
        self.curves_table.render_content(self.table_content)
        header = self.curves_table.table_instance.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

    def render_chart(self):
        for chart_name, chart in self.charts.items():
            all_series = []
            for curve, series in self.curves.items():
                s = series.get(chart_name, None)
                if not s:
                    continue
                all_series.append(s)
            chart.set_series(all_series)
