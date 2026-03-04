from enum import Enum, unique
from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db_drift.db.connectors.base_connector import BaseDBConnector


@unique
class ExitCode(Enum):
    SUCCESS = 0
    GENERAL_ERROR = 1
    USAGE_ERROR = 2
    DATA_ERROR = 65
    NO_INPUT = 66
    UNAVAILABLE = 69
    SOFTWARE_ERROR = 70
    NO_PERMISSION = 77
    CONFIG_ERROR = 78
    SIGINT = 130


def get_supported_dbms_registry() -> dict[str, type["BaseDBConnector"]]:
    """
    Return supported DBMS connector classes.

    Imports are kept inside this function to avoid circular imports at module load time.
    """
    sqlite_module = import_module("db_drift.db.connectors.sqlite")
    oracle_module = import_module("db_drift.db.connectors.oracle")

    sqlite_connector = sqlite_module.SQLiteConnector
    oracle_connector = oracle_module.OracleConnector

    # An easy-to-update registry pattern for supported DBMS connectors
    return {
        "sqlite": sqlite_connector,
        "oracle": oracle_connector,
        # As we add more connectors, uncomment the lines below
        # "postgresql": PostgresConnector,  # noqa: ERA001
        # "mysql": MySQLConnector,  # noqa: ERA001
    }


@unique
class DBConstraintType(Enum):
    PRIMARY_KEY = "PRIMARY KEY"
    FOREIGN_KEY = "FOREIGN KEY"
    UNIQUE = "UNIQUE"
    CHECK = "CHECK"
    NOT_NULL = "NOT NULL"
    EXCLUSION = "EXCLUSION"  # PostgreSQL specific
    READ_ONLY = "READ ONLY"  # For Oracle views
    CHECK_OPTION = "CHECK OPTION"  # For Oracle views
