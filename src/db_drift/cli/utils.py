from argparse import Namespace
from importlib import metadata

from db_drift.utils.exceptions import CliArgumentError, CliUsageError


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
        raise CliUsageError(msg)

    if "://" not in args.source or "://" not in args.target:
        msg = "Malformed connection string: both source and target must contain '://'."
        raise CliArgumentError(msg)

    if args.source.split("://")[0] != args.target.split("://")[0]:
        msg = "Source and target databases must be of the same DBMS type."  # As of Issue #50
        raise CliArgumentError(msg)
