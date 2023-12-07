import sys

from PySide6 import QtWidgets
import pyqtgraph as pg
import pandas as pd

from PySide6.QtCore import Slot
import numpy as np

from gammaspotter.process_data import ProcessData


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Gammaspotter GUI utility")

        hbox_main = QtWidgets.QHBoxLayout(central_widget)
        self.plot_widget = pg.PlotWidget()
        hbox_main.addWidget(self.plot_widget)

        vbox_menu = QtWidgets.QVBoxLayout()
        hbox_main.addLayout(vbox_menu)

        form = QtWidgets.QFormLayout()
        vbox_menu.addLayout(form)

        open_btn = QtWidgets.QPushButton("Open Measurement")
        form.addRow(open_btn)

        self.peak_sens_spin = QtWidgets.QSpinBox()
        self.peak_sens_spin.setRange(1, 10000)
        self.peak_sens_spin.setValue(100)
        form.addRow("Peak detection sensitivity", self.peak_sens_spin)

        fit_peaks_btn = QtWidgets.QPushButton("Fit Peaks")
        form.addRow(fit_peaks_btn)

        open_btn.clicked.connect(self.open_file)
        fit_peaks_btn.clicked.connect(self.detect_peaks)

    @Slot()
    def open_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(filter="CSV files (*.csv)")
        if filename:
            self.plot_widget.clear()
            self.plot_widget.setLabel("left", "Counts")
            self.plot_widget.setLabel("bottom", "Energy")

            opened_file = pd.read_csv(filename)
            self.process_data = ProcessData(opened_file)

            current_data = self.process_data.data
            self.plot(x=current_data.iloc[:, 0], y=current_data.iloc[:, 1])

    @Slot()
    def detect_peaks(self):
        peaks_data = self.process_data.find_gamma_peaks(
            prominence=self.peak_sens_spin.value()
        )
        self.plot(x=peaks_data.iloc[:, 0], y=peaks_data.iloc[:, 1])

    def plot(self, x, y):
        self.plot_widget.plot(
            x=np.array(x), y=np.array(y), symbol=None, pen={"color": "w", "width": 5}
        )

    def plot_vline(self, data_feature):
        for x_peak in data_feature:
            self.plot_widget.InfiniteLine(pos=x_peak)


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
