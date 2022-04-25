# -*- coding: utf-8 -*-
from PyQt5.QtCore import QUrl

from tools.view.mixin import ToolKitMixin
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from typing import Union
import numpy as np
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
import os
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Chart(ToolKitMixin):
    """
    曲线可视化图表
    """

    def __init__(self, instance: QWebEngineView, title: str, cache_dir):
        super(Chart, self).__init__(instance)
        self._title = title
        self._cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        self._theme = ThemeType.LIGHT
        self._chart = Line(
            init_opts=opts.InitOpts(
                theme=self._theme,
                width='100%',
                height='100%'
            )
        ).set_global_opts(
            title_opts=opts.TitleOpts(title="模板中心曲线", subtitle="砺星曲线分析"),
            datazoom_opts=opts.DataZoomOpts(
                range_start=0,
                range_end=100,
                xaxis_index=0
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross"
            ),
            toolbox_opts=opts.ToolboxOpts(
                pos_left='70%',
                feature=opts.ToolBoxFeatureOpts(
                    magic_type=opts.ToolBoxFeatureMagicTypeOpts(
                        is_show=False
                    )
                )
            ),
            brush_opts=opts.BrushOpts(
                x_axis_index="all",
                y_axis_index="all",
                brush_link="all",
                out_of_brush={"colorAlpha": 0.1},
                brush_type="lineX",
            ),
        )

    @property
    def view(self) -> QWebEngineView:
        return self.qt_instance

    def show(self):
        self.view.show()

    def set_series(self, series=None):
        if not series:
            series = []
        chart: Union[Line, Bar] = self._chart
        if not chart:
            return
        chart.options['series'] = series
        max_x = 1
        x_axis_series = np.arange(max_x)  # 此数据不重要
        chart.add_xaxis(x_axis_series)
        if not self.view or not chart:
            return
        html_data = chart.render_embed("simple_chart.html", Environment(
            loader=FileSystemLoader(
                os.path.join(
                    os.path.abspath(os.path.dirname(__file__)), "../../templates"
                )
            )
        ))
        cache_file = os.path.join(self._cache_dir, f"{self.view.objectName()}_cache.html")
        with open(cache_file, 'w') as f:
            f.write(html_data)
        self.view.setUrl(QUrl.fromLocalFile(cache_file))
