"""Base exceptions for db-drift application."""


from db_drift.utils.exceptions.status_codes import ExitCode


class DbDriftError(Exception):
    """Base exception for all db-drift related errors."""

    def __init__(self, message: str, exit_code: int = ExitCode.GENERAL_ERROR) -> None:
        """
        Initialize the exception.

        Args:
            message: The error message
            exit_code: The exit code to use when this error causes program termination
        """
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code

    def __str__(self) -> str:
        """Return the error message."""
        return self.message


class DbDriftUserError(DbDriftError):
    """Base class for user-caused errors (wrong arguments, invalid config, etc.)."""

    def __init__(self, message: str, exit_code: int = ExitCode.USAGE_ERROR) -> None:
        """Initialize user error with default exit code 2."""
        super().__init__(message, exit_code)


class DbDriftSystemError(DbDriftError):
    """Base class for system-level errors (network issues, permission errors, etc.)."""

    def __init__(self, message: str, exit_code: int = ExitCode.GENERAL_ERROR) -> None:
        """Initialize system error with default exit code 1."""
        super().__init__(message, exit_code)


class DbDriftInterruptError(DbDriftError):
    """Exception for user interruption (Ctrl+C)."""

    def __init__(self, message: str = "Operation cancelled by user") -> None:
        """Initialize interrupt error with standard Unix signal exit code."""
        # 128 + SIGINT (2) = 130
        super().__init__(message, exit_code=ExitCode.SIGINT)
