import ctypes as C
from loguru import logger as _logger
from typing import Dict
from .globals import global_var
import numpy as np

c_float_p = C.POINTER(C.c_float)

CRAFT_TYPE = C.c_int  # 重新定义
CURVE_MODE = C.c_int


def interp_curve(curve, target_time_step):
    if target_time_step is None:
        raise Exception('目标采样时间为空')
    time_arr = curve['cur_t']
    angle_arr = curve['cur_w']
    torque_arr = curve['cur_m']
    errMsg = ''
    if torque_arr is None:
        errMsg += '曲线扭矩缺失。'
    if angle_arr is None:
        errMsg += '曲线角度缺失。'
    if errMsg != '':
        raise Exception(errMsg)
    if len(time_arr) != len(angle_arr) or len(time_arr) != len(torque_arr):
        raise Exception('曲线数据长度不匹配，时间：{}，角度：{}，扭矩：{}'.format(len(time_arr), len(angle_arr), len(torque_arr)))
    target_time = [t for t in np.arange(0, time_arr[-1], target_time_step)]
    target_angle = np.interp(target_time, time_arr, angle_arr)
    target_torque = np.interp(target_time, time_arr, torque_arr)
    return {
        'cur_m': target_torque,
        'cur_w': target_angle,
        'cur_t': target_time
    }


class CURVE_DATA(C.Structure):
    _fields_ = [
        ("curve_len", C.c_uint),
        ("curve_angle", c_float_p),
        ("curve_torque", c_float_p),
        ("curve_final_angle", C.c_float),
        ("curve_final_torque", C.c_float),
    ]


class CURVE_TEMPLATE(C.Structure):
    _fields_ = [
        # 曲线模板长度
        ("template_single_len", C.c_uint),

        # 角度模板数据
        ("template_angle", c_float_p),

        # 扭矩模板数据
        ("template_torque", c_float_p),

        # 启动点
        ("start_point", C.c_uint),
    ]


class CURVE_TEMPLATE_GROUP(C.Structure):
    _fields_ = [
        # 曲线模板个数
        ("template_size", C.c_uint),

        # 模板组中心索引，该索引为template_data_array中曲线模板序号，从0开始
        ("template_centroid_index", C.c_int),

        # 曲线模板序列
        ("template_data_array", C.POINTER(CURVE_TEMPLATE)),
    ]


class CURVE_TEMPLATE_CLUSTER(C.Structure):
    _fields_ = [
        # 算法版本
        ("algorithm_version", C.c_int),

        # 曲线组个数
        ("curve_template_groups_k", C.c_uint),

        # 曲线模板组序列
        ("curve_template_group_array", C.POINTER(CURVE_TEMPLATE_GROUP)),
    ]


class CURVE_PARAM(C.Structure):
    _fields_ = [
        ("torque_low_limit", C.c_float),  # 扭矩下限值，即起始扭矩，此扭矩值开始的数据记为有效值
        ("torque_up_limit_min", C.c_float),  # 扭矩上限区间最小值
        ("torque_up_limit_max", C.c_float),  # 扭矩上限区间最大值
        ("threshold", C.c_float),  # 曲线比对阈值
        ("slope_threshold", C.c_float),  # 曲线斜率比对阈值
        ("torque_threshold", C.c_float),  # 扭矩差值阈值
        ("angle_threshold", C.c_float),  # 角度对比阈值
        ("angle_up_limit_min", C.c_float),  # 角度上限区间最小值
        ("angle_up_limit_max", C.c_float),  # 角度上限区间最大值
        ("sampling_time", C.c_float),  # 采样时间间隔
    ]


def P_ARRAY(C_TYPE, data, length=None):
    if length is None:
        length = len(data)
    _ARR = C_TYPE * length
    return _ARR(*data)


def meta_data_2_CURVE_PARAM(
        meta_data: Dict) -> CURVE_PARAM:
    return CURVE_PARAM(meta_data['torque_low_limit'],
                       meta_data['torque_up_limit_min'],
                       meta_data['torque_up_limit_max'],
                       meta_data['threshold'],
                       meta_data['slope_threshold'],
                       meta_data['torque_threshold'],
                       meta_data['angle_threshold'],
                       meta_data['angle_up_limit_min'],
                       meta_data['angle_up_limit_max'],
                       meta_data['sampling_time'])


