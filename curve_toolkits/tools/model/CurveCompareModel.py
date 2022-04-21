from os import path

import pandas as pd

from tools.model.CurveModel import CurveModel


class CurveCompareModel:
    def __init__(self, name, curve1: CurveModel, curve2: CurveModel):
        self.name = name
        self.curve1 = curve1
        self.curve2 = curve2

    def _get_series(self, x_data: str, y_data: str):
        return {
            'name': self.name,
            'type': 'line',
            'yAxisIndex': 0,
            'symbol': 'circle',
            'clip': False,
            'showSymbol': False,
            'itemStyle': {
            },
            'lineStyle': {
                'width': 4
            },
            'label': {'show': False},
            'data': CurveModel.gen_data_points(
                x_data, y_data
            )
        }

    @staticmethod
    def gen_data_points(x, y):
        points = []
        for i in range(min(len(x), len(y))):
            points.append((x[i], y[i]))
        return points

    @property
    def series_torque(self):
        return None

    @property
    def series_angle(self):
        return None

    @property
    def series_torque_rate(self):
        return None

    @property
    def series_torque_rate_log(self):
        return None
