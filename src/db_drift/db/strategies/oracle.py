from oracledb import cursor
from sqlalchemy import Row

from db_drift.models.column import Column
from db_drift.models.table import Table
from db_drift.models.view import View


def fetch_oracle_tables(cursor: cursor.Cursor) -> dict[str, Table]:
    """
    Fetch the list of tables from the Oracle database available to the connected user.

    Args:
        cursor (cursor.Cursor): The Oracle database cursor.

    Returns:
        list[Table]: A list of Table objects representing the tables in the database.
    """
    table_rows = _get_table_like_obj_list("TABLE", cursor)
    tables: dict[str, Table] = {
        f"{row[2]}.{row[0]}": Table(
            doc=row[1],
            columns={},  # Initialize empty columns dict
        )
        for row in table_rows
    }

    column_rows = _get_column_list("TABLE", cursor)
    for col in column_rows:
        table_name = f"{col[3]}.{col[0]}"
        # This assumes that all columns belong to fetched tables and skips others
        if table_name in tables:
            tables[table_name].columns[col[1]] = Column(
                doc=col[2],
                data_type=col[4],  # TODO @dyka3773: Add length/precision info from col[6] if needed
                is_nullable=(col[5] == "Y"),  # Oracle uses 'Y'/'N' for nullable
            )

    return tables


def fetch_oracle_views(cursor: cursor.Cursor) -> dict[str, View]:
    """
    Fetch the list of views from the Oracle database available to the connected user.

    Args:
        cursor (cursor.Cursor): The Oracle database cursor.

    Returns:
        list[View]: A list of View objects representing the views in the database.
    """
    view_rows = _get_table_like_obj_list("VIEW", cursor)
    views: dict[str, View] = {
        f"{row[2]}.{row[0]}": View(
            doc=row[1],
            columns={},  # Initialize empty columns dict
        )
        for row in view_rows
    }

    column_rows = _get_column_list("VIEW", cursor)
    for col in column_rows:
        view_name = f"{col[3]}.{col[0]}"
        # This assumes that all columns belong to fetched views and skips others
        if view_name in views:
            views[view_name].columns[col[1]] = Column(
                doc=col[2],
                data_type=col[4],  # TODO @dyka3773: Add length/precision info from col[6] if needed
                is_nullable=(col[5] == "Y"),  # Oracle uses 'Y'
            )

    return views


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


def _get_column_list(object_type: str, cursor: cursor.Cursor) -> list[Row]:
    """
    Fetch columns for a given object type from the Oracle database.

    Args:
        object_type (str): The type of object to fetch columns for ("TABLE" or "VIEW").
        cursor (cursor.Cursor): The Oracle database cursor.

    Returns:
        list: A list of columns for the specified object type.
    """
    select_columns = f"""
        SELECT
            atcc.table_name,
            atcc.column_name,
            atcc.comments,
            atcc.owner,
            atc.data_type,
            atc.nullable,
            atc.data_length
        FROM all_col_comments atcc
        JOIN all_tab_columns atc
            ON atcc.table_name = atc.table_name
            AND atcc.column_name = atc.column_name
            AND atcc.owner = atc.owner
        WHERE atcc.table_name IN (
            SELECT DISTINCT table_name
            FROM all_catalog
            WHERE table_type = '{object_type}'
                AND table_name NOT LIKE '%$%'
                AND owner NOT IN (
                    SELECT DISTINCT username
                    FROM all_users
                    WHERE ORACLE_MAINTAINED = 'Y'
                )
        )
        ORDER BY atcc.owner, atcc.table_name, atcc.column_name
    """
    cursor.execute(select_columns)
    return cursor.fetchall()
