# -*- coding:utf-8 -*-

import ctypes as C
from loguru import logger as _logger

import numpy as np
from typing import Dict, Optional, List
from .constants import CA_NORMAL_ATTACH, CA_VER_PLATFORM, CA_VER_ALGORITHM, RET_MAP, CA_NO_ERROR, version_length, \
    CA_ERROR_PARAMETER, \
    SDK_ATTACH_LEVEL, CURVE_MODES
from .structs import CURVE_PARAM, CURVE_DATA, curveData2CStructure, CURVE_TEMPLATE_CLUSTER, clusterCStructure2Dict, \
    c_float_p, CURVE_MODE, CRAFT_TYPE, CURVE_PARAM_2_meta_data, templateData2CStructure, \
    meta_data_2_CURVE_PARAM, P_ARRAY
from .globals import global_var

CurveLib = None

LOADED_TEMPLATES = []
MAX_CURVE_MODES = len(CURVE_MODES.keys())


def gen_cluster_key(bolt_number, craft_type, mode):
    return '{}/{}/{}'.format(bolt_number, craft_type, mode)


def parse_cluster_key(cluster_key):
    bolt_number, craft_type, curve_mode = cluster_key.split('/')
    return {
        'bolt_number': bolt_number,
        'craft_type': craft_type,
        'curve_mode': curve_mode,
    }


def is_cluster_loaded(bolt_number, craft_type, curve_mode):
    cluster_key = gen_cluster_key(bolt_number, craft_type, curve_mode)
    _logger.info(LOADED_TEMPLATES)
    _logger.info('checking template {}'.format(cluster_key))
    return cluster_key in LOADED_TEMPLATES


def loaded_clusters(bolt_number=None, craft_type=None, curve_mode=None):
    filtered_templates = map(parse_cluster_key, LOADED_TEMPLATES)
    if bolt_number is not None:
        filtered_templates = filter(lambda t: t['bolt_number'] == str(bolt_number), filtered_templates)
    if craft_type is not None:
        filtered_templates = filter(lambda t: t['craft_type'] == str(craft_type), filtered_templates)
    if curve_mode is not None:
        filtered_templates = filter(lambda t: t['curve_mode'] == str(curve_mode), filtered_templates)
    return list(filtered_templates)


def createCtypeCharPoint(s: str):
    return C.create_string_buffer(s.encode('utf-8'))


def guardRet(ret):
    if ret not in RET_MAP.keys():
        raise Exception("{0} Is Not Defined".format(ret))
    if ret != CA_NO_ERROR:
        raise Exception(RET_MAP[ret])


def doCAFunction(fn, *args):
    if not CurveLib:
        raise Exception("Library Is Not Loaded")
    ff = getattr(CurveLib, fn, None)
    if not ff:
        raise Exception("{0} Is Not Found".format(fn))
    try:
        _logger.debug('calling {}, {}'.format(fn, args))
        ret = ff(*args)
        _logger.info("do Function {0}, ret: {1}".format(fn, ret))
        return ret
    except Exception as e:
        _logger.error("do Function {0} Error: {1}".format(fn, repr(e)))
        raise Exception("do Function {0} Error: {1}".format(fn, repr(e)))


def ca_attach() -> int:
    ret = doCAFunction('ca_attach', CA_NORMAL_ATTACH)
    return ret


def ca_detach() -> int:
    ret = doCAFunction('ca_detach')
    return ret


def initCurveLib(MSDK):
    try:
        global CurveLib
        CurveLib = MSDK
        ca_attach()
    except Exception as e:
        _logger.error('initCurveLib error: {}'.format(repr(e)))
        raise e


def get_platform_version() -> str:
    p = C.create_string_buffer(version_length)
    # 获取库版本
    doCAFunction('ca_get_version', CA_VER_PLATFORM, p, version_length)
    ss = p.value
    if isinstance(p.value, bytes):
        ss = p.value.decode('utf-8')
    global_var['VER_PLATFORM'] = ss
    _logger.info(global_var['VER_PLATFORM'])
    return global_var['VER_PLATFORM']


def get_algorithm_version() -> str:
    p = C.create_string_buffer(version_length)

    # 获取算法版本
    doCAFunction('ca_get_version', CA_VER_ALGORITHM, p, version_length)
    global_var['VER_ALGORITHM'] = p.value
    _logger.info(repr(global_var['VER_ALGORITHM']))
    return global_var['VER_ALGORITHM']


