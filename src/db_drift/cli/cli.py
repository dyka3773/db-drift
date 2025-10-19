import argparse
import logging

from db_drift.cli.utils import check_args_validity, get_version
from db_drift.utils.constants import SUPPORTED_DBMS
from db_drift.utils.custom_logging import handle_verbose_logging
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
        required=True,
        help="Specify the type of DBMS (default: sqlite)",
        default="sqlite",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output filename for the drift report (default: drift_report.html)",
        default="drift_report.html",
    )

    parser.add_argument(
        "--source",
        required=True,
        help="Connection string for the source database",
    )

    parser.add_argument(
        "--target",
        required=True,
        help="Connection string for the target database",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging output",
    )

    try:
        args = parser.parse_args()

        if args.verbose:
            handle_verbose_logging()
            logger.debug("Verbose mode enabled.")

        logger.debug(f"Parsed arguments: {args}")

        check_args_validity(args)

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
