import click
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

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
def graph(path: Path, detect_peaks: bool, no_cleaning: bool, fit_peaks: bool):
    """Display a measurement in CSV format as an interactive MPL plot.

    Args:
        path (Path): location of the data file that should be displayed
        no_cleaning (bool): disable removal of edge effect
        detect_peaks (bool): indicate whether the peaks should be detected and displayed in the figure
        fit_peaks (bool): fit a gaussian function over the peaks to determine their positions more accurately
    """
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
        fit_results = data_process.fit_peaks()
        for result in fit_results:
            plt.axvline(x=result.values["cen"], c="grey", linestyle="dotted")

    plt.show()


if __name__ == "__main__":
    cmd_group()
