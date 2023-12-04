import click
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from rich.table import Table
from rich.console import Console
from datetime import datetime

from gammaspotter.process_data import ProcessData


@click.group()
def cmd_group():
    """A CLI tool for gammaspotter."""
    pass


@cmd_group.command()
@click.option(
    "--no-cleaning",
    help="Disable the default removal of last few rows of data usually containing edge effect abnormalities.",
    is_flag=True,
)
@click.option(
    "--detect-peaks",
    help="Display the positions of the detected peaks in the spectrum.",
    is_flag=True,
)
@click.option(
    "--fit-peaks",
    help="Determine the positions of the peaks accurately by fitting a gaussian function to it.",
    is_flag=True,
)
@click.argument(
    "path", type=click.Path("rb", dir_okay=False, executable=False, path_type=Path)
)
@click.option(
    "-c",
    "--calibrate",
    type=click.Path(
        exists=True,
        dir_okay=False,
        file_okay=True,
        help="File containing calibration results which will be applied to the graph.",
    ),
)
def graph(
    path: click.Path,
    detect_peaks: bool,
    no_cleaning: bool,
    fit_peaks: bool,
    calibrate: bool,
):
    """Display a measurement in CSV format as an interactive MPL plot.

    Args:
        path (Path): location of the data file that should be displayed
        no_cleaning (bool): disable removal of edge effect
        detect_peaks (bool): indicate whether the peaks should be detected and displayed in the figure
        fit_peaks (bool): fit a gaussian function over the peaks to determine their positions more accurately
        calibrate (bool): indicate a path where calibration results are stored
    """
    path = Path(path)
    data = pd.read_csv(path)
    data_process = ProcessData(data=data)

    if not no_cleaning:
        data = data_process.remove_edge_effect()

    fig, ax = plt.subplots()

    if detect_peaks:
        peaks_df = data_process.find_gamma_peaks(width=[3, 7], prominence=300)

        if peaks_df.size > 0:
            peaks_df.plot(
                ax=ax,
                x="x_peaks",
                y="y_peaks",
                label="Detected peaks",
                kind="scatter",
                c="red",
                s=50,
                marker="x",
                zorder=1,
            )
        else:
            click.echo(
                "No peaks have been detected, please adjust your detection parameters if you think this is incorrect."
            )

    data.plot(
        ax=ax,
        x="pulseheight",
        y="counts_ch_A",
        label="Spectrum",
        legend=True,
        xlabel="Pulseheight",
        ylabel="Counts",
        title=path.stem,
        zorder=0,
    )

    if fit_peaks:
        energies = []
        fit_results = data_process.fit_peaks()
        for result in fit_results:
            x_expectation_val = result.values["cen"]
            plt.axvline(x=x_expectation_val, c="grey", linestyle="dotted")
            energies.append(x_expectation_val)

        print(f"{energies=}")

    plt.show()


@cmd_group.command()
@click.argument("path", type=click.Path())
@click.argument("isotope", type=click.Choice(["Na-22"]))
@click.option(
    "-s",
    "--save",
    type=click.Path(dir_okay=True, file_okay=False),
    help="Provide a directory where the calibration data should be saved.",
)
def calibrate(path: click.Path, isotope: str, save: click.Path):
    calibration_catalog = {"Na-22": [511, 1274.537]}

    data = pd.read_csv(path)
    data_process = ProcessData(data=data)

    known_energies = calibration_catalog[isotope]

    calibration_params = data_process.calibrate(known_energies=known_energies)

    table = Table(title=f"{isotope} Calibration Results")
    table.add_column("Scaling Factor")
    table.add_column("Energy Offset")
    scaling_str = f"{round(calibration_params[0], 4)} keV/mV"
    hoffset_str = f"{round(calibration_params[1], 4)} keV"
    table.add_row(scaling_str, hoffset_str)
    console = Console()
    console.print(table)

    if save:
        calibration_Series = pd.Series(
            {
                "unix timestamp": datetime.now(),
                "isotope": isotope,
                "scaling factor": calibration_params[0],
                "horizontal offset": calibration_params[1],
            }
        )

        save = Path(save)
        path = save / f"{isotope}_calibration.json"
        calibration_Series.to_json(path)


if __name__ == "__main__":
    cmd_group()
