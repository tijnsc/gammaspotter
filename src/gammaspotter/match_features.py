from math import sqrt
from scipy.special import erfc
import pandas as pd


class MatchFeatures:
    def __init__(self, data_peaks: pd.DataFrame, catalog_data: pd.DataFrame):
        """Class for matching the found gamma peaks with the literature energies.

        Args:
            data_peaks (pd.DataFrame): DataFrame containing the found gamma peaks.
            catalog_data (pd.DataFrame): DataFrame containing the literature energies.
        """
        self.data_peaks = data_peaks
        self.catalog_isotopes = catalog_data.iloc[:, [0, 1]].values.tolist()

    def match_isotopes(self) -> pd.DataFrame:
        """Function for matching the found gamma peaks with the literature energies.

        Returns:
            pd.DataFrame: A sorted DataFrame of possible sources.
        """
        output_list = []
        peak_nr = 1

        # looping every known source by every peak for finding all the sigmas
        for found_isotope in self.data_peaks.itertuples(index=False):
            for catalog_isotope in self.catalog_isotopes:
                literature_energy = catalog_isotope[0]
                literature_isotope = catalog_isotope[1]
                measured_energy = found_isotope[1]
                std_meas = found_isotope[2]

                z_score = (measured_energy - literature_energy) / std_meas
                percentage_match = self.sigma_changer(abs(z_score))

                if percentage_match > 0:
                    output_list.append(
                        [
                            peak_nr,
                            literature_isotope,
                            percentage_match,
                            literature_energy,
                        ]
                    )
            peak_nr += 1

        output_df = pd.DataFrame(
            output_list, columns=["Peak Number", "Isotope", "Percentage", "Energy"]
        )
        sorted_df = output_df.sort_values(
            by=["Peak Number", "Percentage"], ascending=[True, False]
        )

        return sorted_df

    def sigma_changer(self, z_score):
        """Function fo changing the sigma in to a percentage.

        Args:
            z_score (float): The z_score of the measured data compared to the literature value.

        Returns:
            float: Percentage of the given sigma.
        """
        return round(erfc(z_score / sqrt(2)) * 100, 2)
