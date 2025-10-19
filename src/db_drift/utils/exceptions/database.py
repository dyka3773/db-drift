"""Database-related exceptions for db-drift."""

from db_drift.utils.constants import ExitCode
from db_drift.utils.exceptions.base import DbDriftSystemError


class DatabaseError(DbDriftSystemError):
    """Base class for database-related errors."""

    def __init__(self, message: str, connection_string: str | None = None) -> None:
        """
        Initialize database error.

        Args:
            message: The error message
            connection_string: Optional connection string (will be redacted in logs)
        """
        super().__init__(message)
        self.connection_string = connection_string


class DatabaseConnectionError(DatabaseError):
    """Exception for database connection failures."""

    def __init__(
        self,
        message: str,
        connection_string: str | None = None,
        host: str | None = None,
        port: int | None = None,
        database: str | None = None,
    ) -> None:
        """
        Initialize connection error.

        Args:
            message: The error message
            connection_string: Optional connection string
            host: Database host
            port: Database port
            database: Database name
        """
        if host and database:
            full_message = f"Failed to connect to database '{database}' on {host}"
            if port:
                full_message += f":{port}"
            full_message += f": {message}"
        else:
            full_message = f"Database connection failed: {message}"

        # Override the default exit code for connection errors
        super().__init__(full_message, connection_string)
        self.exit_code = ExitCode.UNAVAILABLE
        self.host = host
        self.port = port
        self.database = database


class DatabaseQueryError(DatabaseError):
    """Exception for database query execution errors."""

    def __init__(
        self,
        message: str,
        query: str | None = None,
        connection_string: str | None = None,
    ) -> None:
        """
        Initialize query error.

        Args:
            message: The error message
            query: The problematic SQL query
            connection_string: Optional connection string
        """
        full_message = f"Database query failed: {message}"
        super().__init__(full_message, connection_string)
        self.exit_code = ExitCode.SOFTWARE_ERROR
        self.query = query


class DatabaseSchemaError(DatabaseError):
    """Exception for database schema-related errors."""

    def __init__(
        self,
        message: str,
        schema_name: str | None = None,
        connection_string: str | None = None,
    ) -> None:
        """
        Initialize schema error.

        Args:
            message: The error message
            schema_name: The problematic schema name
            connection_string: Optional connection string
        """
        full_message = f"Schema '{schema_name}' error: {message}" if schema_name else f"Database schema error: {message}"

        super().__init__(full_message, connection_string)
        self.exit_code = ExitCode.DATA_ERROR
        self.schema_name = schema_name


class DatabaseAuthenticationError(DatabaseError):
    """Exception for database authentication failures."""

    def __init__(
        self,
        message: str = "Authentication failed",
        username: str | None = None,
        connection_string: str | None = None,
    ) -> None:
        """
        Initialize authentication error.

        Args:
            message: The error message
            username: The username that failed authentication
            connection_string: Optional connection string
        """
        full_message = f"Authentication failed for user '{username}': {message}" if username else f"Database authentication failed: {message}"

        super().__init__(full_message, connection_string)
        self.exit_code = ExitCode.NO_PERMISSION
        self.username = username


class DatabaseTimeoutError(DatabaseError):
    """Exception for database operation timeouts."""

    def __init__(
        self,
        message: str = "Operation timed out",
        timeout_seconds: float | None = None,
        connection_string: str | None = None,
    ) -> None:
        """
        Initialize timeout error.

        Args:
            message: The error message
            timeout_seconds: The timeout value that was exceeded
            connection_string: Optional connection string
        """
        if timeout_seconds:
            full_message = f"Database operation timed out after {timeout_seconds}s: {message}"
        else:
            full_message = f"Database operation timed out: {message}"

        super().__init__(full_message, connection_string)
        self.timeout_seconds = timeout_seconds
