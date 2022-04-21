from sdk.structs import meta_data_2_CURVE_PARAM, CURVE_PARAM_2_meta_data


def is_curve_param_valid(curve_param=None):
    # TODO: 实现曲线检验逻辑
    return True


def is_bolt_data_valid(bolt_data=None):
    # TODO: 实现螺栓数据
    return True


def param_to_float(curve_param: dict):
    return CURVE_PARAM_2_meta_data(meta_data_2_CURVE_PARAM(curve_param))
