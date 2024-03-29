import json
import platform

from psycopg2 import errors
from loguru import _logger
from sqlalchemy.exc import IntegrityError

ss = '''[{"M+": 2, 'M-': 1.600000023841858, 'MS': 0, 'MA': 1.7999999523162842, 'W+': 3700, 'W-': 0, 'WA': 0,
       'tool_sn': '21M05649', 'tightening_unit': 'OPde53c8a8775c300', 'measure_result': 'OK',
       'measure_torque': 1.8072596788406372, 'measure_angle': 2963.800048828125, 'measure_time': 0, 'batch': '1/1',
       'seq': 0, 'group_seq': 0, 'count': 0, 'scanner_code': '', 'job': 0, 'remote_addr': '',
       'controller_sn': 'OPde53c8a8775c300', 'controller_name': 'OP300', 'batch_count': 1, 'error_code': '',
       'channel_id': 1, 'update_time': '2022-06-29T10:59:02+08:00', 'pset': 1, 'tightening_id': '0000000198',
       'strategy': 'AD', 'torque_max': 2, 'torque_min': 1.600000023841858, 'torque_threshold': 0,
       'torque_target': 1.7999999523162842, 'angle_max': 3700, 'angle_min': 0, 'angle_target': 0, 'workorder_id': 0,
       'user_id': 0, 'nut_no': '', 'vin': '', 'last_calibration_date': '', 'total_tool_counter': 198, 'id': 0,
       'point_id': '', 'mode': '', 'station_name': '', 'step_results': None}]'''

if __name__ == "__main__":
    s = ss

    b = json.loads(json.dumps(eval(s)))
    print(b)

    try:
        a = 1 / 0
    except ZeroDivisionError as e:
        # 已经存在的结果不再执行后续流程，避免异常处理陷入循环
        print(f'结果已存在')
    except Exception as e:
        raise Exception("保存结果异常: {}".format(repr(e)))
        # print("aaaaa")

    q = platform.system()
    print("hhhh")
