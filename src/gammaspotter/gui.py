import sys

from PySide6 import QtWidgets
import pyqtgraph as pg
import pandas as pd

from PySide6.QtCore import Slot
from gammaspotter.process_data import ProcessData
from gammaspotter.match_features import MatchFeatures


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Gammaspotter GUI")

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

        self.peak_thresh_spin = QtWidgets.QSpinBox()
        self.peak_thresh_spin.setRange(1, 1000000)
        self.peak_thresh_spin.setValue(100)
        form.addRow("Peak detection threshold", self.peak_thresh_spin)

        self.domain_width_spin = QtWidgets.QSpinBox()
        self.domain_width_spin.setRange(1, 1000000)
        self.domain_width_spin.setValue(10)
        form.addRow("Fit domain width", self.domain_width_spin)

        grid_buttons = QtWidgets.QGridLayout()
        form.addRow(grid_buttons)

        detect_peaks_btn = QtWidgets.QPushButton("Detect Peaks")
        grid_buttons.addWidget(detect_peaks_btn, 0, 0)
        remove_peaks_btn = QtWidgets.QPushButton("Remove Detected Peaks")
        grid_buttons.addWidget(remove_peaks_btn, 0, 1)

        fit_peaks_btn = QtWidgets.QPushButton("Fit Peaks")
        grid_buttons.addWidget(fit_peaks_btn, 1, 0)
        remove_fit_peaks_btn = QtWidgets.QPushButton("Remove Fit Peaks")
        grid_buttons.addWidget(remove_fit_peaks_btn, 1, 1)

        vbox_menu.addWidget(QtWidgets.QLabel("Analysis Log"))
        self.analysis_log = QtWidgets.QTextEdit()
        self.analysis_log.setReadOnly(True)
        self.analysis_log.append(
            "Gammaspotter by Dylan Telleman and Tijn Schuitevoerder.\n"
        )
        vbox_menu.addWidget(self.analysis_log)

        hbox_clear = QtWidgets.QHBoxLayout()
        vbox_menu.addLayout(hbox_clear)
        clear_analysis_log_btn = QtWidgets.QPushButton("Clear Log")
        hbox_clear.addWidget(clear_analysis_log_btn)
        clear_analysis_plot_btn = QtWidgets.QPushButton("Clear Plot")
        hbox_clear.addWidget(clear_analysis_plot_btn)

        open_btn.clicked.connect(self.open_file)
        clear_analysis_log_btn.clicked.connect(self.clear_analysis_log)
        clear_analysis_plot_btn.clicked.connect(self.clear_analysis_plot)
        remove_peaks_btn.clicked.connect(self.remove_points)
        remove_fit_peaks_btn.clicked.connect(self.remove_vlines)
        detect_peaks_btn.clicked.connect(self.plot_peaks)
        fit_peaks_btn.clicked.connect(self.plot_fit_peaks)

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

        find_peaks_btn = QtWidgets.QPushButton("Find Peaks")
        form.addRow(find_peaks_btn)

        save_cal_btn = QtWidgets.QPushButton("Save Calibrated Measurement")
        form.addRow(save_cal_btn)

        vbox_menu.addWidget(QtWidgets.QLabel("Calibration Log"))
        self.calibration_log = QtWidgets.QTextEdit()
        self.calibration_log.setReadOnly(True)
        self.calibration_log.append(
            "Gammaspotter by Dylan Telleman and Tijn Schuitevoerder.\n"
        )
        vbox_menu.addWidget(self.calibration_log)

        hbox_clear = QtWidgets.QHBoxLayout()
        vbox_menu.addLayout(hbox_clear)
        clear_calibration_log_btn = QtWidgets.QPushButton("Clear Log")
        hbox_clear.addWidget(clear_calibration_log_btn)
        clear_calibration_plot_btn = QtWidgets.QPushButton("Clear Plot")
        hbox_clear.addWidget(clear_calibration_plot_btn)

        open_btn.clicked.connect(self.open_file)
        find_peaks_btn.clicked.connect(self.detect_cal_peaks)
        clear_calibration_log_btn.clicked.connect(self.clear_calibration_log)
        clear_calibration_plot_btn.clicked.connect(self.clear_calibration_plot)

    @Slot()
    def clear_analysis_log(self):
        self.analysis_log.clear()

    @Slot()
    def clear_calibration_log(self):
        self.calibration_log.clear()

    @Slot()
    def clear_analysis_plot(self):
        try:
            del self.process_data_analyze
        except:
            self.analysis_log.append("Nothing to clear.\n")
        else:
            self.plot_widget_analyze.clear()
            self.analysis_log.append("Cleared the plot.\n")

    @Slot()
    def clear_calibration_plot(self):
        try:
            del self.process_data_calibrate
        except:
            self.calibration_log.append("Nothing to clear.\n")
        else:
            self.plot_widget_calibrate.clear()
            self.calibration_log.append("Cleared the plot.\n")

    @Slot()
    def open_file(self):
        """Function for oping a file in to the application. It is possible to open two different files in the two tabs."""
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(filter="CSV files (*.csv)")
        if filename:
            opened_file = pd.read_csv(filename)

            match self.central_widget.currentIndex():
                case 0:
                    plot_widget = self.plot_widget_analyze
                    self.process_data_analyze = ProcessData(opened_file)
                    latest_data = self.process_data_analyze
                    window_log = self.analysis_log

                case 1:
                    plot_widget = self.plot_widget_calibrate
                    self.process_data_calibrate = ProcessData(opened_file)
                    latest_data = self.process_data_calibrate
                    window_log = self.calibration_log

            plot_widget.clear()

            plot_widget.setLabel("left", "Counts")
            plot_widget.setLabel("bottom", "Energy")

            spectrum_data = latest_data.data
            plot_widget.plot(
                x=spectrum_data.iloc[:, 0],
                y=spectrum_data.iloc[:, 1],
                symbol=None,
                pen={"color": "w", "width": 3},
            )
            window_log.append(f"Opened {filename}.\n")

    @Slot()
    def plot_peaks(self):
        """Function for finding the peaks in the plot."""
        try:
            self.plot_widget_analyze.removeItem(self.peaks_scatter)
        except:
            pass
        try:
            peaks_data = self.process_data_analyze.find_gamma_peaks(
                prominence=self.peak_thresh_spin.value()
            )
        except:
            self.analysis_log.append("No data has been loaded.\n")
            return
        self.peaks_scatter = pg.ScatterPlotItem(
            size=15, brush=pg.mkBrush("r"), symbol="x"
        )
        self.peaks_scatter.addPoints(x=peaks_data.iloc[:, 0], y=peaks_data.iloc[:, 1])
        self.plot_widget_analyze.addItem(self.peaks_scatter)

        self.analysis_log.append(
            f"Detected {len(peaks_data)} peaks:\n{peaks_data.to_markdown(index=False, tablefmt='plain', headers=['Energy', 'Counts'])}\n"
        )

    @Slot()
    def plot_fit_peaks(self):
        """Function for fitting the peaks to a gaussian function for finding a more accurate peak and showing this in the plot."""
        try:
            for vline in self.vlines:
                self.plot_widget_analyze.removeItem(vline)
        except:
            pass
        try:
            fit_peaks_x = self.process_data_analyze.fit_peaks(
                domain_width=self.domain_width_spin.value(),
                prominence=self.peak_thresh_spin.value(),
            )
        except:
            self.analysis_log.append("No data has been loaded.\n")
            return

        self.vlines = []
        for x_peak in fit_peaks_x.iloc[:, 0]:
            vline = pg.InfiniteLine(pos=x_peak, label=f"{round(x_peak, 1)}")
            self.vlines.append(vline)
            self.plot_widget_analyze.addItem(vline)

        self.analysis_log.append(
            f"Fitted {len(fit_peaks_x)} peaks:\n{fit_peaks_x.to_markdown(index=False, tablefmt='plain', headers=['Energy', 'Standard Error'])}\n"
        )

    @Slot()
    def remove_points(self):
        try:
            self.plot_widget_analyze.removeItem(self.peaks_scatter)
            self.analysis_log.append("Points have been removed.\n")
        except:
            self.analysis_log.append("There are no points to remove.\n")

    @Slot()
    def remove_vlines(self):
        try:
            for vline in self.vlines:
                self.plot_widget_analyze.removeItem(vline)
            self.analysis_log.append("Peak fit lines have been removed.\n")
        except:
            self.analysis_log.append("There are no lines to remove.\n")

    # maybe move this to model
    def detect_cal_peaks(self):
        """Find the six most prominent peaks in the calibration spectrum."""
        found_peaks_count = 10000
        prominence = 10
        while found_peaks_count > 2:
            found_peaks = self.process_data_calibrate.fit_peaks(
                domain_width=10, prominence=prominence
            )
            found_peaks_count = len(found_peaks)
            prominence += 50

        self.vlines_cal = []
        for x_peak in found_peaks.iloc[:, 0]:
            vline = pg.InfiniteLine(pos=x_peak, label=f"{round(x_peak, 1)}")
            self.vlines_cal.append(vline)
            self.plot_widget_calibrate.addItem(vline)

        self.calibration_log.append(
            f"Detected {len(found_peaks)} peaks:\n{found_peaks.to_markdown(index=False, tablefmt='plain', headers=['Energy', 'Counts'])}\n"
        )


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