# 分析曲线
def doCACurveVerify(bolt_number: str, curve_data: CURVE_DATA, windows: np.ndarray, measure_result,
                    max_result_count: int = MAX_CURVE_MODES) -> List[int]:
    try:
        _logger.debug("verifying {}...".format(bolt_number))
        result = P_ARRAY(CURVE_MODE, [], max_result_count)
        result_count = C.c_int(max_result_count)
        _logger.debug("windows.ctypes.shape {0}".format(len(windows)))
        len_windows = len(windows)
        windows = windows.astype(np.float32)
        bolt_no = createCtypeCharPoint(bolt_number)
        c_window = windows.ctypes.data_as(C.POINTER(c_float_p))
        ret = doCAFunction('ca_curve_verify', bolt_no, C.byref(curve_data),
                           c_window, len_windows, result, C.byref(result_count))
        _logger.info('ca_curve_verify returning {}'.format(RET_MAP[ret]))
        if ret == CA_ERROR_PARAMETER:
            return ret, [measure_result]
        verify_result_arr = result[:result_count.value]
        return ret, verify_result_arr
    except Exception as e:
        _logger.error("doCACurveVerify failed: ".format(repr(e)))
        raise e


# 分析曲线match
def doCACurveMatch(bolt_number: str, craft_type, curve_params, curve_data: CURVE_DATA, windows: np.ndarray,
                   template_cluster, measure_result, max_result_count: int = MAX_CURVE_MODES) -> List[int]:
    try:
        _logger.debug("matching {}...".format(bolt_number))
        result = P_ARRAY(CURVE_MODE, [], max_result_count)
        result_count = C.c_int(max_result_count)
        _logger.debug("windows.ctypes.shape {0}".format(len(windows)))
        len_windows = len(windows)
        windows = windows.astype(np.float32)
        bolt_no = createCtypeCharPoint(bolt_number)
        c_window = windows.ctypes.data_as(C.POINTER(c_float_p))
        c_template_cluster = templateData2CStructure(template_cluster)
        c_curve_params = meta_data_2_CURVE_PARAM(curve_params)
        ret = doCAFunction('ca_curve_match', bolt_no, CRAFT_TYPE(craft_type), c_curve_params, C.byref(curve_data),
                           c_window, len_windows, C.byref(c_template_cluster), result, C.byref(result_count))
        _logger.info('ca_curve_verify returning {}'.format(RET_MAP[ret]))
        if ret == CA_ERROR_PARAMETER:
            return ret, [measure_result]
        verify_result_arr = result[:result_count.value]
        return ret, verify_result_arr
    except Exception as e:
        _logger.error("doCACurveMatch failed: ".format(repr(e)))
        raise e


# 创建新模板
def doCANewTemplate(curve_meta_data, curve_param, bolt_number, craft_type: int, mode: int, final_angle: float,
                    final_torque: float):
    _logger.info("encoding template cluster...")
    template_cluster, curve_param = doCACurveEncode(bolt_number, craft_type, mode, curve_param, curve_meta_data,
                                                    final_angle, final_torque)
    _logger.info("loading template to sdk...")
    cluster_data = clusterCStructure2Dict(template_cluster)
    doCALoadCurveTemplate(bolt_number, craft_type, mode, curve_param, template_cluster)
    _logger.info("releasing template cluster...")
    doCAReleaseCurveTemplate(C.byref(template_cluster))
    _logger.info("new template cluster created")
    return cluster_data


# 根据曲线生成模板
def doCACurveEncode(bolt_number: str, craft_type: int, mode: int, curve_param: Dict,
                    curve_meta_data: Dict, final_angle: float, final_torque: float):
    # 异常曲线不encode，只encode正常曲线
    if mode != 0:
        return None
    curve_data = curveData2CStructure(curve_meta_data, final_angle, final_torque,
                                      curve_param.get('sampling_time', None))
    c_params = meta_data_2_CURVE_PARAM(curve_param)
    ret_template_cluster = CURVE_TEMPLATE_CLUSTER()
    ret = doCAFunction('ca_curve_encode',
                       createCtypeCharPoint(bolt_number),
                       CRAFT_TYPE(craft_type),
                       CURVE_MODE(mode),
                       C.byref(c_params),
                       C.c_uint(1),
                       C.byref(curve_data),
                       C.byref(ret_template_cluster)
                       )
    guardRet(ret)
    return ret_template_cluster, CURVE_PARAM_2_meta_data(c_params)


# 根据多条曲线生成模板
def doCACurveEncodeMultiple(bolt_number: str, craft_type: int, mode: int, curve_param: Dict,
                            curve_meta_data: List[Dict], final_angles: List[float], final_torques: List[float]):
    # 异常曲线不encode，只encode正常曲线
    if mode != 0:
        return None
    curves_data = []
    for index, curve in enumerate(curve_meta_data):
        curves_data.append(curveData2CStructure(curve, final_angles[index], final_torques[index],
                                                curve_param.get('sampling_time', None)))
    curves_count = len(curves_data)
    curves_arr = P_ARRAY(CURVE_DATA, curves_data, curves_count)

    c_params = meta_data_2_CURVE_PARAM(curve_param)
    ret_template_cluster = CURVE_TEMPLATE_CLUSTER()
    ret = doCAFunction('ca_curve_encode',
                       createCtypeCharPoint(bolt_number),
                       CRAFT_TYPE(craft_type),
                       CURVE_MODE(mode),
                       C.byref(c_params),
                       C.c_uint(curves_count),
                       C.byref(curves_arr),
                       C.byref(ret_template_cluster)
                       )
    guardRet(ret)
    return ret_template_cluster, CURVE_PARAM_2_meta_data(c_params)


