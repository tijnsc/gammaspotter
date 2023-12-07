import sys

from PySide6 import QtWidgets
import pyqtgraph as pg
import pandas as pd

from PySide6.QtCore import Slot

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
            opened_file = pd.read_csv(filename)

            self.process_data = ProcessData(opened_file)
            
            current_data = self.process_data.data
            self.energy = current_data.iloc[:, 0]
            self.counts = current_data.iloc[:, 1]
            self.plot()

    def plot(self):
        self.plot_widget.plot(
            x=self.energy, y=self.counts, symbol=None, pen={"color": "w", "width": 5}
        )
        self.plot_widget.setLabel("left", "Counts")
        self.plot_widget.setLabel("bottom", "Energy")


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
