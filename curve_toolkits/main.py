# -*- coding:utf-8 -*-
from loguru import logger
from tools.controller.AppController import AppController
import os
import sys, traceback
import platform

logger.add("logs/curve_toolkit.log", rotation="1 days", level="INFO", encoding='utf-8')  # 文件日誌
# logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")

if os.getenv('ENV_RUNTIME') == 'prod' or os.getenv('ENV_RUNTIME') == 'production':
    if platform.system()=='Windows':
        os.environ['QTWEBENGINEPROCESS_PATH'] = os.path.join(os.getcwd(), 'PyQt5', 'Qt', 'bin', 'QtWebEngineProcess.exe')
    else:
        os.environ['QTWEBENGINEPROCESS_PATH'] = os.path.join(os.getcwd(), 'PyQt5', 'Qt', 'bin', 'QtWebEngineProcess')

logger.info('系统启动！！！')

app_controller = AppController()


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logger.error(tb)

sys.excepthook = excepthook

app_controller.run_app()
