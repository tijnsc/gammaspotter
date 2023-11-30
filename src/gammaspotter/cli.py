import click
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from gammaspotter.process_data import CalibrateData, AnalyzeData


@click.group()
def cmd_group():
    """A CLI tool for gammaspotter."""
    pass


@cmd_group.command()
@click.option(
    "--peaks",
    help="Display the positions of the detected peaks in the spectrum.",
    is_flag=True,
)
@click.argument(
    "path", type=click.Path("rb", dir_okay=False, executable=False, path_type=Path)
)
def graph(path: Path, peaks: bool):
    """Display a measurement in CSV format as an interactive MPL plot.

    Args:
        path (str): location of the data file that should be displayed
    """

    data = pd.read_csv(path)

    ax = data.plot(
        "pulseheight",
        "counts_ch_A",
        legend=False,
        xlabel="Pulseheight",
        ylabel="Counts",
        title=path.stem,
        zorder=0,
    )

    if peaks:
        peaks_df = AnalyzeData.find_gamma_peaks(data=data, width=[3, 7], prominence=300)
        peaks_df.plot(
            ax=ax,
            x="x_peaks",
            y="y_peaks",
            kind="scatter",
            c="red",
            s=50,
            marker="x",
            zorder=1,
        )

    plt.show()


if __name__ == "__main__":
    cmd_group()
