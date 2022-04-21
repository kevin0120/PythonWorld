# -*- coding: utf-8 -*-
import os
import pandas as pd


class AnalysisBoltsModel:
    bolts = None

    def is_bolts_loaded(self):
        return self.bolts is not None and len(self.bolts['编号']) > 0

    def read_analysis_bolts(self, file_name: str):
        if not file_name:
            raise Exception('未选中编号文件！')
        if not os.path.isfile(file_name):
            raise Exception("打开编号文件必须是一个文件！")
        suffix: str = os.path.splitext(file_name)[-1]
        data: pd.DataFrame = pd.DataFrame()
        if suffix.lower() == '.csv':
            data = pd.read_csv(file_name, names=['编号'])
        if suffix.lower() == '.xlsx':
            data = pd.read_excel(file_name, names=['编号'])
        if data.empty:
            raise Exception("文件: {} 不支持。 只支持CSV或者EXCEL文件!!!")
        self.bolts = data
        return data
