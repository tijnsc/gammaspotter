# Analysis

### Selecting a Measurement
On the application interface, locate the `Open Measurement` button, typically situated on the right-hand side. This button serves as the entry point for choosing the measurement you wish to analyze. Click on this button to browse and select the specific measurement file you intend to use for analysis.

### Configuring Peak Detection Threshold
Directly below the `Open Measurement` button, you'll find a customizable box labeled `Peak Detection Threshold`. This parameter controls the sensitivity of the program when identifying peaks within the spectrum.

- **Increasing Threshold:** Increase the threshold value for a more strict peak detection. This results in fewer peaks being identified.
- **Decreasing Threshold:** Lowering the threshold will enhance sensitivity, identifying more peaks in the spectrum.

### Adjusting Fit Domain Width
Adjacent to the threshold setting, locate the `Fit Domain Width` box. This setting allows you to manipulate the width over which the program fits around the identified peaks.

- **Width Customization:** Increase or decrease the width to fine-tune the fitting range around identified peaks in the spectrum.

### Showing Plot
There are two checkboxes that can be selected. These will change the plot visible on the left side.

- **Show Detected Peaks:** This will display the peaks detected by the program on the plot.
- **Show Fitted Peaks:** Selecting this box will show the fitted peaks on the plot with a yellow line.

### Matching Isotopes
This button will search through the catalog and compare the values of the found energy with the literature value. The isotopes will be sorted by percentage and displayed on the right in the `Analysis Log`.

### Loading Catalog
If you want to use another catalog, locate the `Load alternative catalog` button. This will allow you to insert a .csv file as a catalog for finding the isotopes.

### Result Peaks
Changing the `Max. results per peak` scroll box will alter the number of matches shown. The isotopes are sorted by percentage, and if more matches are desired, this can be achieved by increasing the number.

### Analysis Log
The textbox on the right side under the buttons is a 'read-only' text box. All the information will be displayed here.