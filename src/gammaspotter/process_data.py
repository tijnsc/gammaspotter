import pandas as pd
from scipy.signal import find_peaks
from lmfit import models
from gammaspotter.fit_models import FitModels

import matplotlib.pyplot as plt


class ProcessData:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def calibrate(self):
        pass

    def remove_edge_effect(self) -> pd.DataFrame:
        """Remove the last few rows of a dataframe to remove an edge effect from out of range binning.

        Returns:
            pd.DataFrame: data without last four columns
        """
        return self.data[:-4]

    def find_gamma_peaks(self, width, prominence) -> pd.DataFrame:
        """Detect peaks in the gamma spectrum and return their positions in the graph.

        Returns:
            pd.DataFrame: the x and y coordinates of the detected peaks
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
            centers (list[float]): x-values around which the domains should be generated
            width (float, optional): width of the generated DataFrames. Defaults to 10.

        Returns:
            list[pd.DataFrame]: list containing generated DataFrames
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

    def fit_gauss(self, amp, cen, wid, startheight):
        gmodel = FitModels.gaussian
        lmfit_model = models.Model(gmodel)
        x = self.data.iloc[:, 0]
        y = self.data.iloc[:, 1]
        result = lmfit_model.fit(
            y, x=x, amp=amp, cen=cen, wid=wid, startheight=startheight
        )
        return result


if __name__ == "__main__":
    data = pd.read_csv("data/Na-22 2400s HPG.csv")
    data_processing = ProcessData(data=data)

    # result = data_processing.fit_gauss(amp=10, cen=10, wid=10, startheight=10)
    # result.params.pretty_print()

    centers = data_processing.find_gamma_peaks([3, 6], 200)
    centers_x = centers.iloc[:, 0]
    centers_y = centers.iloc[:, 1]
    domains = data_processing.isolate_domains(centers=centers_x)

    for index, domain in enumerate(domains):
        data_processing.fit_gauss(
            amp=centers_y.values[index],
            cen=centers_x.values[index],
            wid=10,
            startheight=10,
        )

    plt.show()
