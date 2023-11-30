import click
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


@click.group()
def cmd_group():
    """A CLI tool for gammaspotter."""
    pass


@cmd_group.command()
@click.argument(
    "path", type=click.Path("rb", dir_okay=False, executable=False, path_type=Path)
)
def graph(path: Path):
    """Display a measurement in CSV format as an interactive MPL plot.

    Args:
        path (str): location of the data file that should be displayed
    """
    data = pd.read_csv(path)
    data.plot(
        "pulseheight",
        "counts_ch_A",
        legend=False,
        xlabel="Pulseheight",
        ylabel="Counts",
        title=path.stem,
    )
    plt.show()


if __name__ == "__main__":
    cmd_group()
