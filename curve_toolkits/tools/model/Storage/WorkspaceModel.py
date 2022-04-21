from os import path
import os
from loguru import logger


class WorkspaceModel:
    def __init__(self):
        self._workspace = None
        self._default_workspace = path.join(os.path.expanduser('~'), 'curve_toolkits/workspace')

    def set_working_dir(self, dir=None):
        if dir is not None:
            self._workspace = dir
        if self._workspace is None:
            self._workspace = path.abspath(self._default_workspace)
        if not path.exists(self._workspace):
            logger.info('正在创建工作空间')
            os.makedirs(self._workspace)
        logger.info(self._workspace)
        return self._workspace

    @property
    def workspace(self):
        return self._workspace

    @property
    def template_curves_dir(self):
        template_curves_dir = path.join(self._workspace, 'template_curves')
        if path.isdir(template_curves_dir):
            return template_curves_dir
        os.makedirs(template_curves_dir)


workspace_model = WorkspaceModel()
