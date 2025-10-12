"""Configuration-related exceptions for db-drift."""

from pathlib import Path

from db_drift.constants import ExitCode
from db_drift.utils.exceptions.base import DbDriftUserError


class ConfigError(DbDriftUserError):
    """Base class for configuration-related errors."""

    def __init__(self, message: str, config_path: str | Path | None = None) -> None:
        """
        Initialize configuration error.

        Args:
            message: The error message
            config_path: Path to the problematic configuration file
        """
        full_message = f"Configuration error in '{config_path}': {message}" if config_path else f"Configuration error: {message}"

        super().__init__(full_message)
        self.exit_code = ExitCode.CONFIG_ERROR
        self.config_path = str(config_path) if config_path else None


class MissingConfigError(ConfigError):
    """Exception for missing configuration files or required settings."""

    def __init__(
        self,
        message: str,
        config_path: str | Path | None = None,
        setting_name: str | None = None,
    ) -> None:
        """
        Initialize missing config error.

        Args:
            message: The error message
            config_path: Path to the configuration file
            setting_name: Name of the missing setting
        """
        if setting_name and config_path:
            full_message = f"Missing required setting '{setting_name}' in '{config_path}': {message}"
        elif setting_name:
            full_message = f"Missing required setting '{setting_name}': {message}"
        elif config_path:
            full_message = f"Missing configuration file '{config_path}': {message}"
        else:
            full_message = f"Missing configuration: {message}"

        # Call ConfigError.__init__ instead of super() to avoid double processing
        DbDriftUserError.__init__(self, full_message)
        self.config_path = str(config_path) if config_path else None
        self.setting_name = setting_name


class ConfigValidationError(ConfigError):
    """Exception for invalid configuration values."""

    def __init__(
        self,
        message: str,
        config_path: str | Path | None = None,
        setting_name: str | None = None,
        setting_value: str | None = None,
    ) -> None:
        """
        Initialize validation error.

        Args:
            message: The error message
            config_path: Path to the configuration file
            setting_name: Name of the invalid setting
            setting_value: The invalid value
        """
        if setting_name and setting_value:
            full_message = f"Invalid value '{setting_value}' for setting '{setting_name}': {message}"
        elif setting_name:
            full_message = f"Invalid setting '{setting_name}': {message}"
        else:
            full_message = f"Invalid configuration: {message}"

        # Call ConfigError.__init__ to get proper path handling
        super().__init__(full_message, config_path)
        self.setting_name = setting_name
        self.setting_value = setting_value


class ConfigFormatError(ConfigError):
    """Exception for configuration file format errors."""

    def __init__(
        self,
        message: str,
        config_path: str | Path | None = None,
        line_number: int | None = None,
    ) -> None:
        """
        Initialize format error.

        Args:
            message: The error message
            config_path: Path to the configuration file
            line_number: Line number where the error occurred
        """
        if line_number and config_path:
            full_message = f"Format error in '{config_path}' at line {line_number}: {message}"
        elif config_path:
            full_message = f"Format error in '{config_path}': {message}"
        else:
            full_message = f"Configuration format error: {message}"

        # Call ConfigError.__init__ to get proper path handling
        super().__init__(full_message, config_path)
        self.line_number = line_number
