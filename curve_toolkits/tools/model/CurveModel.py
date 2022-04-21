from os import path

import pandas as pd

from sdk import sdk
from sdk.structs import interp_curve
from typing import List


class CurveModel:
    def __init__(self, name, cur_t, cur_m, cur_w):
        self.data = pd.DataFrame(interp_curve({
            'cur_t': cur_t,
            'cur_w': sdk.doCAGetCorrectAngle(cur_w),
            'cur_m': cur_m,
        }, 0.0001), columns=['cur_t', 'cur_w', 'cur_m'])
        self.name = name

    @staticmethod
    def from_file(file, name=None):
        data = pd.read_csv(file)
        return CurveModel(
            path.basename(file) if not name else name,
            data.get('Time', data.get('时间', data.get('cur_t', None))).tolist(),
            data.get('Torque', data.get('扭矩', data.get('cur_m', None))).tolist(),
            data.get('Angle', data.get('角度', data.get('cur_w', None))).tolist()
        )

    def _get_series(self, x_data: List[float], y_data: List[float]):
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
    def series_angle_torque(self):
        return self._get_series(
            self.data.get('cur_w').to_list(),
            self.data.get('cur_m').to_list()
        )

    @property
    def series_time_torque(self):
        return self._get_series(
            self.data.get('cur_t').to_list(),
            self.data.get('cur_m').to_list()
        )

    @property
    def series_time_angle(self):
        return self._get_series(
            self.data.get('cur_t').to_list(),
            self.data.get('cur_w').to_list()
        )

    @property
    def series_torque_rate(self):
        torque_rate = sdk.doCAGetTorqueRate(
            self.data.get('cur_m').to_list(),
            self.data.get('cur_w').to_list(),
            20
        )
        return self._get_series(
            self.data.get('cur_t').to_list(),
            torque_rate
        )

    @property
    def series_turning_state(self):
        turning_state = sdk.doCAGetCurveTurningState(
            self.data.get('cur_w').to_list()
        )
        return  self._get_series(
            self.data.get('cur_t').to_list(),
            turning_state
        )
