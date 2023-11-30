import pandas as pd
from scipy.signal import find_peaks


class CalibrateData:
    def __init__(self) -> None:
        pass

    def calibrate(self):
        pass


class AnalyzeData:
    def __init__(self) -> None:
        pass

    def find_gamma_peaks(df: pd.DataFrame) -> pd.DataFrame:
        """Detect peaks in the gamma spectrum and return their positions in the graph.

        Args:
            df (pd.DataFrame): the DataFrame containing the spectrum data that should be analyzed

        Returns:
            pd.DataFrame: the x and y coordinates of the detected peaks
        """
        y = df.iloc[:, 1]
        peaks, _ = find_peaks(y, width=[3, 7], prominence=300)
        peak_positions = df.index[peaks]

        x_peaks = df.iloc[:, 0][peak_positions]
        y_peaks = df.iloc[:, 1][peak_positions]

        peaks_df = pd.DataFrame(
            {
                "x_peaks": x_peaks,
                "y_peaks": y_peaks,
            }
        )

        return peaks_df


if __name__ == "__main__":
    print(AnalyzeData.find_gamma_peaks(pd.read_csv("data/Na-22 2400s HPG.csv")))
