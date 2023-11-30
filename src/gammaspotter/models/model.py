import pandas as pd
from scipy.signal import find_peaks


class CalibrateData:
    def __init__(self) -> None:
        pass


class AnalyzeData:
    def __init__(self) -> None:
        pass

    def find_gamma_peaks(df: pd.DataFrame) -> pd.DataFrame:
        y = df["counts_ch_A"]
        peaks, _ = find_peaks(y, prominence=90)
        peak_positions = df.index[peaks]

        x_peaks = df["pulseheight"][peak_positions]
        y_peaks = df["counts_ch_A"][peak_positions]

        peaks_df = pd.DataFrame(
            {
                "x_peaks": x_peaks,
                "y_peaks": y_peaks,
            }
        )

        return peaks_df


if __name__ == "__main__":
    print(AnalyzeData.find_gamma_peaks(pd.read_csv("data/Na-22 2400s HPG.csv")))
