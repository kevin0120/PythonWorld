import pandas as pd
from tools.view.FileLoader import FileLoader


def is_curve_valid(curve_data=None, curve_path=None):
    # TODO: 实现曲线检验逻辑
    if curve_path is None and curve_data is None:
        return False
    if curve_path:
        try:
            curve = read_file(curve_path)
            assert curve.get('时间', curve.get('Time', curve.get('cur_t', None))) is not None
            assert curve.get('扭矩', curve.get('Torque', curve.get('cur_m', None))) is not None
            assert curve.get('角度', curve.get('Angle', curve.get('cur_w', None))) is not None
        except Exception:
            return False
        try:
            assert curve.get('时间', curve.get('Time', curve.get('cur_t', None))).iloc[-1] != \
                   curve.get('时间', curve.get('Time', curve.get('cur_t', None))).iloc[0]
        except Exception:
            return False
    return True


def read_file(file):
    data = pd.read_csv(file)
    return data


def curve_df_to_dict(df: pd.DataFrame):
    template_time = df.get('Time', df.get('时间', df.get('cur_t', None))).tolist()
    template_torque = df.get('Torque', df.get('扭矩', df.get('cur_m', None))).tolist()
    template_angle = df.get('Angle', df.get('角度', df.get('cur_w', None))).tolist()
    return {
        'template_time': template_time,
        'template_angle': template_angle,
        'template_torque': template_torque
    }


def template_dict_to_sdk_dict(data):
    return {
        'cur_t': data['template_time'],
        'cur_m': data['template_torque'],
        'cur_w': data['template_angle']
    }


def select_curve_from_filesystem(title="选择曲线"):
    return FileLoader().open_file(title, "CSV Files (*.csv);;Excel Files (*.xlst);;All Files (*)")

def select_curves_from_filesystem(title="选择曲线"):
    return FileLoader().open_files(title, "CSV Files (*.csv);;Excel Files (*.xlst);;All Files (*)")
