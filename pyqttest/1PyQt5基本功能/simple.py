#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Py40.com PyQt5 tutorial

In this example, we create a simple
window in PyQt5.

author: Jan Bodnar
website: py40.com
last edited: January 2015
"""

import sys
# http://code.py40.com/pyqt5/18.html
# 这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QTabWidget

if __name__ == '__main__':
    # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)
    # QWidget部件是pyqt5所有用户界面对象的基类。他为QWidget提供默认构造函数。默认构造函数没有父类。
    MainWindow = QMainWindow()

    MainWindow.setObjectName("MainWindow")
    MainWindow.resize(1366, 700)

    centralwidget = QWidget(MainWindow)
    centralwidget.setObjectName("centralwidget")

    horizontalLayout = QHBoxLayout(centralwidget)
    horizontalLayout.setObjectName("horizontalLayout")

    tabWidget_2 = QTabWidget(centralwidget)
    tabWidget_2.setTabPosition(QTabWidget.West)
    tabWidget_2.setTabShape(QTabWidget.Rounded)
    tabWidget_2.setUsesScrollButtons(True)
    tabWidget_2.setTabBarAutoHide(False)
    tabWidget_2.setObjectName("tabWidget_2")

    _translate = QtCore.QCoreApplication.translate
    setting_tab = QWidget()
    setting_tab.setObjectName("setting_tab")

    horizontalLayout_3 = QHBoxLayout(setting_tab)

    horizontalLayout.addWidget(tabWidget_2)
    MainWindow.setCentralWidget(centralwidget)

    tabWidget_2.addTab(setting_tab, "")
    tabWidget_2.setTabText(tabWidget_2.indexOf(setting_tab), _translate("MainWindow", "设置"))

    MainWindow.setWindowTitle(_translate("MainWindow", "唐山转向架动检车间标定程序"))

    MainWindow.showMaximized()

    # w = QWidget()

    #
    # # resize()方法调整窗口的大小。这离是250px宽150px高
    # w.resize(2500, 1500)
    # # move()方法移动窗口在屏幕上的位置到x = 300，y = 300坐标。
    # w.move(300, 300)
    # # 设置窗口的标题
    # w.setWindowTitle('Simple')
    # # 显示在屏幕上
    # w.show()
    #

    ret = app.exec()
    # 系统exit()方法确保应用程序干净的退出
    # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    sys.exit(ret)
