from ..model.CurveModel import CurveModel
from ..utils.curve import select_curve_from_filesystem, select_curves_from_filesystem
from ..view.Pages.CurveAnalysisPage import CurveAnalysisPage
from loguru import logger


class CurveAnalysisController:
    def __init__(self, page: CurveAnalysisPage):
        page.connect_add_curve(self.add_curve)
        page.connect_remove_curve(self.remove_curve)
        page.connect_select_curve(self.select_curve)
        self.page = page
        self.selected_curve = None

    def select_curve(self, curve):
        self.selected_curve = curve

    def add_curve(self):
        file_names = select_curves_from_filesystem()
        logger.info('add curve')
        logger.info(file_names)
        if not file_names or len(file_names) == 0:
            return
        for file_name in file_names:
            curve = CurveModel.from_file(file_name)
            self.page.add_curve(name=file_name, curve_data={
                'angle_torque': curve.series_angle_torque,
                'time_torque': curve.series_time_torque,
                'time_angle': curve.series_time_angle,
                'torque_rate': curve.series_torque_rate,
                'turning_state': curve.series_turning_state
            })

    def remove_curve(self):
        if self.selected_curve is None:
            return
        logger.info('remove curve')
        self.page.remove_curve(self.selected_curve)
        self.selected_curve = None
