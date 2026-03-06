import sqlite3

from db_drift.models.index import Index
from db_drift.models.trigger import Trigger
from db_drift.utils.string import hash_body


def fetch_sqlite_indexes(cursor: sqlite3.Cursor) -> dict[str, Index]:
    """
    Fetch SQLite indexes from the database catalog.

    Args:
        cursor (sqlite3.Cursor): The SQLite database cursor.

    Returns:
        dict[str, Index]: A dictionary of Index objects keyed by index name.
    """
    select_indexes = """
        SELECT
            name,
            tbl_name
        FROM sqlite_master
        WHERE type = 'index'
        ORDER BY tbl_name, name
    """
    cursor.execute(select_indexes)
    index_rows = cursor.fetchall()
    indexes: dict[str, Index] = {}

    for index_name, table_name in index_rows:
        cursor.execute(f"PRAGMA index_list('{table_name}')")
        index_list_rows = cursor.fetchall()
        uniqueness = next(
            ("UNIQUE" if row[2] else "NONUNIQUE" for row in index_list_rows if row[1] == index_name),
            "NONUNIQUE",
        )

        cursor.execute(f"PRAGMA index_info('{index_name}')")
        index_info_rows = cursor.fetchall()
        indexes[index_name] = Index(
            table_name=table_name,
            uniqueness=uniqueness,
            columns={row[2] for row in index_info_rows if row[2] is not None},
        )

    return indexes


def fetch_sqlite_triggers(cursor: sqlite3.Cursor) -> dict[str, Trigger]:
    """
    Fetch SQLite triggers from the database catalog.

    Args:
        cursor (sqlite3.Cursor): The SQLite database cursor.

    Returns:
        dict[str, Trigger]: A dictionary of Trigger objects keyed by trigger name.
    """
    select_triggers = """
        SELECT
            name,
            tbl_name,
            sql
        FROM sqlite_master
        WHERE type = 'trigger'
        ORDER BY tbl_name, name
    """
    cursor.execute(select_triggers)
    trigger_rows = cursor.fetchall()

    return {
        row[0]: Trigger(
            body=hash_body(row[2] or ""),
            definition=f"table: {row[1]}",
        )
        for row in trigger_rows
    }
