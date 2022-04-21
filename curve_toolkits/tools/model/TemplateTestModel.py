from typing import Union
from typing import Dict
from sdk import sdk
import pandas as pd
import numpy as np
import json
from tools.utils.curve import read_file, curve_df_to_dict, template_dict_to_sdk_dict
from tools.utils.template import read_curve_templates_from_file
from scipy.optimize import basinhopping
import os.path as path
import os


class TemplateTestModel:
    def __init__(self):
        pass

    @staticmethod
    def diff_of_template(
            curve_template: dict,
            tags: pd.DataFrame,
    ) -> (float, pd.DataFrame):
        """
        输入结果、曲线和模板，返回使用该模板分析的结果与标记结果的差异和差异详情
        :param curve_template: 需要测试的曲线模板json
        :param curve_files: 用于验证的曲线文件列表
        :param tags: 曲线结果标签
        :return: 差异率, 差异详情
        """

        bolt_number = curve_template.get('nut_no', None)
        craft_type = curve_template.get('craft_type', None)
        curve_param = curve_template.get('curve_param', None)
        template_cluster = curve_template.get('template_cluster', None)

        assert bolt_number is not None, '曲线模板解析失败，nut_no缺失'
        assert craft_type is not None, '曲线模板解析失败，craft_type缺失'
        assert craft_type is not None, '曲线模板解析失败，curve_param缺失'
        assert template_cluster is not None, '曲线模板解析失败，template_cluster缺失'

        diff_detail = pd.DataFrame(tags).join(
            pd.DataFrame(columns=['analysis_result', 'is_diff']))
        if tags.empty:
            return 0, 0, diff_detail

        for index, row in diff_detail.iterrows():
            try:
                file_path = row['curve_path']
                curve_data = TemplateTestModel.read_curve_file(file_path)
                verify_error, curve_mode = TemplateTestModel.match_curve(
                    bolt_number,
                    craft_type,
                    curve_param,
                    curve_data,
                    template_cluster.get('0'),
                    row['tag'],
                    curve_param.get("sampling_time")
                )

                diff_detail.loc[index, 'analysis_result'] = 'OK' if curve_mode[0] == 0 else 'NOK'
                diff_detail.loc[index, 'is_diff'] = False if diff_detail.loc[index, 'analysis_result'] == row[
                    'tag'] else True
                diff_detail.loc[index, 'verify_error'] = verify_error
                diff_detail.loc[index, 'curve_mode'] = json.dumps(curve_mode)
            except Exception as e:
                print(e)
                continue

        oks = diff_detail.loc[diff_detail['tag'] == 'OK']
        noks = diff_detail.loc[diff_detail['tag'] == 'NOK']
        diff_rate_ok = oks.loc[oks['is_diff'] == True].shape[0] / oks.shape[0] if oks.shape[0] > 0 else 0
        diff_rate_nok = noks.loc[noks['is_diff'] == True].shape[0] / noks.shape[0] if noks.shape[0] > 0 else 0
        return diff_rate_ok, diff_rate_nok, diff_detail

    @staticmethod
    def read_curve_file(file_path: str) -> str:
        """
        读取曲线文件为算法可以识别的json结构
        :param file_path:
        :return:
        """
        return template_dict_to_sdk_dict(curve_df_to_dict(read_file(file_path)))

    @staticmethod
    def match_curve(bolt_number, craft_type, curve_params, curve_data, template_cluster, measure_result, sampling_time):
        """
        调用算法的match函数，返回verify_error和curve_mode
        :param bolt_number:
        :param craft_type:
        :param curve_params:
        :param curve_data:
        :param template_cluster:
        :param measure_result:
        :param sampling_time:
        :return:
        """
        windows = []
        c_curve_data = sdk.curveData2CStructure(curve_data, 0, 0, sampling_time)
        return sdk.doCACurveMatch(
            bolt_number,
            craft_type,
            curve_params,
            c_curve_data,
            np.array(windows),
            template_cluster,
            measure_result
        )

    @staticmethod
    def optimize(
            templates: Dict,
            results: pd.DataFrame,
            curves_base_path: str,
            optimize_args=None,
            optimize_range=0.5,
            optimize_count=2
    ):
        """
        最优化算法参数
        :return:
        """
        full_args = ['angle_threshold', 'slope_threshold', 'threshold', 'torque_threshold']
        if optimize_args is None:
            optimize_args = ['slope_threshold', 'threshold']
        for arg in optimize_args:
            if arg not in full_args:
                optimize_args.remove(arg)

        bolt_numbers = templates.keys()
        result = pd.DataFrame(columns=['bolt_number', *optimize_args, 'diff_rate'])
        for bn in bolt_numbers:
            template = Dict.copy(TemplateTestModel.get_template_by_bolt_number(templates, bn))

            tags = TemplateTestModel.get_bolt_results(results, bn)
            tags['tag'] = tags['measure_result']
            tags = TemplateTestModel.set_curve_path(curves_base_path, tags)
            curve_param = template.get('curve_param')
            # ranges = list(map(lambda x: (
            #     float(curve_param.get(x)) * (1 - optimize_range), float(curve_param.get(x)) * (1 + optimize_range)),
            #                   optimize_args))
            x0 = list(map(lambda x: float(curve_param.get(x)), optimize_args))

            def minimize_func(x):
                curve_param_copy = Dict.copy(curve_param)

                template_copy = Dict.copy(template)
                curve_param.update({optimize_args[n]: v for n, v in enumerate(x)})
                template_copy.update({
                    'curve_param': curve_param_copy
                })
                diff_rate_ok, diff_rate_nok, diff_detail = TemplateTestModel.diff_of_template(template_copy, tags)
                diff_rate = diff_detail.loc[diff_detail['is_diff'] == True].shape[0] / diff_detail.shape[0] \
                    if diff_detail.shape[0] > 0 else 0
                return diff_rate

            res = basinhopping(minimize_func, x0, niter=5, T=0.01, stepsize=0.5, disp=True, interval=2)
            ret = pd.DataFrame([{
                'bolt_number': bn,
                **{arg: res['x'][n] for n, arg in enumerate(optimize_args)},
                'diff_rate': res['fun']
            }])
            result = result.append(ret)

            # for i, vs in enumerate(variants):
            #     curve_param.update({keys[n]: v for n, v in enumerate(vs)})
            #
            #     template.update({'curve_param': curve_param})
            #     diff_rate_ok, diff_rate_nok, diff_detail = TemplateTestModel.diff_of_template(template, tags)
            #     ret = pd.DataFrame([{
            #         **{keys[n]: v for n, v in enumerate(vs)},
            #         'diff_rate': diff_rate_ok + diff_rate_nok
            #     }])
            #     result = result.append(ret)
            #     # arg_name = ', '.join([f"{'%.4f' % vs[n]}" for n in range(0, len(list(vs)))])
        result.to_csv(f"./optimize.csv")

    @staticmethod
    def get_template_by_bolt_number(templates_dict: Dict, bolt_number: str):
        template_keys = list(templates_dict.keys())
        key = list(filter(lambda k: bolt_number in k, template_keys))[0]

        return templates_dict[key]

    @staticmethod
    def get_bolt_results(results: Union[str, pd.DataFrame], bolt_number):
        if '/' in bolt_number:
            bolt_number = bolt_number.split('/')[0]
        if type(results) == str:
            results = pd.read_csv(results)
        return results.loc[results['bolt_number'] == bolt_number]

    @staticmethod
    def set_curve_path(base_path, results):
        ret = pd.DataFrame(results)
        ret['curve_path'] = ret['entity_id'].map(
            lambda e: f'{base_path}/{e}.csv'
        )
        return ret


