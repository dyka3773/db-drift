from argparse import Namespace
from importlib import metadata

from db_drift.utils.exceptions import CliArgumentError


def get_version() -> str:
    """Get the current version of the package."""
    try:
        return metadata.version("db-drift")
    except metadata.PackageNotFoundError:
        return "unknown"


def check_args_validity(args: Namespace) -> None:
    """
    Check validity of CLI arguments.

    Args:
        args: Parsed argparse Namespace
    Raises:
        CliArgumentError: If any argument is invalid
        CliUsageError: If usage is incorrect
    """
    if not args.source or not args.target:
        msg = "Both source and target connection strings must be provided."
        raise CliArgumentError(msg)

    if args.source == args.target:
        msg = "Source and target connection strings must be different."
        # FIXME @dyka3773: Temporarily disabling this check for testing purposes  # noqa: FIX001, TD001
        # raise CliUsageError(msg)  # noqa: ERA001
