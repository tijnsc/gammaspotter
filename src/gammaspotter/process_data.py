import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from lmfit import models
from gammaspotter.fit_models import FitModels


class ProcessData:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def calibrate(self):
        pass

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
        """Creates subset dataframes from the input data which contain a domain of given width around specified center values, useful for isolating peaks in spectra.

        Args:
            centers (list[float]): x-values around which the domains should be generated.
            width (float, optional): Width of the generated DataFrames. Defaults to 10.

        Returns:
            list[pd.DataFrame]: list containing generated DataFrames.
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
            data (pd.DataFrame): input data, has to be provided seperately from the main dataset
            amp (float): expected amplitude of the distribution
            cen (float): expected center of the distribution
            wid (float): expected width of the distribution
            startheight (float): expected start height of the distribution

        Returns:
            ModelResult: result of the performed fit
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


if __name__ == "__main__":
    pass
