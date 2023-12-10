import sys

from PySide6 import QtWidgets
from PySide6.QtWebEngineWidgets import QWebEngineView
import pyqtgraph as pg
import pandas as pd
from collections import deque
from pathlib import Path

from PySide6.QtCore import Slot, QUrl, Qt
from gammaspotter.process_data import ProcessData
from gammaspotter.match_features import MatchFeatures


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # load default isotope catalog
        self.isotope_catalog = pd.read_csv("catalogs/gamma-energies-common.csv")
        self.catalog_name = "default catalog"

        self.central_widget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Gammaspotter GUI")

        self.calibrate_tab = QtWidgets.QWidget()
        self.analyze_tab = QtWidgets.QWidget()
        self.help_tab = QtWidgets.QWidget()

        self.central_widget.addTab(self.calibrate_tab, "Calibrate")
        self.central_widget.addTab(self.analyze_tab, "Analyze")
        self.central_widget.addTab(self.help_tab, "Help")

        self.setup_calibrate_tab()
        self.setup_analyze_tab()
        self.setup_help_tab()

    def setup_calibrate_tab(self):
        hbox_main = QtWidgets.QHBoxLayout(self.calibrate_tab)
        self.plot_widget_calibrate = pg.PlotWidget()
        self.cal_data_loaded = False
        hbox_main.addWidget(self.plot_widget_calibrate)

        vbox_menu = QtWidgets.QVBoxLayout()
        hbox_main.addLayout(vbox_menu)

        form = QtWidgets.QFormLayout()
        vbox_menu.addLayout(form)

        open_btn = QtWidgets.QPushButton("Open Measurement")
        form.addRow(open_btn)

        self.reset_axis_btn = QtWidgets.QPushButton("Reset Axis")
        form.addRow(self.reset_axis_btn)

        self.domain_width_spin_cal = QtWidgets.QSpinBox()
        self.domain_width_spin_cal.setSingleStep(1)
        self.domain_width_spin_cal.setRange(1, 1000000)
        self.domain_width_spin_cal.setValue(5)
        form.addRow("Domain width", self.domain_width_spin_cal)

        self.preset_energies = QtWidgets.QComboBox()
        self.preset_energies.addItems(["---", "Na-22"])
        form.addRow("Preset energies", self.preset_energies)

        self.energy_spin_1 = QtWidgets.QDoubleSpinBox()
        self.energy_spin_1.setSingleStep(0.1)
        self.energy_spin_1.setRange(0, 1000000)
        self.energy_spin_1.setValue(0)
        form.addRow("Energy 1 [keV]", self.energy_spin_1)

        self.energy_spin_2 = QtWidgets.QDoubleSpinBox()
        self.energy_spin_2.setSingleStep(0.1)
        self.energy_spin_2.setRange(0, 1000000)
        self.energy_spin_2.setValue(0)
        form.addRow("Energy 2 [keV]", self.energy_spin_2)

        self.calc_factors_btn = QtWidgets.QPushButton("Calculate Conversion Factors")
        form.addRow(self.calc_factors_btn)

        self.apply_cal_btn = QtWidgets.QPushButton("Apply Calibration To Files")
        form.addRow(self.apply_cal_btn)

        self.allow_calibration_steps(False)

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

        self.v_line_mouse_left = pg.InfiniteLine(pen=pg.mkPen(color="g", width=1))
        self.v_line_mouse_right = pg.InfiniteLine(pen=pg.mkPen(color="g", width=1))

        self.show_calibrate_funcs(False)

        self.plot_widget_calibrate.scene().sigMouseMoved.connect(self.cal_mouse_domain)
        self.plot_widget_calibrate.scene().sigMouseClicked.connect(
            self.add_calibration_point
        )

        self.preset_energies.currentIndexChanged.connect(self.set_preset_energies)
        self.calc_factors_btn.clicked.connect(self.calc_cal_factors)

        open_btn.clicked.connect(self.open_file)
        self.reset_axis_btn.clicked.connect(self.plot_widget_calibrate.autoRange)
        self.apply_cal_btn.clicked.connect(self.apply_calibration)

        clear_calibration_log_btn.clicked.connect(self.clear_calibration_log)
        clear_calibration_data_btn.clicked.connect(self.clear_calibration_data)

    def setup_analyze_tab(self):
        hbox_main = QtWidgets.QHBoxLayout(self.analyze_tab)
        self.plot_widget_analyze = pg.PlotWidget()
        self.analyze_data_loaded = False
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

        match_hbox = QtWidgets.QHBoxLayout()
        form.addRow(match_hbox)

        self.match_isotopes_btn = QtWidgets.QPushButton("Match isotopes")
        match_hbox.addWidget(self.match_isotopes_btn)

        self.load_alt_catalog_btn = QtWidgets.QPushButton("Load alternative catalog")
        match_hbox.addWidget(self.load_alt_catalog_btn)

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

        self.load_alt_catalog_btn.clicked.connect(self.load_catalog)
        self.match_isotopes_btn.clicked.connect(self.find_isotopes)

        clear_analysis_log_btn.clicked.connect(self.clear_analysis_log)
        clear_analysis_data_btn.clicked.connect(self.clear_analysis_data)

    def setup_help_tab(self):
        vbox_main = QtWidgets.QVBoxLayout(self.help_tab)

        self.webEngineView = QWebEngineView()
        self.webEngineView.load(QUrl("https://tijnsc.github.io/gammaspotter"))
        vbox_main.addWidget(self.webEngineView)

    def show_analysis_funcs(self, action: bool):
        widgets = [
            self.fit_checkbox,
            self.peaks_checkbox,
            self.peak_thresh_spin,
            self.domain_width_spin,
            self.match_isotopes_btn,
            self.result_length_spin,
            self.load_alt_catalog_btn,
        ]
        for widget in widgets:
            widget.setEnabled(action)

        # reset checkboxes to unchecked state
        checkboxes = [self.fit_checkbox, self.peaks_checkbox]
        for checkbox in checkboxes:
            checkbox.setChecked(False)

    def show_calibrate_funcs(self, action: bool):
        widgets = [
            self.reset_axis_btn,
            self.domain_width_spin_cal,
            # self.find_peaks_btn,
            # self.save_cal_btn,
            # self.send_to_analysis_btn,
        ]
        for widget in widgets:
            widget.setEnabled(action)

    @Slot()
    def set_preset_energies(self):
        match self.preset_energies.currentText():
            case "---":
                self.energy_spin_1.setValue(0)
                self.energy_spin_2.setValue(0)
            case "Na-22":
                self.energy_spin_1.setValue(511.0034)
                self.energy_spin_2.setValue(1274.5)

    @Slot()
    def load_catalog(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(filter="CSV files (*.csv)")
        if filename:
            self.isotope_catalog = pd.read_csv(filename)
            self.catalog_name = filename.split("/")[-1]
            self.analysis_log.append(
                f"Loaded {self.catalog_name} with {len(self.isotope_catalog)} entries as custom catalog.\n"
            )

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
            self.analyze_data_loaded = False
            self.show_analysis_funcs(False)
            self.plot_widget_analyze.clear()
            self.plot_widget_analyze.setTitle("")

    @Slot()
    def clear_calibration_data(self):
        try:
            del self.process_data_calibrate
        except:
            pass
        else:
            self.cal_data_loaded = False
            self.show_calibrate_funcs(False)
            self.plot_widget_calibrate.clear()
            self.plot_widget_calibrate.setTitle("")
        finally:
            # initialize the calibration point deques
            self.cal_click_x = deque(maxlen=2)
            self.cal_click_y = deque(maxlen=2)

            self.allow_calibration_steps(False)

    def allow_calibration_steps(self, action: bool):
        self.energy_spin_1.setEnabled(action)
        self.energy_spin_2.setEnabled(action)
        self.preset_energies.setEnabled(action)
        self.calc_factors_btn.setEnabled(action)
        if not action:
            self.preset_energies.setCurrentIndex(0)

    # @Slot()
    # def send_to_analysis(self):
    #     # reusing code from open_file, might be better to move this to a function
    #     self.central_widget.setCurrentIndex(1)
    #     self.plot_widget_analyze.clear()
    #     self.plot_widget_analyze.setTitle("Calibrated Data")
    #     self.plot_widget_analyze.setLabel("left", "Counts")
    #     self.plot_widget_analyze.setLabel("bottom", "Energy [keV]")
    #     self.plot_widget_analyze.showGrid(x=True, y=True)
    #     self.plot_widget_analyze.plot(
    #         x=self.process_data_calibrate.data.iloc[:, 0],
    #         y=self.process_data_calibrate.data.iloc[:, 1],
    #         symbol=None,
    #         pen={"color": "w", "width": 3},
    #     )
    #     self.process_data_analyze = self.process_data_calibrate
    #     self.calibration_log.append("Sent data to analysis tab.\n")
    #     self.analysis_log.append("Recieved data from calibration tab.\n")
    #     self.show_analysis_funcs(True)

    @Slot()
    def open_file(self):
        """Function for opening a file and showing it in the plot."""
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(filter="CSV files (*.csv)")
        if filename:
            opened_file = pd.read_csv(filename)

            # opened_file.iloc[:, 0] = (
            #     opened_file.iloc[:, 0] * 26.85781161331581 - 33.821059315931734
            # )

            match self.central_widget.currentIndex():
                case 0:
                    self.clear_calibration_data()
                    plot_widget = self.plot_widget_calibrate
                    self.process_data_calibrate = ProcessData(opened_file)
                    latest_data = self.process_data_calibrate
                    window_log = self.calibration_log
                    self.show_calibrate_funcs(True)
                    x_unit = "mV"
                    self.cal_data_loaded = True
                case 1:
                    self.clear_analysis_data()
                    plot_widget = self.plot_widget_analyze
                    self.process_data_analyze = ProcessData(opened_file)
                    latest_data = self.process_data_analyze
                    window_log = self.analysis_log
                    self.show_analysis_funcs(True)
                    x_unit = "keV"
                    self.analyze_data_loaded = True

            plot_widget.clear()

            plot_widget.setTitle(filename.split("/")[-1])
            plot_widget.setLabel("left", "Counts")
            plot_widget.setLabel("bottom", f"Energy [{x_unit}]")
            plot_widget.showGrid(x=True, y=True)

            spectrum_data = latest_data.data
            plot_widget.plot(
                x=spectrum_data.iloc[:, 0],
                y=spectrum_data.iloc[:, 1],
                symbol=None,
                pen={"color": "w", "width": 3},
            )

            plot_widget.autoRange()
            plot_widget.disableAutoRange()
            window_log.append(f"Opened {filename}.\n")

    @Slot()
    def add_calibration_point(self, event):
        if event.button() == Qt.LeftButton:
            pos_click = event.scenePos()
            pos_click = self.plot_widget_calibrate.plotItem.vb.mapSceneToView(pos_click)

            if (
                pos_click.x() > self.process_data_calibrate.data.iloc[:, 0].min()
                and pos_click.x() < self.process_data_calibrate.data.iloc[:, 0].max()
                and pos_click.y() > self.process_data_calibrate.data.iloc[:, 1].min()
                and pos_click.y() < self.process_data_calibrate.data.iloc[:, 1].max()
            ):
                # try except block for when the user clicks before data is loaded
                try:
                    self.cal_click_x.append(pos_click.x())
                    self.cal_click_y.append(pos_click.y())
                except AttributeError:
                    pass
                else:
                    # can have length of 2 at most
                    selected_peaks = pd.DataFrame(
                        {
                            "energy": self.cal_click_x,
                            "counts": self.cal_click_y,
                        }
                    )
                    try:
                        self.fitted_calibration_peaks = (
                            self.process_data_calibrate.fit_peaks(
                                peaks=selected_peaks,
                                domain_width=self.domain_width_spin_cal.value(),
                            )
                        )
                    except RuntimeError:
                        self.calibration_log.append(
                            "The selected peaks could not be analyzed, please try selecting different peaks.\n"
                        )
                        # clear the lines and reset point deques
                        self.plot_vlines_cal([])
                        self.cal_click_x.clear()
                        self.cal_click_y.clear()
                    else:
                        # everything went well, plot the lines and save the energies with uncertainties
                        self.plot_vlines_cal(self.fitted_calibration_peaks["energy"])
                        if len(self.fitted_calibration_peaks) == 2:
                            self.calibration_log.append(
                                f"Selected peaks:\n{self.fitted_calibration_peaks.to_markdown(index=False, tablefmt='plain', headers=['Energy [mV]', 'Std Err [mV]'])}\n"
                            )
            else:
                self.calibration_log.append(
                    "Please select a peak within the range of the data.\n"
                )

    def plot_vlines_cal(self, x_positions: list):
        """Function for plotting the vertical lines in the calibration plot."""
        try:
            for vline in self.vlines_cal:
                self.plot_widget_calibrate.removeItem(vline)
        except:
            pass
        self.vlines_cal = []
        for x_peak in x_positions:
            vline = pg.InfiniteLine(pos=x_peak, pen=pg.mkPen(color="y", width=1))
            self.vlines_cal.append(vline)
            self.plot_widget_calibrate.addItem(vline)

        if len(x_positions) == 2:
            self.allow_calibration_steps(True)
        else:
            self.allow_calibration_steps(False)

    # not a very good solution, but it works
    @Slot()
    def cal_mouse_domain(self, event):
        """Function for displaying the domain lines in the plot at mouse postition."""
        if self.cal_data_loaded:
            pos_click = self.plot_widget_calibrate.plotItem.vb.mapSceneToView(event)
            try:
                self.plot_widget_calibrate.removeItem(self.v_line_mouse_left)
                self.plot_widget_calibrate.removeItem(self.v_line_mouse_right)
            except:
                pass
            self.v_line_mouse_left.setPos(
                pos_click.x() - (self.domain_width_spin_cal.value() / 2)
            )
            self.v_line_mouse_right.setPos(
                pos_click.x() + (self.domain_width_spin_cal.value() / 2)
            )
            self.plot_widget_calibrate.addItem(self.v_line_mouse_left)
            self.plot_widget_calibrate.addItem(self.v_line_mouse_right)

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
                peaks = self.process_data_analyze.find_gamma_peaks(
                    prominence=self.peak_thresh_spin.value()
                )
                self.fit_peaks_x = self.process_data_analyze.fit_peaks(
                    peaks=peaks,
                    domain_width=self.domain_width_spin.value(),
                )
            except RuntimeError:
                self.analysis_log.append(
                    "No peaks detected. Try lowering the peak detection threshold or adjusting the domain width.\n"
                )
            else:
                self.vlines = []
                for peak_nr, x_peak in enumerate(self.fit_peaks_x.iloc[:, 0]):
                    vline = pg.InfiniteLine(
                        pos=x_peak,
                        label=f"{peak_nr + 1}",
                        pen=pg.mkPen(color="y", width=1),
                    )
                    self.vlines.append(vline)
                    self.plot_widget_analyze.addItem(vline)

                peak_count = len(self.fit_peaks_x)
                self.fit_peaks_x.insert(0, "peak", range(1, peak_count + 1))

                self.analysis_log.append(
                    f"FITTED {peak_count} PEAKS:\n{self.fit_peaks_x.to_markdown(index=False, tablefmt='plain', headers=['Peak', 'Energy [keV]', 'Std Err [keV]'])}\n"
                )

    @Slot()
    def find_isotopes(self):
        try:
            mf = MatchFeatures(
                data_peaks=self.fit_peaks_x, catalog_data=self.isotope_catalog
            )
        except AttributeError:
            self.analysis_log.append("No peaks fitted. Try fitting the peaks first.\n")
        else:
            matches = mf.match_isotopes()
            result_length = self.result_length_spin.value()
            peak_count = len(self.fit_peaks_x)
            self.analysis_log.append(f"Using {self.catalog_name} as isotope catalog.")
            self.analysis_log.append(f"MATCHED {peak_count} PEAKS:")
            for index in range(peak_count):
                peak_nr = index + 1

                # gets the first result_length rows of the matches dataframe where the peak numbers match
                peak_matches = matches[matches.iloc[:, 0] == peak_nr].iloc[
                    :result_length, 1:4
                ]
                if len(peak_matches) > 0:
                    self.analysis_log.append(
                        f"--- Peak {peak_nr} matches with: ---\n{peak_matches.to_markdown(index=False, tablefmt='plain', headers=['Isotope', 'Certainty [%]', 'Energy [keV]'])}"
                    )
                else:
                    self.analysis_log.append(f"--- Peak {peak_nr} has no matches. ---")
            self.analysis_log.append("")

    @Slot()
    def calc_cal_factors(self):
        """Function for calculating the conversion factors for the calibration."""
        (
            self.scaling_factor,
            self.horizontal_offset,
        ) = self.process_data_calibrate.calibrate(
            known_energies=[self.energy_spin_1.value(), self.energy_spin_2.value()],
            found_energies=[
                self.fitted_calibration_peaks.iloc[:, 0].values[0],
                self.fitted_calibration_peaks.iloc[:, 0].values[1],
            ],
        )
        self.calibration_log.append(
            f"CALIBRATION RESULTS:\nConversion factor: {self.scaling_factor:.2f} keV/mV\nEnergy offset: {self.horizontal_offset:.2f} keV\n"
        )

    @Slot()
    def apply_calibration(self):
        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
            filter="CSV files (*.csv)"
        )
        if file_paths:
            for file_path in file_paths:
                file_path = Path(file_path)
                opened_file = pd.read_csv(file_path)
                calibrated_data = self.process_data_calibrate.apply_calibration(
                    data=opened_file,
                    scaling_factor=self.scaling_factor,
                    horizontal_offset=self.horizontal_offset,
                )

                filename_extended = file_path.stem + "_calibrated" + file_path.suffix
                new_filename = file_path.parent / filename_extended
                calibrated_data.to_csv(new_filename, index=False)
                self.calibration_log.append(f"Saved {filename_extended}.\n")


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
