import numpy as np
from scipy.special import erfc


def matcher(found_energy_sigma_list, energy_list):
    output_list = []
    sorted_list = []
    peak_nr = 1

    for found_energy_sigma in found_energy_sigma_list:
        found_energy = found_energy_sigma[0]
        sigma = found_energy_sigma[1]
        for energy in energy_list:
            sigma_source = abs(energy[1] - found_energy) / sigma
            percentage = sigma_changer(sigma_source)
            output_list.append([peak_nr, energy[0], percentage])
        peak_nr += 1

    start = 0
    count = 0
    number = 1
    
    for peak in output_list:
        if peak[0] == number:
            pass
        else:
            sorted_cut_list = sorted(output_list[start:count], reverse=True, key=lambda x: x[2])
            sorted_list = sorted_list + sorted_cut_list
            start = count
            number += 1
        count += 1
    sorted_cut_list = sorted(output_list[start:count], reverse=True, key=lambda x: x[2])
    sorted_list = sorted_list + sorted_cut_list
    
    return sorted_list


def sigma_changer(sigma_source):
    x = sigma_source
    percentage = erfc(x / np.sqrt(2)) *  100
    return percentage


if __name__ == "__main__":
    list_1 = [[1475.5, 15], [511, 5], [200, 20]]
    list_2 = [["Na-22", 1480], ["Cs-137", 510]]
    print(matcher(list_1, list_2))

