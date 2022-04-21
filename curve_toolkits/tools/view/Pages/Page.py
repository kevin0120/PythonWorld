from PyQt5 import QtWidgets  # import PyQt5 widgets


class Page(QtWidgets.QWidget):
    def __init__(self, ui: QtWidgets.QWidget, window):
        super(Page, self).__init__()
        self._ui = ui
        self.window = window

    @property
    def ui(self) -> QtWidgets.QWidget:
        return self._ui
