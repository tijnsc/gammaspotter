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
        self.help_tab = QtWidgets.QWidget()

        self.central_widget.addTab(self.analyze_tab, "Analyze")
        self.central_widget.addTab(self.calibrate_tab, "Calibrate")
        self.central_widget.addTab(self.help_tab, "Help")

        self.setup_analyze_tab()
        self.setup_calibrate_tab()
        self.setup_help_tab()

    def setup_analyze_tab(self):
        hbox_main = QtWidgets.QHBoxLayout(self.analyze_tab)
        self.plot_widget_analyze = pg.PlotWidget()
        hbox_main.addWidget(self.plot_widget_analyze)

        vbox_menu = QtWidgets.QVBoxLayout()
        hbox_main.addLayout(vbox_menu)

        form = QtWidgets.QFormLayout()
        vbox_menu.addLayout(form)

        open_btn = QtWidgets.QPushButton("Open calibrated data")
        form.addRow(open_btn)

        self.peak_thresh_spin = QtWidgets.QSpinBox()
        self.peak_thresh_spin.setSingleStep(15)
        self.peak_thresh_spin.setRange(1, 1000000)
        self.peak_thresh_spin.setValue(100)
        form.addRow("Peak detection threshold", self.peak_thresh_spin)

        self.peaks_checkbox = QtWidgets.QCheckBox()
        form.addRow("Show detected peaks", self.peaks_checkbox)

        self.domain_width_spin = QtWidgets.QSpinBox()
        self.domain_width_spin.setSingleStep(5)
        self.domain_width_spin.setRange(1, 1000000)
        self.domain_width_spin.setValue(60)
        form.addRow("Fit domain width", self.domain_width_spin)

        self.fit_checkbox = QtWidgets.QCheckBox()
        form.addRow("Show fitted peaks", self.fit_checkbox)

        self.match_isotopes_btn = QtWidgets.QPushButton("Match Isotopes")
        form.addRow(self.match_isotopes_btn)

        self.result_length_spin = QtWidgets.QSpinBox()
        self.result_length_spin.setSingleStep(1)
        self.result_length_spin.setRange(1, 100)
        self.result_length_spin.setValue(5)
        form.addRow("Max. results per peak", self.result_length_spin)

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        form.addRow(line)

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
        clear_analysis_data_btn = QtWidgets.QPushButton("Clear Data")
        hbox_clear.addWidget(clear_analysis_data_btn)

        self.show_analysis_funcs(False)

        open_btn.clicked.connect(self.open_file)

        self.peak_thresh_spin.valueChanged.connect(self.plot_peaks)
        self.peaks_checkbox.stateChanged.connect(self.plot_peaks)

        self.peak_thresh_spin.valueChanged.connect(self.plot_fit_peaks)
        self.domain_width_spin.valueChanged.connect(self.plot_fit_peaks)
        self.fit_checkbox.stateChanged.connect(self.plot_fit_peaks)

        self.match_isotopes_btn.clicked.connect(self.find_isotopes)

        clear_analysis_log_btn.clicked.connect(self.clear_analysis_log)
        clear_analysis_data_btn.clicked.connect(self.clear_analysis_data)

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

        self.find_peaks_btn = QtWidgets.QPushButton("Find Peaks")
        form.addRow(self.find_peaks_btn)

        self.save_cal_btn = QtWidgets.QPushButton("Save calibrated data")
        form.addRow(self.save_cal_btn)

        self.send_to_analysis_btn = QtWidgets.QPushButton("Send data to analyze tab")
        form.addRow(self.send_to_analysis_btn)

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        form.addRow(line)

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
        clear_calibration_data_btn = QtWidgets.QPushButton("Clear Data")
        hbox_clear.addWidget(clear_calibration_data_btn)

        self.show_calibrate_funcs(False)

        open_btn.clicked.connect(self.open_file)
        self.find_peaks_btn.clicked.connect(self.detect_cal_peaks)
        self.send_to_analysis_btn.clicked.connect(self.send_to_analysis)

        clear_calibration_log_btn.clicked.connect(self.clear_calibration_log)
        clear_calibration_data_btn.clicked.connect(self.clear_calibration_data)

    def setup_help_tab(self):
        vbox_main = QtWidgets.QVBoxLayout(self.help_tab)

        hbox_btns = QtWidgets.QHBoxLayout()
        vbox_main.addLayout(hbox_btns)

        self.analyze_button = QtWidgets.QPushButton("Help with analysis")
        hbox_btns.addWidget(self.analyze_button)

        self.calibrate_button = QtWidgets.QPushButton("Help with calibration")
        hbox_btns.addWidget(self.calibrate_button)

        self.analyze_button.clicked.connect(self.analyze_help)
        self.calibrate_button.clicked.connect(self.calibrate_help)

        vbox_main.addWidget(QtWidgets.QLabel("Helpdesk"))
        self.help_log = QtWidgets.QTextEdit()
        self.help_log.setReadOnly(True)
        self.help_log.append(
            """This is a helpdesk for if you find yourself having problems with the program.
Choose which tab you having problems with.

Hope we can help you well,
Dylan Telleman and Tijn Schuitevoerder
"""
        )
        vbox_main.addWidget(self.help_log)

    def show_analysis_funcs(self, action: bool):
        widgets = [
            self.fit_checkbox,
            self.peaks_checkbox,
            self.peak_thresh_spin,
            self.domain_width_spin,
            self.match_isotopes_btn,
            self.result_length_spin,
        ]
        for widget in widgets:
            widget.setEnabled(action)

        # reset checkboxes to unchecked state
        checkboxes = [self.fit_checkbox, self.peaks_checkbox]
        for checkbox in checkboxes:
            checkbox.setChecked(False)

    def show_calibrate_funcs(self, action: bool):
        widgets = [
            self.combo_isotope,
            self.find_peaks_btn,
            self.save_cal_btn,
            self.send_to_analysis_btn,
        ]
        for widget in widgets:
            widget.setEnabled(action)

    @Slot()
    def clear_analysis_log(self):
        self.analysis_log.clear()

    @Slot()
    def clear_calibration_log(self):
        self.calibration_log.clear()

    @Slot()
    def clear_analysis_data(self):
        try:
            del self.process_data_analyze
        except:
            pass
        else:
            self.show_analysis_funcs(False)
            self.plot_widget_analyze.clear()

    @Slot()
    def clear_calibration_data(self):
        try:
            del self.process_data_calibrate
        except:
            pass
        else:
            self.show_calibrate_funcs(False)
            self.plot_widget_calibrate.clear()

    @Slot()
    def send_to_analysis(self):
        self.central_widget.setCurrentIndex(0)

    @Slot()
    def open_file(self):
        """Function for oping a file in to the application. It is possible to open two different files in the two tabs."""
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(filter="CSV files (*.csv)")
        if filename:
            opened_file = pd.read_csv(filename)

            match self.central_widget.currentIndex():
                case 0:
                    self.clear_analysis_data()
                    plot_widget = self.plot_widget_analyze
                    self.process_data_analyze = ProcessData(opened_file)
                    latest_data = self.process_data_analyze
                    window_log = self.analysis_log
                    self.show_analysis_funcs(True)
                    x_unit = "keV"

                case 1:
                    self.clear_calibration_data()
                    plot_widget = self.plot_widget_calibrate
                    self.process_data_calibrate = ProcessData(opened_file)
                    latest_data = self.process_data_calibrate
                    window_log = self.calibration_log
                    self.show_calibrate_funcs(True)
                    x_unit = "mV"

            plot_widget.clear()

            plot_widget.setLabel("left", "Counts")
            plot_widget.setLabel("bottom", f"Energy [{x_unit}]")

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

        if self.peaks_checkbox.isChecked():
            peaks_data = self.process_data_analyze.find_gamma_peaks(
                prominence=self.peak_thresh_spin.value()
            )
            self.peaks_scatter = pg.ScatterPlotItem(
                size=15, brush=pg.mkBrush("r"), symbol="x"
            )
            self.peaks_scatter.addPoints(
                x=peaks_data.iloc[:, 0], y=peaks_data.iloc[:, 1]
            )
            self.plot_widget_analyze.addItem(self.peaks_scatter)

            self.analysis_log.append(
                f"DETECTED {len(peaks_data)} PEAKS:\n{peaks_data.to_markdown(index=False, tablefmt='plain', headers=['Energy [keV]', 'Counts'])}\n"
            )

    @Slot()
    def plot_fit_peaks(self):
        """Function for fitting the peaks to a gaussian function for finding a more accurate peak and showing this in the plot."""
        try:
            for vline in self.vlines:
                self.plot_widget_analyze.removeItem(vline)
        except:
            pass

        if self.fit_checkbox.isChecked():
            try:
                self.fit_peaks_x = self.process_data_analyze.fit_peaks(
                    domain_width=self.domain_width_spin.value(),
                    prominence=self.peak_thresh_spin.value(),
                )
            except TypeError:
                self.analysis_log.append(
                    "No peaks detected. Try lowering the peak detection threshold or adjusting the domain width.\n"
                )
            else:
                self.vlines = []
                for peak_nr, x_peak in enumerate(self.fit_peaks_x.iloc[:, 0]):
                    vline = pg.InfiniteLine(pos=x_peak, label=f"{peak_nr + 1}")
                    self.vlines.append(vline)
                    self.plot_widget_analyze.addItem(vline)

                self.analysis_log.append(
                    f"FITTED {len(self.fit_peaks_x)} PEAKS:\n{self.fit_peaks_x.to_markdown(index=False, tablefmt='plain', headers=['Energy [keV]', 'Standard Error'])}\n"
                )

    # maybe move this to model
    @Slot()
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
            f"DETECTED {len(found_peaks)} PEAKS:\n{found_peaks.to_markdown(index=False, tablefmt='plain', headers=['Energy [mV]', 'Counts'])}\n"
        )

    @Slot()
    def find_isotopes(self):
        try:
            mf = MatchFeatures(self.fit_peaks_x)
        except AttributeError:
            self.analysis_log.append("No peaks fitted. Try fitting the peaks first.\n")
        else:
            matches = mf.match_isotopes()
            result_length = self.result_length_spin.value()
            self.analysis_log.append("MATCHED PEAKS:")
            for index in range(len(self.fit_peaks_x)):
                peak_nr = index + 1

                # gets the first result_length rows of the matches dataframe where the peak numbers match
                peak_matches = matches[matches.iloc[:, 0] == peak_nr].iloc[
                    :result_length, 1:3
                ]
                if len(peak_matches) > 0:
                    self.analysis_log.append(
                        f"--- Peak {peak_nr} matches with:\n{peak_matches.to_markdown(index=False, tablefmt='plain', headers=['Isotope', 'Certainty [%]'])}"
                    )
                else:
                    self.analysis_log.append(f"--- Peak {peak_nr} has no matches.")
            self.analysis_log.append("\n")

    @Slot()
    def analyze_help(self):
        self.help_log.clear()
        self.help_log.append(
            """On the right hand side of the application you can see an 'Open Measurement' button.
This is where you can choose which measurement you want to use.

Right under the button there is a changable box 'Peak detection treshold'
This determines how sensitive the program is with finding the peaks.
When the threshold is set higher it will find less peaks.

Under the treshold there is a changable box 'Fit domain width'.
You can change how wide you want to fit over the found peaks.
"""
        )

    @Slot()
    def calibrate_help(self):
        self.help_log.clear()
        self.help_log.append(
            "This is the information for helping with the calibrate tab."
        )


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
