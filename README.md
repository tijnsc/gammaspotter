# gammaspotter
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://tijnsc.github.io/gammaspotter/)
[![pypi version](https://img.shields.io/pypi/v/gammaspotter.svg)](https://pypi.org/project/gammaspotter/)

The [gammaspotter](https://github.com/tijnsc/gammaspotter/) application is designed to identify radioactive sources in gamma spectra.

---

**[Features](#features)** - **[Installation](#installation)**

![gammaspotter_window](https://raw.githubusercontent.com/tijnsc/gammaspotter/main/.github/images/gammaspotter_window.png)

## Features

- **Measurement Calibration** The calibrate tab lets the user calibrate a gamma spectrum by comparing known energies to peak energies.

- **Data Visualization:** The analyze tab offers an interactive visualization to help you gain insights into your data.

- **Statistical Analysis:** You can perform statistical analysis on your calibrated data using built-in functions and algorithms. This includes peak detection, peak fitting and isotope match detection.

- **Report Generation:** Once you have completed your analysis, the analyze tab enables you to generate reports summarizing your findings. You can access visualizations and statistical results.

## Installation

To install the "gammaspotter" package, you can use [Poetry](https://python-poetry.org/), a dependency management and packaging tool for Python.

1. First, make sure you have Poetry installed on your system. If not, you can install it by following the [official Poetry installation guide](https://python-poetry.org/docs/#installation).

2. Clone the repository from GitHub:

    ```bash
    git clone https://github.com/tijnsc/gammaspotter.git
    ```

    When the repository has been downloaded, navigate into it:

    ```bash 
    cd gammaspotter
    ```

3. Install the package:

    ```bash
    poetry install
    ```

4. Finally, you can start using the package by running `gammaspotter`.