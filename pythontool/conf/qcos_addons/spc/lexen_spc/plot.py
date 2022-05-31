# -*- coding: utf-8 -*-
from __future__ import division  # 精确除以
import logging
# from typing import List, Optional, Union, Set
import numpy as np
import math
import sys

major_version = sys.version_info.major

_logger = logging.getLogger(__name__)


def normfun(x, mu, sigma):
    pdf = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
    return pdf


def normal(data, usl, lsl, step=1, density=True):
    # type: (List[float], float, float, int, bool) -> tuple
    if usl < lsl:
        _logger.error("normal usl Must Be Greater Than lsl")
        return [], []
    # if not isinstance(step, int):
    #     _logger.error("histogram Step Must Be Int Type")
    #     return None, None
    if not data:
        _logger.error("normal Data Must Be Int Type")
        return [], []
    sigma = np.std(data)
    mean = np.mean(data)
    d = np.random.normal(mean, sigma, 100)
    dd = d.tolist()
    x_line, y_line, _ = histogram(
        dd, usl=usl, lsl=lsl, step=step, density=density)
    for i, val in enumerate(x_line):
        if i + 1 < len(x_line):
            if density:
                y_line[i] = normfun((x_line[i] + x_line[i + 1]) / 2, mean, sigma) * step
            else:
                y_line[i] = normfun((x_line[i] + x_line[i + 1]) / 2, mean, sigma) * step * 100
    return x_line, y_line


def histogram(data, usl, lsl, step=1, density=True):
    # type: (Union[List[float], object], float, float, int, bool) -> tuple
    if usl < lsl:
        _logger.error("histogram usl Must Be Greater Than lsl")
        return [], [], 0
    # if not isinstance(step, int):
    #     _logger.error("histogram Step Must Be Int Type")
    #     return None, None
    if not data:
        _logger.error("histogram Data Must Be Int Type")
        return [], [], 0
    sigma = np.std(data)
    mean = np.mean(data)
    data_min = mean - 3 * sigma
    data_max = mean + 3 * sigma
    if usl and lsl:
        bins = np.arange(lsl, usl + step, step)
    else:
        bins = np.arange(data_min - step, data_max + step, step)
    y_line, x_line = np.histogram(data, bins, density=False)
    y = []
    # data中有效数据的长度
    eff_length = 0
    for i, val in enumerate(y_line):
        if np.nan in y_line.tolist():
            y_line[i] = 0
        y.append((y_line[i]) / len(data))
        eff_length += y_line[i]
    return x_line, np.array(y), eff_length
