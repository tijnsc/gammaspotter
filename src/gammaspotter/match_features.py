import numpy as np
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
        catalog_energy_list = catalog_data.iloc[:, [1, 0]].values.tolist()
        self.catalog_energy_list = catalog_energy_list

    def matcher(self):
        """Function for matching the found gamma peaks with the literature energies.

        Returns:
            list: A sorted list of possible sources.
        """
        output_list = []
        sorted_list = []
        peak_nr = 1

        # looping every known source by every peak for finding all the sigmas
        for found_energy_sigma in self.data_peaks:
            for energy in self.catalog_energy_list:
                sigma_source = (
                    abs(energy[1] - found_energy_sigma[0]) / found_energy_sigma[1]
                )
                output_list.append(
                    [peak_nr, energy[0], self.sigma_changer(sigma_source)]
                )
            peak_nr += 1

        start = 0
        count = 0
        number = 1

        # loop for sorting the list by every peak
        for peak in output_list:
            if not peak[0] == number:
                sorted_cut_list = sorted(
                    output_list[start:count], reverse=True, key=lambda x: x[2]
                )
                sorted_list = sorted_list + sorted_cut_list
                start = count
                number += 1
            count += 1
        sorted_cut_list = sorted(
            output_list[start:count], reverse=True, key=lambda x: x[2]
        )
        sorted_list = sorted_list + sorted_cut_list

        return sorted_list

    def sigma_changer(self, sigma_source):
        """Function fo changing the sigma in to a percentage.

        Args:
            sigma_source (float): The error of the fit function.

        Returns:
            float: Percentage of the given sigma.
        """
        percentage = erfc(sigma_source / np.sqrt(2)) * 100
        return percentage


if __name__ == "__main__":
    list_1 = [[1475.5, 15], [511, 5], [200, 20]]
    cat = [
        ["Na-22", 1274.5],
        ["Cs-137", 661.64],
        ["Ba-133", 356],
        ["Co-60", 1173.2],
        ["Co-60", 1332.5],
        ["K-40", 1460],
    ]
    print(MatchFeatures(list_1).matcher())

    # MatchFeatures(list_1)
