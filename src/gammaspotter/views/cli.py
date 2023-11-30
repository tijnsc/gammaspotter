import click


@click.group()
def cmd_group():
    """A CLI tool for gammaspotter."""
    pass


@cmd_group.command()
@click.argument("path", type=click.Path("rb"))
def graph(path):
    print(f"{path=}")


if __name__ == "__main__":
    cmd_group()
