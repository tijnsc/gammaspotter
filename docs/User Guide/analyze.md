# Analysis

### Key Features

1. Data Visualization: The analyze tab offers an interactive visualization to help you gain insights into your data.

2. Statistical Analysis: You can perform statistical analysis on your calibrated data using built-in functions and algorithms. This includes [`peak detection`][gammaspotter.process_data.ProcessData.find_gamma_peaks], [`peak fitting`][gammaspotter.process_data.ProcessData.fit_peaks] and [`isotope match detection`][gammaspotter.match_features.MatchFeatures.match_isotopes].

3. Report Generation: Once you have completed your analysis, the analyze tab enables you to generate reports summarizing your findings. You can access visualizations and statistical results.

### Selecting a Measurement
On the application interface, locate the [`Open Measurement`][gammaspotter.gui.UserInterface.open_file] button, typically situated on the right-hand side. This button serves as the entry point for choosing the measurement you wish to analyze. Click on this button to browse and select the specific measurement file you intend to use for analysis.

### Configuring Peak Detection Threshold
Directly below the `Open Measurement` button, you'll find a customizable box labeled `Peak Detection Threshold`. This parameter controls the sensitivity of the program when identifying peaks within the spectrum.

- **Increasing Threshold:** Increase the threshold value for a more strict peak detection. This results in fewer peaks being identified.
- **Decreasing Threshold:** Lowering the threshold will enhance sensitivity, identifying more peaks in the spectrum.

### Adjusting Fit Domain Width
Adjacent to the threshold setting, locate the `Fit Domain Width` box. This setting allows you to manipulate the width over which the program fits around the identified peaks.

- **Width Customization:** Increase or decrease the width to fine-tune the fitting range around identified peaks in the spectrum.
