import pandas as pd
import numpy as np

from statistics import mean
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

from gammaspotter.fit_models import FitModels


class ProcessData:
    def __init__(self, data: pd.DataFrame) -> None:
        # remove last four rows of data to remove edge effect from out of range binning
        self.data = data[:-4]

    def find_gamma_peaks(self, prominence) -> pd.DataFrame:
        """Detect peaks in the gamma spectrum and return their positions in the graph.

        Returns:
            pd.DataFrame: The x and y coordinates of the detected peaks.
        """
        y = self.data.iloc[:, 1]
        peaks, _ = find_peaks(y, prominence=prominence)
        peak_positions = self.data.index[peaks]

        x_peaks = self.data.iloc[:, 0][peak_positions]
        y_peaks = self.data.iloc[:, 1][peak_positions]

        peaks_data = pd.DataFrame(
            {
                "x_peaks": x_peaks,
                "y_peaks": y_peaks,
            }
        )

        return peaks_data

    def isolate_domains(self, centers: list[float], width: float) -> list[pd.DataFrame]:
        """Creates subset dataframes from the input data which contain a domain of given width around specified center values,
           useful for isolating peaks in spectra.

        Args:
            centers (list[float]): x-values around which the domains should be generated.
            width (float, optional): Width of the generated DataFrames.

        Returns:
            list[pd.DataFrame]: List containing generated DataFrames.
        """
        domains = []
        for x in centers:
            upper_bound = x + width / 2
            lower_bound = x - width / 2
            domain = self.data[
                (self.data.iloc[:, 0] >= lower_bound)
                & (self.data.iloc[:, 0] <= upper_bound)
            ]
            domains.append(domain)

        return domains

    def fit_peaks(self, peaks: pd.DataFrame, domain_width: float) -> pd.DataFrame:
        """Takes raw spectrum data and performs a gaussian model fit on domains of the roughly detected peaks.
        This function returns more accurate peak positions than 'find_gamma_peaks'.

        Args:
            peaks (pd.DataFrame): x and y values of peaks
            domain_width (float): width of the domains generated for analysis
        Returns:
            pd.DataFrame: x-values of fitted peaks with uncertainties
        """
        peaks_x = peaks.iloc[:, 0]
        peaks_y = peaks.iloc[:, 1]

        domains = self.isolate_domains(centers=peaks_x, width=domain_width)

        x_positions = []
        x_positions_std = []
        for index, domain in enumerate(domains):
            x = domain.iloc[:, 0]
            y = domain.iloc[:, 1]

            # [amp, cen, wid, startheight]
            initial_guess = [
                peaks_y.values[index],
                peaks_x.values[index],
                domain_width,
                domain.iloc[:, 1].min(),
            ]

            # only positive parameters are allowed
            bounds = ([0, 0, 0, 0], np.inf)

            fit_func = FitModels.gaussian
            popt, pcov = curve_fit(fit_func, x, y, p0=initial_guess, bounds=bounds)

            # extract fitted parameters
            amp, cen, wid, startheight = popt
            fit_errors = np.sqrt(np.diag(pcov))

            # get the energy and standard error
            energy_of_peak = cen
            standard_error = fit_errors[1]

            x_positions.append(energy_of_peak)
            x_positions_std.append(standard_error)

        x_positions_df = pd.DataFrame(
            {
                "energy": x_positions,
                "stderr": x_positions_std,
            }
        )

        return x_positions_df

    # def calibrate(self, known_energies: list[float]) -> tuple[float]:
    #     """Function for making the calibration so the plot is given in keV and not in mV or any other unit.

    #     Args:
    #         known_energies (list[float]): list of energies that correspond with a known source

    #     Raises:
    #         Exception: when there occures an error it tells you to use a different measurement

    #     Returns:
    #         scaling_factor[float]: how much the two peaks need to be scaled for them to have the right distance between them
    #         horizontal_offset[float]: how far the two peaks need to be moved so they line up with the known energies in keV
    #     """
    #     detected_peak_fit = []
    #     results = self.fit_peaks(width=10)
    #     for result in results:
    #         detected_peak_fit.append(result.values["cen"])

    #     if len(detected_peak_fit) != len(known_energies):
    #         raise Exception(
    #             "Detected and reference peak mismatch. Please try another measurement or use another isotope."
    #         )

    #     detected_peak_fit = sorted(detected_peak_fit)
    #     known_energies = sorted(known_energies)

    #     diff_meas = detected_peak_fit[-1] - detected_peak_fit[0]
    #     diff_ref = known_energies[-1] - known_energies[0]

    #     scaling_factor = diff_ref / diff_meas
    #     horizontal_offsets = []
    #     for peak_nr in range(len(detected_peak_fit)):
    #         horizontal_offsets.append(
    #             detected_peak_fit[peak_nr] * scaling_factor - known_energies[peak_nr]
    #         )

    #     horizontal_offset = mean(horizontal_offsets)
    #     return scaling_factor, horizontal_offset
