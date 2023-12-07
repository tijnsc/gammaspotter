import numpy
     


def matcher(found_energy_sigma_list, energy_list):
    output_list = []
    peak_nr = 1
    for found_energy_sigma in found_energy_sigma_list:
        found_energy = found_energy_sigma[0]
        sigma = found_energy_sigma[1]
        for energy in energy_list:
            source_name = energy[0]
            energy_value = energy[1]
            sigma_source = abs(energy_value - found_energy) / sigma
            output_list.append([peak_nr ,source_name, sigma_source])
        peak_nr += 1
       
    

if __name__ == "__main__":
    list_1 = [[1475.5, 15], [511, 5]]
    list_2 = [["Na-22", 1480], ["Cs-137", 500]]
    matcher(list_1, list_2)

    
    

    
        
        










