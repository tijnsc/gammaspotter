# Analysis

### Selecting a Measurement
On the application interface, locate the [`Open Measurement`][gammaspotter.gui.UserInterface.open_file] button, typically situated on the right-hand side. This button serves as the entry point for choosing the measurement you wish to analyze. Click on this button to browse and select the specific measurement file you intend to use for analysis.

### Configuring Peak Detection Threshold
Directly below the `Open Measurement` button, you'll find a customizable box labeled `Peak Detection Threshold`. This parameter controls the sensitivity of the program when identifying peaks within the spectrum.

- **Increasing Threshold:** Increase the threshold value for a more strict peak detection. This results in fewer peaks being identified.
- **Decreasing Threshold:** Lowering the threshold will enhance sensitivity, identifying more peaks in the spectrum.

### Adjusting Fit Domain Width
Adjacent to the threshold setting, locate the `Fit Domain Width` box. This setting allows you to manipulate the width over which the program fits around the identified peaks.

- **Width Customization:** Increase or decrease the width to fine-tune the fitting range around identified peaks in the spectrum.

### Showing plot
There are two checkboxes that can be checkt. This will change the plot that can be seen on th eleft side.

- **Show detected peaks:** This will show the peaks that are detected by the program in the plot. 
- **Show fitted peaks:** Checking this box will show the fitted peaks in the plot with a yellow line.

### Matching isotopes
This button will search trough the catalog and compare the values of the found energy and the literature value. The isotopes will be sorted on percentage and shown on the right in the `Analysis Log`.

### Loading catalog
If you want to use another catalog, locate the `Load alternative catalog` button. This will give you the chance to insert a .csv file as a catalog for findeing the isotopes.

### Result peaks
Changing the `Max. results per peak` scrollbox will change the amount of matches are shown. The isotopes are sorted on percentage and when there are more matches wanted this can be done by increasing the number.

### Analysis Log
The textbox on the right side under the buttons is a 'read only' text box. All the information will be shown here.
