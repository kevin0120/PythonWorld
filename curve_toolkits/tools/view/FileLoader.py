from PyQt5.QtWidgets import QFileDialog
import os


class FileLoader:

    def open_file(self, title: str = "打开文件", file_types: str = "All Files (*)", directory=os.path.expanduser('~'),
                  **kwargs):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            caption=title,
            filter=file_types,
            options=options,
            directory=directory,
            **kwargs
        )
        return file_name

    def open_directory(self, title, directory=os.path.expanduser('~'), **kwargs):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir = QFileDialog.getExistingDirectory(
            caption=title,
            directory=directory,
            options=options,
            **kwargs
        )
        return dir

    def open_files(self, title: str = "打开文件", file_types: str = "All Files (*)", directory=os.path.expanduser('~'),
                  **kwargs):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_names, _ = QFileDialog.getOpenFileNames(
            caption=title,
            filter=file_types,
            options=options,
            directory=directory,
            **kwargs
        )
        return file_names