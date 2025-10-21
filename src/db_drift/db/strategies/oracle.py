from oracledb import cursor
from sqlalchemy import Row

from db_drift.models.table import Table
from db_drift.models.view import View


def fetch_oracle_tables(cursor: cursor.Cursor) -> list[Table]:
    """
    Fetch the list of tables from the Oracle database available to the connected user.

    Args:
        cursor (cursor.Cursor): The Oracle database cursor.

    Returns:
        list[Table]: A list of Table objects representing the tables in the database.
    """
    rows = _get_table_like_obj_list("TABLE", cursor)
    tables = [
        Table(
            name=f"{row[2]}.{row[0]}",
            doc=row[1],
            columns=[],
        )
        for row in rows
    ]

    # TODO @dyka3773: Fetch columns for each table and populate the 'columns' attribute
    return tables  # noqa: RET504


def fetch_oracle_views(cursor: cursor.Cursor) -> list[View]:
    """
    Fetch the list of views from the Oracle database available to the connected user.

    Args:
        cursor (cursor.Cursor): The Oracle database cursor.

    Returns:
        list[View]: A list of View objects representing the views in the database.
    """
    rows = _get_table_like_obj_list("VIEW", cursor)
    views = [
        View(
            name=f"{row[2]}.{row[0]}",
            doc=row[1],
            columns=[],
        )
        for row in rows
    ]

    # TODO @dyka3773: Fetch columns for each view and populate the 'columns' attribute
    return views  # noqa: RET504


def _get_table_like_obj_list(obj: str, cursor: cursor.Cursor) -> list[Row]:
    """
    Fetch table-like objects (tables, views) from the Oracle database.

    Args:
        obj (str): The type of object to fetch ("TABLE" or "VIEW").
        cursor (cursor.Cursor): The Oracle database cursor.

    Returns:
        list: A list of Table or View objects.
    """
    select_obj_comments = f"""
        SELECT
            table_name,
            comments,
            owner
        FROM all_tab_comments
        WHERE table_name NOT LIKE '%$%'
            AND table_type = '{obj}'
            AND owner NOT IN (
                SELECT DISTINCT username
                FROM all_users
                WHERE ORACLE_MAINTAINED = 'Y'
            )
        ORDER BY owner, table_name
    """
    cursor.execute(select_obj_comments)
    return cursor.fetchall()
