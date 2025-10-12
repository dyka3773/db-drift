import argparse


def cli() -> None:
    parser = argparse.ArgumentParser(
        prog="db-drift",
        description="A command-line tool to visualize the differences between two DB states.",
    )

    args = parser.parse_args()
