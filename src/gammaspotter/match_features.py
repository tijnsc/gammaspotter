from math import sqrt
from scipy.special import erfc
import pandas as pd


class MatchFeatures:
    def __init__(self, data_peaks: pd.DataFrame, catalog_path: str = None):
        self.data_peaks = data_peaks

        if catalog_path is None:
            # use built in catalog
            self.catalog = "catalogs/gamma-energies.csv"
        else:
            self.catalog = catalog_path

        catalog_data = pd.read_csv(self.catalog)
        catalog_isotopes = catalog_data.iloc[:, [0, 1]].values.tolist()
        self.catalog_isotopes = catalog_isotopes

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
        return round(erfc(z_score / 5 * sqrt(2)) * 100, 2)


if __name__ == "__main__":
    # list_1 = [[1475.5, 15], [511, 5], [200, 20]]
    # cat = [
    #     ["Na-22", 1274.5],
    #     ["Cs-137", 661.64],
    #     ["Ba-133", 356],
    #     ["Co-60", 1173.2],
    #     ["Co-60", 1332.5],
    #     ["K-40", 1460],
    # ]
    # print(MatchFeatures(list_1).match_isotopes())

    # MatchFeatures(list_1)
    pass