def test_templates(template_file, result_file, curve_path, sample=None, report_path='./report'):
    templates = read_curve_templates_from_file(template_file)
    full_bolt_number = templates.keys()
    # full_bolt_number = ['OP110L_0_0_12/1']
    if not path.exists(report_path):
        os.makedirs(report_path)
    result = pd.DataFrame(columns=['bolt_number', 'diff_ok', 'diff_nok', 'diff_full'])
    for test_bolt_number in full_bolt_number:
        template = TemplateTestModel.get_template_by_bolt_number(templates, test_bolt_number)

        test_tags: pd.DataFrame = TemplateTestModel.get_bolt_results(result_file, test_bolt_number)
        if sample and (sample < len(test_tags)):
            test_tags = test_tags.sample(sample)
        test_tags['tag'] = test_tags['measure_result']
        test_tags = TemplateTestModel.set_curve_path(curve_path, test_tags)

        diff_rate_ok, diff_rate_nok, diff_detail = TemplateTestModel.diff_of_template(template, test_tags)
        diff_rate = diff_detail.loc[diff_detail['is_diff'] == True].shape[0] / diff_detail.shape[0] \
            if diff_detail.shape[0] > 0 else 0
        ret = pd.DataFrame([{
            'bolt_number': test_bolt_number,
            'diff_ok': diff_rate_ok,
            'diff_nok': diff_rate_nok,
            'diff_full': diff_rate
        }])
        result = result.append(ret)
        diff_detail.to_csv(
            f"{report_path}/{test_template_file.split('/')[-1].split('.')[0]}({test_bolt_number.split('/')[0]}).csv")
    report_path = f"{report_path}/test_report_{test_template_file.split('/')[-1].split('.')[0]}.csv"
    result.to_csv(report_path)


def test_optimize(template_file, result_file, curve_path):
    TemplateTestModel.optimize(
        templates=read_curve_templates_from_file(template_file),
        results=pd.read_csv(result_file),
        curves_base_path=curve_path
    )


if __name__ == '__main__':
    test_template_file = os.environ.get('TEST_TEMPLATE_FILE')
    test_result_file = os.environ.get('TEST_RESULT_FILE')
    test_curve_path = os.environ.get('TEST_CURVE_PATH')
    test_report_path = os.environ.get('TEST_REPORT_PATH', './report')
    test_report_samples = int(os.environ.get('TEST_CURVE_SAMPLES', '0'))
    test_templates(
        test_template_file,
        test_result_file,
        test_curve_path,
        report_path=test_report_path,
        sample=test_report_samples
    )