# 加载曲线模板
def doCALoadCurveTemplate(bolt_number: str, craft_type: int, mode: int, params: Dict,
                          c_template_cluster: CURVE_TEMPLATE_CLUSTER):
    cluster_key = gen_cluster_key(bolt_number, craft_type, mode)
    curve_params = meta_data_2_CURVE_PARAM(params)
    ret = doCAFunction('ca_load_curve_template', createCtypeCharPoint(bolt_number), CRAFT_TYPE(craft_type),
                       CURVE_MODE(mode),
                       curve_params, C.byref(c_template_cluster))
    guardRet(ret)
    if cluster_key not in LOADED_TEMPLATES:
        LOADED_TEMPLATES.append(cluster_key)


# 更新曲线参数与模板
def doCAUpdateCurveParamAndTemplate(bolt_number: str, craft_type: int, mode: int, param_data,
                                    curve_data: CURVE_DATA, verify_error: int) -> Optional[Dict]:
    p_template_cluster = C.pointer(CURVE_TEMPLATE_CLUSTER())
    params: CURVE_PARAM = meta_data_2_CURVE_PARAM(param_data)
    ret = doCAFunction('ca_update_curve_params_and_template',
                       createCtypeCharPoint(bolt_number),
                       CRAFT_TYPE(craft_type),
                       CURVE_MODE(mode),
                       C.pointer(params),
                       C.byref(curve_data),
                       C.c_int(verify_error),
                       p_template_cluster)
    guardRet(ret)
    cluster = clusterCStructure2Dict(p_template_cluster.contents)
    # 此处不需要release
    if cluster.get('curve_template_groups_k', 0) == 0:
        return None
    return cluster


# 取得曲线模板，曲线模板可视化
def doCAGetCurveTemplate(bolt_number: str, mode: int) -> Dict:
    p_template_cluster = C.pointer(CURVE_TEMPLATE_CLUSTER())
    ret = doCAFunction('ca_get_curve_template', createCtypeCharPoint(bolt_number), CURVE_MODE(mode),
                       p_template_cluster)
    guardRet(ret)
    cluster = clusterCStructure2Dict(p_template_cluster.contents)
    doCAReleaseCurveTemplate(p_template_cluster)
    return cluster


# 删除曲线模板
def doCADeleteCurveTemplate(bolt_number: str, craft_type: int, mode: int):
    cluster_key = gen_cluster_key(bolt_number, craft_type, mode)
    ret = doCAFunction('ca_delete_curve_template', createCtypeCharPoint(bolt_number), CURVE_MODE(mode))
    if cluster_key in LOADED_TEMPLATES:
        LOADED_TEMPLATES.remove(cluster_key)
    guardRet(ret)


# 取得曲线参数
def doGetCurveParams(bolt_number) -> Dict:
    p_curve_param = C.pointer(CURVE_PARAM())
    ret = doCAFunction('ca_get_curve_params', createCtypeCharPoint(bolt_number), p_curve_param)
    guardRet(ret)
    return CURVE_PARAM_2_meta_data(p_curve_param.contents)


# 释放模板内存
def doCAReleaseCurveTemplate(p_template_cluster):
    doCAFunction('ca_release_curve_template', p_template_cluster)


# 计算曲线扭矩率
def doCAGetTorqueRate(torque: List[float], angle: List[float], window_size=1):
    torque_arr = P_ARRAY(C.c_float, torque)
    angle_arr = P_ARRAY(C.c_float, angle)
    length = min(len(torque), len(angle))
    torque_rate = P_ARRAY(C.c_float, [], length)
    actural_length = C.c_int(length)
    ret = doCAFunction(
        'ca_get_curve_torque_rate',
        torque_arr,
        angle_arr,
        length,
        C.c_int(window_size),
        torque_rate,
        C.byref(actural_length)
    )
    guardRet(ret)
    return torque_rate[:actural_length.value]


# 矫正角度曲线
def doCAGetCorrectAngle(angle: List[float]):
    angle_arr = P_ARRAY(C.c_float, angle)
    length = C.c_int(len(angle))
    correct_angle = P_ARRAY(C.c_float, [], len(angle))
    ret = doCAFunction(
        'ca_get_curve_correct_angle',
        angle_arr,
        length,
        correct_angle,
    )
    guardRet(ret)
    return correct_angle[:length.value]


def doCAGetCurveTurningState(angle: List[float]):
    angle_arr = P_ARRAY(C.c_float, angle)
    length = C.c_int(len(angle))
    turning_state = P_ARRAY(C.c_float, [], len(angle))
    ret = doCAFunction(
        'ca_get_curve_turning_state',
        angle_arr,
        length,
        turning_state,
    )
    guardRet(ret)
    return turning_state[:length.value]