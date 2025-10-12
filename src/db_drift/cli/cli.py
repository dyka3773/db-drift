import argparse

from db_drift.cli.utils import get_version


def cli() -> None:
    parser = argparse.ArgumentParser(
        prog="db-drift",
        description="A command-line tool to visualize the differences between two DB states.",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"db-drift {get_version()}",
    )

    _ = parser.parse_args()
