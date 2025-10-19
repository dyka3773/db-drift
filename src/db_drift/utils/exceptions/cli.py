"""CLI-specific exceptions for db-drift."""

from db_drift.utils.constants import ExitCode
from db_drift.utils.exceptions.base import DbDriftUserError


class CliError(DbDriftUserError):
    """Base class for CLI-related errors."""

    def __init__(self, message: str, exit_code: ExitCode = ExitCode.USAGE_ERROR) -> None:
        """
        Initialize CLI error.

        Args:
            message: The error message
            exit_code: The exit code (default 2 for CLI usage errors)
        """
        super().__init__(message, exit_code)


class CliArgumentError(CliError):
    """Exception for invalid command-line arguments."""

    def __init__(self, message: str, argument: str | None = None) -> None:
        """
        Initialize argument error.

        Args:
            message: The error message
            argument: The problematic argument name
        """
        full_message = f"Invalid argument '{argument}': {message}" if argument else f"Invalid argument: {message}"
        super().__init__(full_message)
        self.argument = argument


class CliUsageError(CliError):
    """Exception for incorrect CLI usage."""

    def __init__(self, message: str, suggestion: str | None = None) -> None:
        """
        Initialize usage error.

        Args:
            message: The error message
            suggestion: Optional suggestion for correct usage
        """
        full_message = message
        if suggestion:
            full_message += f"\n\nSuggestion: {suggestion}"
        super().__init__(full_message)
        self.suggestion = suggestion


class CliConfigError(CliError):
    """Exception for CLI configuration issues."""

    def __init__(self, message: str, config_path: str | None = None) -> None:
        """
        Initialize config error.

        Args:
            message: The error message
            config_path: Path to the problematic config file
        """
        full_message = f"Configuration error in '{config_path}': {message}" if config_path else f"Configuration error: {message}"
        super().__init__(full_message)
        self.config_path = config_path
