# -*- coding:utf-8 -*-
from PyQt5 import QtWidgets, QtCore  # import PyQt5 widgets
from ui.toolkit import Ui_MainWindow
from tools.view import table, Chart, notify
from .mixin import ToolKitMixin


class ToolKitWindow(ToolKitMixin, QtWidgets.QWidget):
    resized = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        main_window = QtWidgets.QMainWindow(*args, **kwargs)
        ToolKitMixin.__init__(self, main_window)
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self.qt_instance)
        self._compare_bolt_table = table.ToolkitTable(self.ui.tableWidget)
        self._params_table = table.ToolkitTable(self.ui.tableParams)
        self._add_curve_button = self.ui.add_curve_button
        self._notifyBox = notify.ToolkitNotify(self.ui.textLog)
        self.init_template_compare_charts()
        self._compare_file = None

    def init_template_compare_charts(self):
        charts = {
            'angle_torque': self.ui.webContentView,
            'time_torque': self.ui.webContentView_2,
            'time_angle': self.ui.webContentView_3,
        }
        self.template_compare_charts = {}
        for key, val in charts.items():
            ll = Chart.Chart(val, key, cache_dir='./')  # fixme
            ll.show()
            self.template_compare_charts.update({key: ll})

    @property
    def compare_items_table(self):
        return self._compare_bolt_table

    @property
    def gen_tmpl_items_table(self):
        return self._gen_tmpl_items_table

    @property
    def params_table(self):
        return self._params_table

    @property
    def add_curve_button(self):
        return self._add_curve_button

    @property
    def notify_box(self):
        return self._notifyBox

    def resizeEvent(self, event):
        self.resized.emit()
        return super(ToolKitWindow, self).resizeEvent(event)
