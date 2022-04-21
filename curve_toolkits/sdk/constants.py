import ctypes as C
from os import environ

# 版本类型：
# 库版本
CA_VER_PLATFORM = 0
# 算法版本
CA_VER_ALGORITHM = 1

# 加载类型
CA_NORMAL_ATTACH = 0

version_length = 8  # 版本字符串长度

ANALYSIS_WINDOWS_TYPE = C.c_float * 2  # 每个窗口起始和结束，长度为2的array

# 错误代码：
CA_NO_ERROR = 0x00
# 虽然返回值是unsigned 但是 python端拿到的还是signed
CA_NO_ERROR_TORQUE = C.c_int32(0x00000001).value  # 扭矩曲线形态异常
CA_NO_ERROR_ANGLE = C.c_int32(0x00000002).value  # 角度曲线异常
CA_NO_ERROR_SLOPE = C.c_int32(0x00000003).value  # 曲线斜率异常
CA_NO_ERROR_TORQUE_DIFF = C.c_int32(0x00000004).value  # 曲线局部扭矩异常
CA_NO_ERROR_MAX_TORQUE = C.c_int32(0x00000005).value  # 曲线最大扭矩异常
CA_NO_ERROR_MAX_ANGLE_SMALL = C.c_int32(0x00000006).value  # 曲线最终角度过小
CA_NO_ERROR_MAX_ANGLE_LARGE = C.c_int32(0x00000007).value  # 曲线最终角度过大
CA_NO_ERROR_SOFT_STOP = C.c_int32(0x00000008).value  # 曲线软停止异常
CA_NO_SUCH_CURVE_TEMPLATE = C.c_int32(0x00000009).value  # 曲线模板缺失

CA_ERROR_PARAMETER = C.c_int32(0x80010001).value  # 内存中无对应曲线编号，曲线对应参数给出错误
CA_ERROR_LICENSE = C.c_int32(0x80010002).value  #
CA_ERROR_LOW_MEM = C.c_int32(0x80010003).value  #
CA_NO_CURVE_FOUND = C.c_int32(0x80010004).value  # 未正确输入曲线
CA_API_NOT_SUPPORTED = C.c_int32(0x80010005).value  #
CA_ERROR_UNKNOWN = C.c_int32(0x80011FFF).value  #

RET_MAP = {
    CA_NO_ERROR: u'正确返回',
    CA_NO_ERROR_TORQUE: u'扭矩曲线形态异常',
    CA_NO_ERROR_ANGLE: u'角度曲线异常',
    CA_NO_ERROR_SLOPE: u'曲线斜率异常',
    CA_NO_ERROR_TORQUE_DIFF: u'曲线局部扭矩异常',
    CA_NO_ERROR_MAX_TORQUE: u'曲线最大扭矩异常',
    CA_NO_ERROR_MAX_ANGLE_SMALL: u'曲线最终角度过小',
    CA_NO_ERROR_MAX_ANGLE_LARGE: u'曲线最终角度过大',
    CA_NO_ERROR_SOFT_STOP: u'曲线软停止异常',
    CA_NO_SUCH_CURVE_TEMPLATE: u'曲线模板缺失',
    CA_ERROR_PARAMETER: u'内存中无对应曲线编号，曲线对应参数给出错误',
    CA_ERROR_LICENSE: u'授权错误',
    CA_ERROR_LOW_MEM: u'内存不足',
    CA_NO_CURVE_FOUND: u'未正确输入曲线',
    CA_API_NOT_SUPPORTED: u'api未支持',
    CA_ERROR_UNKNOWN: u'未知错误'
}

# CURVE_OK = 0,	//曲线正常
# CURVE_NOK = 1,	//曲线异常（未知原因）
# CURVE_NOK_SLIMSY = 101,   //螺栓粘滑
# CURVE_NOK_DROP = 102,     //扭矩异常下落
# CURVE_NOK_REPEAT = 103,   //重复拧紧
# CURVE_NOK_RELEASE_EARLY = 104,   //提前松手
# CURVE_NOK_ANGLE_TOO_LARGE = 105, //角度过大
CURVE_MODES = {
    'CURVE_OK': 0,
    'CURVE_NOK': 1,
    'CURVE_NOK_SLIMSY': 101,
    'CURVE_NOK_DROP': 102,
    'CURVE_NOK_REPEAT': 103,
    'CURVE_NOK_RELEASE_EARLY': 104,
    'CURVE_NOK_ANGLE_TOO_LARGE': 105,
}

SDK_ATTACH_LEVEL = int(environ.get('SDK_ATTACH_LEVEL', '0'))


def is_valid_curve_mode(mode: int) -> bool:
    return mode in CURVE_MODES.values()


def is_ok_mode(mode) -> bool:
    if CURVE_MODES['CURVE_OK'] == mode:
        return True
    return False


MUTE_UNKNOWN_SLOPE_ERRORS = True if environ.get('MUTE_UNKNOWN_SLOPE_ERRORS', 'False') in ['True', 'true',
                                                                                          True] else False
