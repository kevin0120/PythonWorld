from ..model.CurveModel import CurveModel
from ..utils.curve import select_curve_from_filesystem
from ..view.Pages.CurveComparePage import CurveComparePage
from loguru import logger


class CurveCompareController:
    def __init__(self, page: CurveComparePage):
        page.connect_add_curve(self.add_curve)
        page.connect_remove_curve(self.remove_curve)
        self.page = page

    def add_curve(self):
        file_name = select_curve_from_filesystem()
        logger.info('add curve')
        logger.info(file_name)
        if not file_name:
            return
        curve = CurveModel.from_file(file_name)
        self.page.add_curve(name=file_name, curve_data={
            'torque': curve.series_time_torque,
            'angle': curve.series_time_angle
        })

    def remove_curve(self):
        logger.info('remove curve')
