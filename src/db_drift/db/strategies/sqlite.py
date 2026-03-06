import sqlite3

from db_drift.models.trigger import Trigger
from db_drift.utils.string import hash_body


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
            AND name NOT LIKE 'sqlite_%'
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
