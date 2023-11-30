import pandas as pd
from scipy.signal import find_peaks
import numpy as np
from lmfit import models
from gammaspotter.fit_models import FitModels


class CalibrateData:
    def __init__(self) -> None:
        pass

    def calibrate(self):
        pass


class AnalyzeData:
    def __init__(self) -> None:
        pass

    def find_gamma_peaks(self, data: pd.DataFrame, width, prominence) -> pd.DataFrame:
        """Detect peaks in the gamma spectrum and return their positions in the graph.

        Args:
            data (pd.DataFrame): a DataFrame containing the spectrum data that should be analyzed

        Returns:
            pd.DataFrame: the x and y coordinates of the detected peaks
        """
        y = data.iloc[:, 1]
        peaks, _ = find_peaks(y, width=width, prominence=prominence)
        peak_positions = data.index[peaks]

        x_peaks = data.iloc[:, 0][peak_positions]
        y_peaks = data.iloc[:, 1][peak_positions]

        peaks_data = pd.DataFrame(
            {
                "x_peaks": x_peaks,
                "y_peaks": y_peaks,
            }
        )

        return peaks_data

    def isolate_peaks(
        self, data: pd.DataFrame, width: float = 10
    ) -> list[pd.DataFrame]:
        peak_positions = self.find_gamma_peaks(data=data, width=[3, 7], prominence=300)

        domains = []
        for _, row in peak_positions.iterrows():
            x = row["x_peaks"]
            upper_bound = x + width / 2
            lower_bound = x - width / 2
            domain = data[
                (data.iloc[:, 0] >= lower_bound) & (data.iloc[:, 0] <= upper_bound)
            ]
            domains.append(domain)

        return domains

    def fit_data(self, model, x, y, *args, **kwargs):
        lmfit_model = models.Model(model)
        result = lmfit_model.fit(y, x=x, args=args, kwargs=kwargs)
        print(result.fit_report())
        return result


if __name__ == "__main__":
    data = pd.read_csv("data/Na-22 2400s HPG.csv")
    domains = AnalyzeData().isolate_peaks(data=data)

    model = FitModels.gaussian
    AnalyzeData().fit_data(model, data["pulseheight"], data["counts_ch_A"], 30, 1, 1, 0)
