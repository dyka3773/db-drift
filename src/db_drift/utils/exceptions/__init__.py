"""Custom exceptions for db-drift application."""

from db_drift.utils.exceptions.base import DbDriftError, DbDriftInterruptError, DbDriftSystemError, DbDriftUserError
from db_drift.utils.exceptions.cli import CliArgumentError, CliConfigError, CliError, CliUsageError
from db_drift.utils.exceptions.config import ConfigError, ConfigFormatError, ConfigValidationError, MissingConfigError
from db_drift.utils.exceptions.database import (
    DatabaseAuthenticationError,
    DatabaseConnectionError,
    DatabaseError,
    DatabaseQueryError,
    DatabaseSchemaError,
    DatabaseTimeoutError,
)
from db_drift.utils.exceptions.status_codes import ExitCode

__all__ = [
    "CliArgumentError",
    "CliConfigError",
    "CliError",
    "CliUsageError",
    "ConfigError",
    "ConfigFormatError",
    "ConfigValidationError",
    "DatabaseAuthenticationError",
    "DatabaseConnectionError",
    "DatabaseError",
    "DatabaseQueryError",
    "DatabaseSchemaError",
    "DatabaseTimeoutError",
    "DbDriftError",
    "DbDriftInterruptError",
    "DbDriftSystemError",
    "DbDriftUserError",
    "ExitCode",
    "MissingConfigError",
]
