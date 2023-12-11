# gammaspotter

Package for finding and identifying radioactive sources. The goal is to make it easier to find radioactive sources from a gamma spectrum. With only a dataset of the a spectrum and a catalog of possible sources gammaspotter can identify possible sources in the provided spectrum.

---

**[Features](#features)** - **[Installation](#installation)** - **[Quick usage](#quick-usage)**

![gammaspotter_window](https://github.com/tijnsc/gammaspotter/blob/6efafd18579828d9297bbd78ad521452c05ba6d9/docs/img/gammaspotter_window.png)

## Features

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

4. Finally, you can start using the package by running it:

    ```bash
    gammaspotter
    ```

    That's it! You have successfully installed the `gammaspotter` package using Poetry.


## Quick usage

See the [usage](https://tijnsc.github.io/gammaspotter/usage) section of the docs for more examples!
