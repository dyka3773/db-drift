import sqlite3

from db_drift.db.connectors.base_connector import BaseDBConnector
from db_drift.db.strategies.sqlite import fetch_sqlite_indexes, fetch_sqlite_tables, fetch_sqlite_triggers, fetch_sqlite_views


class SQLiteConnector(BaseDBConnector):
    def __init__(self, connection_string: str) -> None:
        """
        Initialize the SQLiteConnector with a connection string.

        Args:
            connection_string (str): The connection string for the SQLite database.
        """
        super().__init__(connection_string)

        self.SUPPORTED_OBJECTS_REGISTRY = {
            "tables": fetch_sqlite_tables,
            "views": fetch_sqlite_views,
            "indexes": fetch_sqlite_indexes,
            "triggers": fetch_sqlite_triggers,
        }

        self.connection_library = sqlite3
