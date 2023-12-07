import numpy as np
from scipy.special import erfc


def matcher(found_energy_sigma_list, energy_list):
    output_list = []
    sorted_list = []
    peak_nr = 1
    number = 1
    count = 0
    start = 0
    for found_energy_sigma in found_energy_sigma_list:
        found_energy = found_energy_sigma[0]
        sigma = found_energy_sigma[1]
        for energy in energy_list:
            source_name = energy[0]
            energy_value = energy[1]
            sigma_source = abs(energy_value - found_energy) / sigma
            percentage = sigma_changer(sigma_source)
            output_list.append([peak_nr, source_name, percentage])
        peak_nr += 1

    
    for peak in output_list:
        if peak[0] == number:
            count += 1
        else:
            cut_list = output_list[start:count]
            start = count
            sorted_cut_list = sorted(cut_list, reverse=True, key=lambda x: x[2])
            sorted_list = sorted_list + sorted_cut_list
            number += 1
            count += 1
    cut_list = output_list[start:count]
    sorted_cut_list = sorted(cut_list, reverse=True, key=lambda x: x[2])
    sorted_list = sorted_list + sorted_cut_list
    
        
        


    
    
    return sorted_list


def sigma_changer(sigma_source):
    x = sigma_source
    percentage = erfc(x / np.sqrt(2)) *  100
    return percentage


if __name__ == "__main__":
    list_1 = [[1475.5, 15], [511, 5], [410, 20]]
    list_2 = [["Na-22", 1480], ["Cs-137", 510]]
    print(matcher(list_1, list_2))

