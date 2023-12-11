# Calibration

### Opening a measurement
To initiate the calibration process, start by opening a measurement file. Ideally, use an a Na-22 dataset due to its distinct peaks. Click the 'Open Measurement' button and select the desired file in .csv format. This initial step is crucial otherwise the program wont work.

### Preparing the calibration
After importing the data the peaks need to be defined by a fit with the right width. The 'Domain width' scrollbox, located on the right side, allows you to adjust the width. A standard setting of 5 is suitable for precise data. However, for less accurate data, consider widening the domain to ensure the cursor surrounds the entire peak. 

Next, use your cursor to click on the peaks in the plot. Additionally, input the energy levels from literature in keV. For Na-22, simplify this step by clicking 'Preset Energies' to automatically set the literature energy levels for the two significant peaks. If using a different source, manually input the energy levels into the 'Energy 1' and 'Energy 2' scrollboxes.

### Conversion factor
With all parameters set, click the 'Calculate Conversion Factor' button. The program will automatically compute the conversion factor and energy offset, displaying the results in the 'Calibration Log'.

### Saving the file
Upon completion of the calibration process, save the calibrated data by clicking 'Apply Calibration To Files'. This action allows you to calibrate any set of data to the correct values. Choose the file you want to analyze for isotopes, and the calibrated file will be generated alongside it. This step ensures that your data is accurately calibrated and ready for further analysis.

