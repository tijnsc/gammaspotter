import sys

from PySide6 import QtWidgets
import pyqtgraph as pg
import pandas as pd

from PySide6.QtCore import Slot

from gammaspotter.process_data import ProcessData


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Gammaspotter GUI utility")

        self.analyze_tab = QtWidgets.QWidget()
        self.calibrate_tab = QtWidgets.QWidget()

        self.central_widget.addTab(self.analyze_tab, "Analyze")
        self.central_widget.addTab(self.calibrate_tab, "Calibrate")

        self.setup_analyze_tab()
        self.setup_calibrate_tab()

    def setup_analyze_tab(self):
        hbox_main = QtWidgets.QHBoxLayout(self.analyze_tab)
        self.plot_widget_analyze = pg.PlotWidget()
        hbox_main.addWidget(self.plot_widget_analyze)

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

        hbox_peaks = QtWidgets.QHBoxLayout()
        form.addRow(hbox_peaks)

        detect_peaks_btn = QtWidgets.QPushButton("Detect Peaks")
        hbox_peaks.addWidget(detect_peaks_btn)

        remove_peaks_btn = QtWidgets.QPushButton("Remove Peaks")
        hbox_peaks.addWidget(remove_peaks_btn)

        open_btn.clicked.connect(self.open_file)
        detect_peaks_btn.clicked.connect(self.plot_peaks)
        remove_peaks_btn.clicked.connect(self.remove_points)

    def setup_calibrate_tab(self):
        hbox_main = QtWidgets.QHBoxLayout(self.calibrate_tab)
        self.plot_widget_calibrate = pg.PlotWidget()
        hbox_main.addWidget(self.plot_widget_calibrate)

        vbox_menu = QtWidgets.QVBoxLayout()
        hbox_main.addLayout(vbox_menu)

        form = QtWidgets.QFormLayout()
        vbox_menu.addLayout(form)

        open_btn = QtWidgets.QPushButton("Open Measurement")
        form.addRow(open_btn)

        self.combo_isotope = QtWidgets.QComboBox()
        self.combo_isotope.addItems(["Na-22", "Cs-137"])
        form.addRow("Measured Isotope", self.combo_isotope)

        open_btn.clicked.connect(self.open_file)

    @Slot()
    def open_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(filter="CSV files (*.csv)")
        if filename:
            opened_file = pd.read_csv(filename)

            match self.central_widget.currentIndex():
                case 0:
                    plot_widget = self.plot_widget_analyze
                    self.process_data_analyze = ProcessData(opened_file)
                    latest_data = self.process_data_analyze

                case 1:
                    plot_widget = self.plot_widget_calibrate
                    self.process_data_calibrate = ProcessData(opened_file)
                    latest_data = self.process_data_calibrate

            plot_widget.clear()

            spectrum_data = latest_data.data
            plot_widget.plot(
                x=spectrum_data.iloc[:, 0],
                y=spectrum_data.iloc[:, 1],
                symbol=None,
                pen={"color": "w", "width": 5},
            )

    @Slot()
    def plot_peaks(self):
        try:
            self.plot_widget_analyze.removeItem(self.peaks_scatter)
        except:
            pass
        peaks_data = self.process_data_analyze.find_gamma_peaks(
            prominence=self.peak_sens_spin.value()
        )
        self.peaks_scatter = pg.ScatterPlotItem(
            size=10, brush=pg.mkBrush("r"), symbol="+"
        )
        self.peaks_scatter.addPoints(x=peaks_data.iloc[:, 0], y=peaks_data.iloc[:, 1])

        self.plot_widget_analyze.addItem(self.peaks_scatter)

    @Slot()
    def remove_points(self):
        self.plot_widget_analyze.removeItem(self.peaks_scatter)

    def plot_vline(self, data_feature):
        for x_peak in data_feature:
            self.plot_widget_analyze.InfiniteLine(pos=x_peak)


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
