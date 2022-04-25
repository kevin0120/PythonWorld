# -*- coding: utf-8 -*-

import platform
from loguru import logger
import ctypes
import sys
import os
from .sdk import initCurveLib

logger.add("logs/curve_sdk.log", rotation="1 days", level="INFO", enqueue=True, encoding='utf-8')  # 文件日誌

MSDK = None

try:
    if MSDK is not None:
        pass
    cwd = os.path.abspath(os.path.dirname(__file__))
    if platform.system() == 'Windows':
        ff = os.path.join(cwd, 'lib')
        # 报错提示os没有这个函数
        # os.add_dll_directory(ff)
        os.environ['path'] += ";" + ff
        fl = os.path.join(ff, 'curve_analysis_platform.dll')
        MSDK = ctypes.cdll.LoadLibrary(fl)
    if platform.system() == 'Linux':
        fl = os.path.join(cwd, 'lib', 'libcurve_analysis_platform.so')
        MSDK = ctypes.CDLL(fl)
    initCurveLib(MSDK)
except Exception as e:
    logger.error(e)
    sys.exit(-1)
