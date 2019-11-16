# -*- coding: utf-8 -*-
import os
import sys
from typing import List
from typing import Optional

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import make_svgs
from ui_main import Ui_main_window

if getattr(sys, 'frozen', False):
    # Running as all-in-one executable.
    bundle_dir = sys._MEIPASS
    cur_dir = os.path.dirname(sys.executable)
else:
    # Running as a console script.
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    cur_dir = os.getcwd()


class MainWindow(QtWidgets.QMainWindow, Ui_main_window):  # type: ignore
    """GUI main window."""

    def __init__(self, parent: Optional[QtWidgets.QWidget]=None) -> None:
        super().__init__(parent)
        self.setupUi(self)  # type: ignore

        default_output_dir = os.path.realpath(
            os.path.join(cur_dir, '..', 'output'))
        self.output_dir.setText(default_output_dir)

        screen_size = QtWidgets.qApp.primaryScreen().size()
        self.setGeometry(
            (screen_size.width() - self.width()) / 2,
            (screen_size.height() - self.height()) / 2,
            self.width(), self.height())

        self.choose_output_dir = QtWidgets.QFileDialog(self)
        self.choose_output_dir.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        self.choose_output_dir.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        self.choose_output_dir.setDirectory(default_output_dir)

        self.browse_dir.clicked.connect(self.choose_output_dir.exec_)
        self.choose_output_dir.directoryEntered[str].connect(self.output_dir.setText)
        self.close_gui.clicked.connect(self.close)
        self.run_script.clicked.connect(self._run)

        default_excel_file = os.path.realpath(
            os.path.join(cur_dir, 'Measurement.xlsx'))

        self.choose_excel_file = QtWidgets.QFileDialog(self)
        self.choose_excel_file.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        self.choose_excel_file.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.choose_excel_file.setDirectory(
            os.path.dirname(default_excel_file))

        self.excelFile.setText(default_excel_file)
        self.browse_excel_file.clicked.connect(self.choose_excel_file.exec_)
        self.choose_excel_file.fileSelected[str].connect(self.excelFile.setText)

    def _run(self) -> None:
        progress = QtWidgets.QProgressDialog(self)
        progress.setRange(0, 100)
        progress.setAutoClose(True)
        progress.setVisible(False)
        progress.setModal(True)
        progress.setMinimumWidth(self.width() / 2)
        progress.setWindowTitle('Running...')

        path = self.output_dir.text() + os.path.sep
        if self.output_svg.isChecked():
            fmt = make_svgs.SVG_FORMAT
        else:
            fmt = make_svgs.PNG_FORMAT

        def _progress_step(percent: float) -> bool:
            frac = percent * 100.0
            progress.setLabelText(
                f'{frac:.2f}% {fmt}s created in {path}...')

            progress.setValue(int(frac))
            QtWidgets.qApp.processEvents()
            return not progress.wasCanceled()

        excel_path = self.excelFile.text()

        QtCore.QTimer.singleShot(
            100, lambda: make_svgs.main(
                raw_table=excel_path,
                custom_raw_table=True,
                output_dir=path,
                output_format=fmt,
                percent_done=_progress_step))

        if progress.exec_() != QtWidgets.QDialog.Accepted:
            QtWidgets.QMessageBox.warning(
                self, 'Running...', 'Script canceled prematurely!')
        self.close()


def main(args: List[str]) -> None:
    app = QtWidgets.QApplication(args)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv[1:])
