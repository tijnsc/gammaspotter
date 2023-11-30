import pandas as pd
from scipy.signal import find_peaks
from lmfit import models
from gammaspotter.fit_models import FitModels


class CalibrateData:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def calibrate(self):
        pass


class CleanData:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def remove_edge_effect(self) -> pd.DataFrame:
        """Remove the last few rows of a dataframe to remove an edge effect from out of range binning.

        Returns:
            pd.DataFrame: data without last four columns
        """
        return self.data[:-4]


class AnalyzeData:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

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

    def isolate_peaks(self, width: float = 10) -> list[pd.DataFrame]:
        """Creates subset dataframes from the input data which contain a domain of set width around peaks in the spectrum.

        Args:
            width (float, optional): width of the generated DataFrames. Defaults to 10.

        Returns:
            list[pd.DataFrame]: list containing generated DataFrames
        """
        peak_positions = self.find_gamma_peaks(width=[3, 7], prominence=300)

        domains = []
        for _, row in peak_positions.iterrows():
            x = row["x_peaks"]
            upper_bound = x + width / 2
            lower_bound = x - width / 2
            domain = self.data[
                (self.data.iloc[:, 0] >= lower_bound)
                & (self.data.iloc[:, 0] <= upper_bound)
            ]
            domains.append(domain)

        return domains

    def fit_data(self, model, x, y, **kwargs):
        lmfit_model = models.Model(model)
        result = lmfit_model.fit(y, x=x, kwargs=kwargs)
        print(result.fit_report())
        return result


if __name__ == "__main__":
    data = pd.read_csv("data/Cs-137 1200s 100mV.csv")
    domains = AnalyzeData().isolate_peaks(data=data)

    model = FitModels.gaussian
    AnalyzeData().fit_data(
        model,
        x=data["pulseheight"],
        y=data["counts_ch_A"],
        amp=10,
        cen=12,
        wid=12,
        startheight=12,
    )
