import sqlite3
from collections.abc import Callable
from typing import TypeVar

from db_drift.models.column import Column
from db_drift.models.index import Index
from db_drift.models.table import Table
from db_drift.models.trigger import Trigger
from db_drift.models.view import View
from db_drift.utils.string import hash_body

PRAGMA_TABLE_INFO_NAME_INDEX = 1
PRAGMA_TABLE_INFO_TYPE_INDEX = 2
PRAGMA_TABLE_INFO_NOT_NULL_INDEX = 3
PRAGMA_TABLE_INFO_PRIMARY_KEY_INDEX = 5
PRAGMA_TABLE_XINFO_HIDDEN_INDEX = 6
PRAGMA_TABLE_XINFO_MIN_LENGTH = 7

TableLike = TypeVar("TableLike", Table, View)


def fetch_sqlite_tables(cursor: sqlite3.Cursor) -> dict[str, Table]:
    """
    Fetch SQLite tables from the database catalog.

    Args:
        cursor (sqlite3.Cursor): The SQLite database cursor.

    Returns:
        dict[str, Table]: A dictionary of Table objects keyed by table name.
    """
    return _fetch_sqlite_table_like_objects(cursor, object_type="table", model_factory=Table)


def fetch_sqlite_views(cursor: sqlite3.Cursor) -> dict[str, View]:
    """
    Fetch SQLite views from the database catalog.

    Args:
        cursor (sqlite3.Cursor): The SQLite database cursor.

    Returns:
        dict[str, View]: A dictionary of View objects keyed by view name.
    """
    return _fetch_sqlite_table_like_objects(cursor, object_type="view", model_factory=View)


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
        cursor.execute(f"PRAGMA index_list('{_escape_sqlite_name(table_name)}')")
        index_list_rows = cursor.fetchall()
        uniqueness = next(
            ("UNIQUE" if row[2] else "NONUNIQUE" for row in index_list_rows if row[1] == index_name),
            "NONUNIQUE",
        )

        cursor.execute(f"PRAGMA index_info('{_escape_sqlite_name(index_name)}')")
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


def _escape_sqlite_name(name: str) -> str:
    """Escape single quotes in SQLite identifiers used in PRAGMA string arguments."""
    return name.replace("'", "''")


def _fetch_sqlite_table_like_objects(
    cursor: sqlite3.Cursor,
    object_type: str,
    model_factory: Callable[..., TableLike],
) -> dict[str, TableLike]:
    """Fetch table-like SQLite objects and their columns from the database catalog."""
    select_objects = f"""
        SELECT
            name
        FROM sqlite_master
        WHERE type = '{object_type}'
            AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """
    cursor.execute(select_objects)
    object_rows = cursor.fetchall()
    objects: dict[str, TableLike] = {}

    for (object_name,) in object_rows:
        cursor.execute(f"PRAGMA table_xinfo('{_escape_sqlite_name(object_name)}')")
        column_rows = cursor.fetchall()
        objects[object_name] = model_factory(doc="", columns={})

        for column in column_rows:
            hidden = column[PRAGMA_TABLE_XINFO_HIDDEN_INDEX] if len(column) >= PRAGMA_TABLE_XINFO_MIN_LENGTH else 0
            if hidden == 1:
                continue

            is_primary_key = column[PRAGMA_TABLE_INFO_PRIMARY_KEY_INDEX] > 0
            objects[object_name].columns[column[PRAGMA_TABLE_INFO_NAME_INDEX]] = Column(
                doc="",
                data_type=column[PRAGMA_TABLE_INFO_TYPE_INDEX] or "",
                is_nullable=(False if is_primary_key else not bool(column[PRAGMA_TABLE_INFO_NOT_NULL_INDEX])),
            )

    return objects
