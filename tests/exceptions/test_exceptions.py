"""Tests for exception handling in db-drift."""

from db_drift.constants import ExitCode
from db_drift.utils.exceptions import (
    CliArgumentError,
    CliError,
    CliUsageError,
    ConfigError,
    ConfigValidationError,
    DatabaseConnectionError,
    DatabaseError,
    DbDriftError,
    DbDriftInterruptError,
    DbDriftSystemError,
    DbDriftUserError,
    MissingConfigError,
)
from db_drift.utils.exceptions.database import DatabaseQueryError
from db_drift.utils.exceptions.formatting import format_error_message, format_suggestion, get_exit_code


class TestBaseExceptions:
    """Test base exception classes."""

    def test_db_drift_error_creation(self) -> None:
        """Test DbDriftError creation with message and exit code."""
        overridden_exit_code = 5

        error = DbDriftError("Test error", exit_code=overridden_exit_code)
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.exit_code == overridden_exit_code

    def test_db_drift_error_default_exit_code(self) -> None:
        """Test DbDriftError uses default exit code."""
        error = DbDriftError("Test error")
        assert error.exit_code == ExitCode.GENERAL_ERROR

    def test_db_drift_user_error_exit_code(self) -> None:
        """Test DbDriftUserError default exit code."""
        error = DbDriftUserError("User error")
        assert error.exit_code == ExitCode.USAGE_ERROR

    def test_db_drift_system_error_exit_code(self) -> None:
        """Test DbDriftSystemError default exit code."""
        error = DbDriftSystemError("System error")
        assert error.exit_code == ExitCode.GENERAL_ERROR

    def test_db_drift_interrupt_error(self) -> None:
        """Test DbDriftInterruptError default behavior."""
        error = DbDriftInterruptError()
        assert error.exit_code == ExitCode.SIGINT
        assert "cancelled by user" in str(error)


class TestCliExceptions:
    """Test CLI-specific exceptions."""

    def test_cli_error_creation(self) -> None:
        """Test CliError creation."""
        error = CliError("CLI error")
        assert str(error) == "CLI error"
        assert error.exit_code == ExitCode.USAGE_ERROR

    def test_cli_argument_error_with_argument(self) -> None:
        """Test CliArgumentError with argument name."""
        error = CliArgumentError("Invalid value", argument="--source")
        assert "Invalid argument '--source': Invalid value" in str(error)
        assert error.argument == "--source"

    def test_cli_argument_error_without_argument(self) -> None:
        """Test CliArgumentError without argument name."""
        error = CliArgumentError("Invalid value")
        assert str(error) == "Invalid argument: Invalid value"
        assert error.argument is None

    def test_cli_usage_error_with_suggestion(self) -> None:
        """Test CliUsageError with suggestion."""
        error = CliUsageError("Wrong usage", suggestion="Try --help")
        assert "Wrong usage" in str(error)
        assert "Try --help" in str(error)
        assert error.suggestion == "Try --help"

    def test_cli_usage_error_without_suggestion(self) -> None:
        """Test CliUsageError without suggestion."""
        error = CliUsageError("Wrong usage")
        assert str(error) == "Wrong usage"
        assert error.suggestion is None


class TestDatabaseExceptions:
    """Test database-related exceptions."""

    def test_database_error_creation(self) -> None:
        """Test DatabaseError creation."""
        error = DatabaseError("DB error", connection_string="postgresql://...")
        assert str(error) == "DB error"
        assert error.connection_string == "postgresql://..."

    def test_database_connection_error_with_host_and_db(self) -> None:
        """Test DatabaseConnectionError with host and database."""
        error = DatabaseConnectionError("Connection failed", host="localhost", port=5432, database="mydb")
        expected = "Failed to connect to database 'mydb' on localhost:5432: Connection failed"
        assert str(error) == expected
        assert error.host == "localhost"
        assert error.port == 5432  # noqa: PLR2004
        assert error.database == "mydb"

    def test_database_connection_error_simple(self) -> None:
        """Test DatabaseConnectionError without host details."""
        error = DatabaseConnectionError("Connection failed")
        assert str(error) == "Database connection failed: Connection failed"

    def test_database_query_error(self) -> None:
        """Test DatabaseQueryError."""
        error = DatabaseQueryError("Query failed", query="SELECT * FROM users")
        assert str(error) == "Database query failed: Query failed"
        assert error.query == "SELECT * FROM users"


class TestConfigExceptions:
    """Test configuration-related exceptions."""

    def test_config_error_with_path(self) -> None:
        """Test ConfigError with config path."""
        error = ConfigError("Invalid config", config_path="/path/to/config.yml")
        expected = "Configuration error in '/path/to/config.yml': Invalid config"
        assert str(error) == expected
        assert error.config_path == "/path/to/config.yml"

    def test_config_error_without_path(self) -> None:
        """Test ConfigError without config path."""
        error = ConfigError("Invalid config")
        assert str(error) == "Configuration error: Invalid config"
        assert error.config_path is None

    def test_missing_config_error_with_setting(self) -> None:
        """Test MissingConfigError with setting name."""
        error = MissingConfigError("Required setting missing", config_path="/path/config.yml", setting_name="database_url")
        expected = "Missing required setting 'database_url' in '/path/config.yml': Required setting missing"
        assert str(error) == expected
        assert error.setting_name == "database_url"

    def test_config_validation_error(self) -> None:
        """Test ConfigValidationError."""
        error = ConfigValidationError("Invalid format", setting_name="port", setting_value="not_a_number")
        expected = "Invalid value 'not_a_number' for setting 'port': Invalid format"
        assert expected in str(error)


class TestExceptionFormatting:
    """Test exception formatting utilities."""

    def test_format_error_message_with_db_drift_error(self) -> None:
        """Test formatting DbDriftError."""
        error = CliError("Test CLI error")
        message = format_error_message(error)
        assert message == "Test CLI error"

    def test_format_error_message_with_generic_error(self) -> None:
        """Test formatting generic exception."""
        error = ValueError("Test value error")
        message = format_error_message(error)
        assert "An unexpected error occurred: ValueError" in message
        assert "Test value error" in message

    def test_get_exit_code_with_db_drift_error(self) -> None:
        """Test getting exit code from DbDriftError."""
        error = CliError("CLI error")
        exit_code = get_exit_code(error)
        assert exit_code == ExitCode.USAGE_ERROR

    def test_get_exit_code_with_keyboard_interrupt(self) -> None:
        """Test getting exit code from KeyboardInterrupt."""
        error = KeyboardInterrupt()
        exit_code = get_exit_code(error)
        assert exit_code == ExitCode.SIGINT

    def test_format_suggestion_for_cli_argument_error(self) -> None:
        """Test suggestion formatting for CLI argument error."""
        error = CliArgumentError("Invalid argument")
        suggestion = format_suggestion(error)
        assert suggestion is not None
        assert "db-drift --help" in suggestion

    def test_format_suggestion_for_database_connection_error(self) -> None:
        """Test suggestion formatting for database connection error."""
        error = DatabaseConnectionError("Connection failed")
        suggestion = format_suggestion(error)
        assert suggestion is not None
        assert "database server is running" in suggestion

    def test_format_suggestion_for_missing_config_error(self) -> None:
        """Test suggestion formatting for missing config error."""
        error = MissingConfigError("Config missing")
        suggestion = format_suggestion(error)
        assert suggestion is not None
        assert "configuration file" in suggestion
