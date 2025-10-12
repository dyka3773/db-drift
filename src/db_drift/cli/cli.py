import argparse
import logging

from db_drift.cli.utils import get_version
from db_drift.constants import SUPPORTED_DBMS
from db_drift.utils.exceptions import CliArgumentError, CliUsageError

logger = logging.getLogger("db-drift")


def cli() -> None:
    parser = argparse.ArgumentParser(
        prog="db-drift",
        description="A command-line tool to visualize the differences between two DB states.",
        exit_on_error=False,  # We'll handle errors ourselves
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"db-drift {get_version()}",
    )

    parser.add_argument(
        "--dbms",
        choices=SUPPORTED_DBMS,
        help="Specify the type of DBMS (default: sqlite)",
        default="sqlite",
    )

    try:
        _ = parser.parse_args()
    except argparse.ArgumentError as e:
        msg = f"Invalid argument: {e}"
        raise CliArgumentError(msg) from e
    except SystemExit as e:
        # argparse calls sys.exit() on error, convert to our exception
        if e.code != 0:
            msg = "Invalid command line arguments. Use --help for usage information."
            raise CliUsageError(msg) from e
        # Re-raise if it's a successful exit (like --help)
        raise
