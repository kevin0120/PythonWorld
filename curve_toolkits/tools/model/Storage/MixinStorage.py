from os import path
from tools.model.Storage.WorkspaceModel import workspace_model
from tools.utils.storage import ensure_exist


class MixinStorage:
    _sub_path = ''

    @property
    def storage_dir(self):
        if workspace_model is None:
            raise Exception('工作空间未定义')
        return ensure_exist(path.join(workspace_model.workspace, self._sub_path))
