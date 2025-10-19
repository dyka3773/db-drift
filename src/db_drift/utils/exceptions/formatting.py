"""Error formatting utilities for db-drift."""

import logging
import sys
import traceback
from typing import TextIO

from db_drift.utils.constants import ExitCode
from db_drift.utils.exceptions import CliArgumentError, DatabaseConnectionError, MissingConfigError
from db_drift.utils.exceptions.base import DbDriftError, DbDriftSystemError


def format_error_message(error: Exception, show_traceback: bool = False) -> str:  # noqa: FBT001, FBT002
    """
    Format an error message for display to the user.

    Args:
        error: The exception to format
        show_traceback: Whether to include traceback information. Default is False.

    Returns:
        Formatted error message
    """
    if isinstance(error, DbDriftError):
        message = str(error)
    else:
        # For unexpected exceptions, provide a generic message
        message = f"An unexpected error occurred: {error.__class__.__name__}"
        if str(error):
            message += f": {error}"

    if show_traceback:
        message += f"\n\nTraceback:\n{''.join(traceback.format_exception(type(error), error, error.__traceback__))}"

    return message


def format_suggestion(error: Exception) -> str | None:
    """
    Generate helpful suggestions for common errors.

    Args:
        error: The exception to generate suggestions for

    Returns:
        Suggestion string or None if no suggestion is available
    """
    if isinstance(error, CliArgumentError):
        return "Use 'db-drift --help' to see available options and their usage."

    if isinstance(error, DatabaseConnectionError):
        suggestions = [
            "Check that the database server is running and accessible",
            "Verify your connection parameters (host, port, database name)",
            "Ensure your credentials are correct",
            "Check network connectivity and firewall settings",
        ]
        return "Try the following:\n" + "\n".join(f"  • {suggestion}" for suggestion in suggestions)

    if isinstance(error, MissingConfigError):
        return "Create a configuration file or provide the required settings via command-line arguments."

    return None


def print_error(
    error: Exception,
    file: TextIO = sys.stderr,
    show_traceback: bool = False,  # noqa: FBT001, FBT002
    show_suggestions: bool = True,  # noqa: FBT001, FBT002
) -> None:
    """
    Print a formatted error message to the specified file.

    Args:
        error: The exception to print
        file: The file to write to (default: stderr)
        show_traceback: Whether to include traceback information
        show_suggestions: Whether to show helpful suggestions
    """
    message = format_error_message(error, show_traceback)
    print(f"Error: {message}", file=file)

    if show_suggestions:
        suggestion = format_suggestion(error)
        if suggestion:
            print(f"\n{suggestion}", file=file)


def get_exit_code(error: Exception) -> int:
    """
    Get the appropriate exit code for an exception.

    Args:
        error: The exception

    Returns:
        Exit code integer
    """
    if isinstance(error, DbDriftError):
        return error.exit_code

    # Standard exit codes for common Python exceptions
    if isinstance(error, KeyboardInterrupt):
        return ExitCode.SIGINT
    if isinstance(error, FileNotFoundError):
        return ExitCode.NO_INPUT
    if isinstance(error, PermissionError):
        return ExitCode.NO_PERMISSION
    if isinstance(error, ConnectionError):
        return ExitCode.UNAVAILABLE

    # Default generic error
    return ExitCode.GENERAL_ERROR


def handle_error_and_exit(
    error: Exception,
    logger: logging.Logger | None = None,
    show_traceback: bool = False,  # noqa: FBT001, FBT002
    show_suggestions: bool = True,  # noqa: FBT001, FBT002
) -> None:
    """
    Handle an error by logging it, printing user-friendly message, and exiting.

    Args:
        error: The exception to handle
        logger: Logger instance for detailed logging
        show_traceback: Whether to show traceback to user
        show_suggestions: Whether to show helpful suggestions
    """
    exit_code = get_exit_code(error)

    # Log the full error details
    if logger:
        if isinstance(error, DbDriftError):
            logger.error(f"{error.__class__.__name__}: {error}")
        else:
            logger.exception(f"Unexpected error: {error.__class__.__name__}: {error}")

    # Print user-friendly error
    print_error(error, show_traceback=show_traceback, show_suggestions=show_suggestions)

    sys.exit(exit_code)


def handle_unexpected_error(debug_mode: int, logger: logging.Logger) -> None:
    """
    Handle unexpected errors based on debug mode.

    Args:
        debug_mode(int): Whether debug mode is enabled (1/True) or not (0/False).
        logger(logging.Logger): The logger instance to use.
    """
    if debug_mode:
        # For debug mode, we'll handle the current exception
        _, exc_value, _ = sys.exc_info()
        if exc_value:
            handle_error_and_exit(
                exc_value,
                logger=logger,
                show_traceback=True,
                show_suggestions=False,
            )
    else:
        system_error = DbDriftSystemError(
            "An unexpected error occurred. Set DB_DRIFT_DEBUG=1 for more details.",
            exit_code=ExitCode.GENERAL_ERROR,
        )
        handle_error_and_exit(
            system_error,
            logger=logger,
            show_traceback=False,
            show_suggestions=False,
        )
