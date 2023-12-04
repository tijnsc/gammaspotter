import pandas as pd
from scipy.signal import find_peaks
from lmfit import models
from gammaspotter.fit_models import FitModels
from statistics import mean


class ProcessData:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def remove_edge_effect(self) -> pd.DataFrame:
        """Remove the last four rows of a dataframe to remove an edge effect from out of range binning.

        Returns:
            pd.DataFrame: Data without last four columns.
        """
        return self.data[:-4]

    def find_gamma_peaks(self, width, prominence) -> pd.DataFrame:
        """Detect peaks in the gamma spectrum and return their positions in the graph.

        Returns:
            pd.DataFrame: The x and y coordinates of the detected peaks.
        """
        y = self.data.iloc[:, 1]
        peaks, _ = find_peaks(y, width=width, prominence=prominence)
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

    def isolate_domains(
        self, centers: list[float], width: float = 10
    ) -> list[pd.DataFrame]:
        """Creates subset dataframes from the input data which contain a domain of given width around specified center values,
           useful for isolating peaks in spectra.

        Args:
            centers (list[float]): x-values around which the domains should be generated.
            width (float, optional): Width of the generated DataFrames iwth a defaults of 10.

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

    def fit_gauss(
        self, data: pd.DataFrame, amp: float, cen: float, wid: float, startheight: float
    ):
        """Takes data and fits a gaussian distribution over it.

        Args:
            data (pd.DataFrame): Input data, has to be provided seperately from the main dataset.
            amp (float): Expected amplitude of the distribution.
            cen (float): Expected center of the distribution.
            wid (float): Expected width of the distribution.
            startheight (float): Expected startheight of the distribution.

        Returns:
            ModelResult: Result of the performed fit.
        """
        gmodel = FitModels.gaussian
        lmfit_model = models.Model(gmodel)
        x = data.iloc[:, 0]
        y = data.iloc[:, 1]
        result = lmfit_model.fit(
            y, x=x, amp=amp, cen=cen, wid=wid, startheight=startheight
        )
        return result

    def fit_peaks(self) -> list:
        """Takes the rough data and uses the peak finder function and the domain function.
           Than fits a gaussian function for better accuracy and returns this.

        Returns:
            list: A list of accurate data.
        """
        peaks = self.find_gamma_peaks([3, 6], 200)
        peaks_x = peaks.iloc[:, 0]
        peaks_y = peaks.iloc[:, 1]
        domains = self.isolate_domains(centers=peaks_x)

        fit_results = []
        for index, domain in enumerate(domains):
            result = self.fit_gauss(
                data=domain,
                amp=peaks_y.values[index],
                cen=peaks_x.values[index],
                wid=10,
                startheight=10,
            )

            fit_results.append(result)

        return fit_results

    def calibrate(self, known_energies: list[float]) -> tuple[float]:
        detected_peak_fit = []
        results = self.fit_peaks()
        for result in results:
            detected_peak_fit.append(result.values["cen"])

        if len(detected_peak_fit) != len(known_energies):
            raise Exception(
                "Detected and reference peak mismatch. Please try another measurement or use another isotope."
            )

        detected_peak_fit = sorted(detected_peak_fit)
        known_energies = sorted(known_energies)

        diff_meas = detected_peak_fit[-1] - detected_peak_fit[0]
        diff_ref = known_energies[-1] - known_energies[0]

        scaling_factor = diff_ref / diff_meas
        horizontal_offsets = []
        for peak_nr in range(len(detected_peak_fit)):
            horizontal_offsets.append(
                detected_peak_fit[peak_nr] * scaling_factor - known_energies[peak_nr]
            )

        horizontal_offset = mean(horizontal_offsets)
        return scaling_factor, horizontal_offset
