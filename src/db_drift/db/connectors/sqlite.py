import sqlite3

from db_drift.db.connectors.base_connector import BaseDBConnector
from db_drift.db.strategies.sqlite import fetch_sqlite_triggers


class SQLiteConnector(BaseDBConnector):
    def __init__(self, connection_string: str) -> None:
        """
        Initialize the SQLiteConnector with a connection string.

        Args:
            connection_string (str): The connection string for the SQLite database.
        """
        super().__init__(connection_string)

        self.SUPPORTED_OBJECTS_REGISTRY = {
            # "tables": self.fetch_sqlite_tables,  # noqa: ERA001
            # "views": self.fetch_sqlite_views,  # noqa: ERA001
            # "indexes": self.fetch_sqlite_indexes,  # noqa: ERA001
            "triggers": fetch_sqlite_triggers,
        }

        self.connection_library = sqlite3
