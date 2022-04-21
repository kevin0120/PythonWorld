from typing import List
import json
import pandas as pd
from .constants import DEFAULT_TEMPLATE_CURVE_COUNT

def parse_curve_params_from_results(results: pd.DataFrame):
    bolt_numbers = results['bolt_number'].unique()
    bolts_data = {}
    oks = results.loc[results['measure_result'] == 'OK']
    for bolt in bolt_numbers:
        rows = oks.loc[oks['bolt_number'] == bolt]
        if rows.empty:
            continue
        first_row = rows.iloc[0]
        craft_type = int(first_row['craft_type'])
        step_result = json.loads(first_row['step_results'])[-1]
        curve_param = {
            "angle_threshold": 0.075,
            "angle_up_limit_max": float(step_result['angle_max']),
            "angle_up_limit_min": float(step_result['angle_min']),
            "sampling_time": 0.0005,
            "slope_threshold": 15,
            "threshold": 0.3,
            "torque_low_limit": 0,
            "torque_threshold": 2.5,
            "torque_up_limit_max": float(step_result['torque_max']),
            "torque_up_limit_min": float(step_result['torque_min'])
        }
        bolts_data.update({
            bolt: {
                'craft_type': craft_type,
                'curve_param': curve_param
            }
        })
    return bolts_data


def choose_template_curves_from_result_file(
        results: pd.DataFrame, bolt_number: str, curve_count: int = DEFAULT_TEMPLATE_CURVE_COUNT, ok_state='OK', random=True
) -> List[str]:
    """
    返回制定螺栓曲线的entity_id
    @param results: 结果DataFrame
    @param bolt_number: 螺栓编号
    @param curve_count: 返回的曲线数量
    @param ok_state: 筛选结果类型，OK/NOK/ALL
    @param random: 是否从满足条件的曲线中随机筛选
    """
    all = results.loc[results['bolt_number'] == bolt_number]
    filtered = all.loc[results['measure_result'] == ok_state] if ok_state != 'ALL' else all
    if filtered.empty:
        return []
    picked_results = filtered.sample(curve_count, replace=True) if random else filtered.head(curve_count)
    curves = picked_results['entity_id'].unique()

    return curves


if __name__ == '__main__':
    result_df = pd.read_csv('./results.csv')
    bolt_data = parse_curve_params_from_results(result_df)
    entity_ids = choose_template_curves_from_result_file(result_df, list(bolt_data.keys())[0])
    pass