def CURVE_PARAM_2_meta_data(curve_param: CURVE_PARAM) -> Dict:
    return {
        'torque_low_limit': curve_param.torque_low_limit,
        'torque_up_limit_min': curve_param.torque_up_limit_min,
        'torque_up_limit_max': curve_param.torque_up_limit_max,
        'threshold': curve_param.threshold,
        'slope_threshold': curve_param.slope_threshold,
        'torque_threshold': curve_param.torque_threshold,
        'angle_threshold': curve_param.angle_threshold,
        'angle_up_limit_min': curve_param.angle_up_limit_min,
        'angle_up_limit_max': curve_param.angle_up_limit_max,
        'sampling_time': curve_param.sampling_time
    }


def curveData2CStructure(curve_data: Dict, final_angle: float, final_torque: float,
                         target_time_step: float) -> CURVE_DATA:
    new_curve_data = interp_curve(curve_data, target_time_step)
    cur_m = new_curve_data['cur_m']
    cur_w = new_curve_data['cur_w']
    len_curve = len(cur_m)
    return CURVE_DATA(len_curve, P_ARRAY(C.c_float, cur_w, len_curve), P_ARRAY(C.c_float, cur_m, len_curve),
                      final_angle, final_torque)


def clusterCStructure2Dict(c_template_cluster: CURVE_TEMPLATE_CLUSTER) -> Dict:
    try:
        template_group_num = c_template_cluster.curve_template_groups_k
        curve_template_group_array = []
        raw_template_array = c_template_cluster.curve_template_group_array[:template_group_num]
        for raw_template in raw_template_array:
            template_data_num = raw_template.template_size
            raw_template_data_array = raw_template.template_data_array[:template_data_num]
            template_data_array = []
            for raw_template_data in raw_template_data_array:
                template_data_len = raw_template_data.template_single_len
                template_angle = raw_template_data.template_angle[:template_data_len]
                template_torque = raw_template_data.template_torque[:template_data_len]
                template_data_array.append({
                    'template_angle': template_angle,
                    'template_torque': template_torque,
                    'start_point': raw_template_data.start_point
                })
            curve_template_group_array.append({
                'template_centroid_index': raw_template.template_centroid_index,
                'template_data_array': template_data_array
            })

        cluster_data = {
            'algorithm_version': c_template_cluster.algorithm_version,
            'curve_template_groups_k': c_template_cluster.curve_template_groups_k,
            'curve_template_group_array': curve_template_group_array
        }

        return cluster_data
    except Exception as e:
        _logger.error("clusterCStructure2Dict failed: {}".format(repr(e)))
        raise e


def templateData2CStructure(template_cluster: Dict) -> CURVE_TEMPLATE_CLUSTER:
    c_template_groups = []
    if template_cluster is None:
        raise Exception('template has no cluster')
    data_groups = template_cluster.get('curve_template_group_array', [])
    len_group = len(data_groups)
    for group in data_groups:
        c_templates = []
        data_templates = group['template_data_array']
        for template in data_templates:
            torque_template = template.get('template_torque', [0.0])
            angle_template = template.get('template_angle', [0.0])
            start_point = template.get('start_point', 0)
            len_template_data = len(torque_template)
            c_template = CURVE_TEMPLATE(len_template_data,
                                        P_ARRAY(C.c_float, angle_template, len_template_data),
                                        P_ARRAY(C.c_float, torque_template, len_template_data),
                                        start_point)
            c_templates.append(c_template)

        len_templates = len(data_templates)
        center_index = group.get('template_centroid_index', 0)
        c_group_templates = P_ARRAY(CURVE_TEMPLATE, c_templates, len_templates)
        c_group = CURVE_TEMPLATE_GROUP(len_templates, center_index, c_group_templates)
        c_template_groups.append(c_group)

    c_groups = P_ARRAY(CURVE_TEMPLATE_GROUP, c_template_groups, len_group)
    c_cluster = CURVE_TEMPLATE_CLUSTER(0, len_group, c_groups)
    return c_cluster


# 指针类型定义
PTR_CURVE_TEMPLATE_CLUSTER = C.POINTER(CURVE_TEMPLATE_CLUSTER)
