from typing import TypeVar, Generic, List
import json
import pandas as pd
from tools.model.ViewingTemplateModel import ViewingTemplateModel

TTemplateRenderModel = TypeVar('TTemplateRenderModel', covariant=True)


def format_template_key(source, bolt, mode, group):
    return '{}/{}/{}/{}'.format(source, bolt, mode, group)


class TemplateRenderModel(Generic[TTemplateRenderModel]):
    def __init__(self, index_column: str = '编号', template_columns: List[str] = None, extra_columns: List[str] = None):
        self._index_column = index_column
        self._template_columns = template_columns
        self._extra_columns = extra_columns
        self._selected_bolt = ViewingTemplateModel()  # 当前激活的螺栓编号

        columns = [index_column]
        if template_columns is not None:
            columns.extend(template_columns)
        if extra_columns is not None:
            columns.extend(extra_columns)
        df = pd.DataFrame(columns=columns)
        self._templates = df.set_index(index_column)

    def set_current_bolt(self, bolt: str):
        self._selected_bolt.set_bolt_number(bolt)

    @property
    def current_bolt(self):
        return self._selected_bolt.bolt_number

    @property
    def templates(self):
        return self._templates

    def get_current_row_data(self, name):
        return self.templates.loc[self.current_bolt, name]

    def set_current_row_data(self, name, value):
        self.templates.loc[self.current_bolt, name] = value

    def set_bolts(self, bolts: pd.DataFrame):
        self._templates = pd.merge(self._templates, bolts, on=[self._index_column], how='right')
        self._templates = self._templates.set_index(self._index_column)

    def add_bolts(self, bolts: pd.DataFrame):
        # TODO: 实现追加对比螺栓
        pass

    def get_table_content(self, columns: List[str] = None) -> pd.DataFrame:
        if columns is None:
            return pd.DataFrame(self._templates.reset_index())
        return pd.DataFrame(self._templates.reset_index()[columns])

    def _load_template_data(self, bolt: str, key: str):
        json_data = self._templates.loc[bolt, key]
        if pd.isnull(json_data):
            return {}
        return json.loads(json_data)

    @property
    def render_curve_params(self):
        return self.get_curve_params(self._selected_bolt.bolt_number)

    def get_curve_params(self, bolt: str):
        result = None
        for key in self._template_columns:
            df = pd.DataFrame([self._load_template_data(bolt, key).get('curve_param')]).T
            df.rename(columns={0: key}, inplace=True)
            if result is None:
                result = df
            else:
                result = pd.merge(result, df, how='outer', left_index=True, right_index=True)
        result = result.reset_index()
        result.rename(columns={'index': '参数'}, inplace=True)
        return result

    def _format_template(self, bolt, source):
        template_cluster = self._load_template_data(bolt, source).get('template_cluster', None)
        sampling_time = self._load_template_data(bolt, source).get('curve_param', {}).get('sampling_time', None)
        if not template_cluster or not sampling_time:
            return {}
        template_curves = {}
        for mode in template_cluster.keys():
            curve_template_group_array = template_cluster[mode]['curve_template_group_array']
            for group in range(len(curve_template_group_array)):
                template_centroid_index = curve_template_group_array[group]['template_centroid_index']
                centroid_curve = curve_template_group_array[group]['template_data_array'][template_centroid_index]
                centroid_curve["template_time"] = list(
                    i * sampling_time for i in range(len(centroid_curve["template_torque"])))
                template_curves.update({
                    format_template_key(source, bolt, mode, group): centroid_curve
                })
        return template_curves

    @property
    def render_curves(self):
        return self.get_curves(self._selected_bolt.bolt_number)

    def get_curves(self, bolt: str):
        curves = {}
        for key in self._template_columns:
            curves.update(self._format_template(bolt, key))
        return curves

    def load_templates(self, templates, col_name):
        if not templates or not col_name:
            return
        bolts = [k.split('/')[0] for k in templates.keys()]
        for bolt in bolts:
            for key in templates.keys():
                if bolt in key:
                    self._templates.loc[bolt, col_name] = json.dumps(templates[key]) if templates[key] else None

    def merge_data(self, other, *args, **kwargs):
        self._templates = pd.merge(self._templates, other, *args, **kwargs)

    def update(self, other, *args, **kwargs):
        # changed = other.combine_first(self._templates)
        self._templates: pd.DataFrame = self._templates.combine_first(other)
        self._templates.update(other)
        return
