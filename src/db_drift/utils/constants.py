from enum import Enum, unique

from db_drift.db.connectors.base_connector import BaseDBConnector
from db_drift.db.connectors.oracle import OracleConnector
from db_drift.db.connectors.sqlite import SQLiteConnector


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


# An easy-to-update registry pattern for supported DBMS connectors
SUPPORTED_DBMS_REGISTRY: dict[str, BaseDBConnector] = {
    "sqlite": SQLiteConnector,
    "oracle": OracleConnector,
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
