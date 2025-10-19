"""Error formatting utilities for db-drift."""

import logging
import sys
import traceback

from db_drift.utils.constants import ExitCode
from db_drift.utils.exceptions import CliArgumentError, DatabaseConnectionError, MissingConfigError
from db_drift.utils.exceptions.base import DbDriftError


def format_error_message(error: Exception) -> str:
    """
    Format an error message for display to the user.

    Args:
        error: The exception to format
    Returns:
        Formatted error message string
    """
    if isinstance(error, DbDriftError):
        message = str(error)
    else:
        # For unexpected exceptions, provide a generic message
        message = f"An unexpected error occurred: {error.__class__.__name__}"
        if str(error):
            message += f": {error}"

    return message


def get_error_stacktrace(error: Exception) -> str | None:
    """
    Get the stacktrace of an error if traceback is to be shown.

    Args:
        error: The exception to get the stacktrace for
    Returns:
        Stacktrace string or None if not applicable
    """
    return "".join(traceback.format_exception(type(error), error, error.__traceback__))


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


def log_error(
    error: Exception,
    logger: logging.Logger,
    show_traceback: bool = False,  # noqa: FBT001, FBT002
    show_suggestions: bool = True,  # noqa: FBT001, FBT002
) -> None:
    """
    Print a formatted error message to the specified file.

    Args:
        error: The exception to print
        logger: Logger instance for logging
        show_traceback: Whether to include traceback information
        show_suggestions: Whether to show helpful suggestions
    """
    message = format_error_message(error)
    logger.error(f"Error: {message}")

    if show_traceback:
        stacktrace = get_error_stacktrace(error)
        logger.debug(f"Stacktrace:\n{stacktrace}")

    if show_suggestions:
        suggestion = format_suggestion(error)
        if suggestion:
            logger.error(suggestion)


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
        return ExitCode.SIGINT.value
    if isinstance(error, FileNotFoundError):
        return ExitCode.NO_INPUT.value
    if isinstance(error, PermissionError):
        return ExitCode.NO_PERMISSION.value
    if isinstance(error, ConnectionError):
        return ExitCode.UNAVAILABLE.value

    # Default generic error
    return ExitCode.GENERAL_ERROR.value


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
            logger.debug(f"{error.__class__.__name__}: {error}")
        else:
            logger.debug(f"Unexpected error: {error.__class__.__name__}: {error}")

    # Print user-friendly error
    log_error(
        error,
        logger=logger,
        show_traceback=show_traceback,
        show_suggestions=show_suggestions,
    )

    sys.exit(exit_code)
