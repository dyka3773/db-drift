from oracledb import cursor
from sqlalchemy import Row

from db_drift.models.column import Column
from db_drift.models.edition import Edition
from db_drift.models.indextype import IndexType
from db_drift.models.materialized_view import MaterializedView
from db_drift.models.mining_model import MiningModel
from db_drift.models.operator import Operator
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
                data_type=col[4],  # TODO @dyka3773: Add length/precision info from col[6] if needed  # noqa: FIX002
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
                data_type=col[4],  # TODO @dyka3773: Add length/precision info from col[6] if needed  # noqa: FIX002
                is_nullable=(col[5] == "Y"),  # Oracle uses 'Y'/'N' for nullable
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
    select_obj = f"""
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
    cursor.execute(select_obj)
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


def fetch_oracle_materialized_views(cursor: cursor.Cursor) -> dict[str, MaterializedView]:
    """
    Fetch the list of materialized views from the Oracle database available to the connected user.

    Args:
        cursor (cursor.Cursor): The Oracle database cursor.

    Returns:
        dict[str, MaterializedView]: A dictionary of MaterializedView objects representing the materialized views in the database.
    """
    select_mv = """
        SELECT
            mview_name,
            comments,
            owner
        FROM all_mview_comments
        WHERE mview_name NOT LIKE '%$%'
            AND owner NOT IN (
                SELECT DISTINCT username
                FROM all_users
                WHERE ORACLE_MAINTAINED = 'Y'
            )
        ORDER BY owner, mview_name
    """
    cursor.execute(select_mv)
    mv_rows = cursor.fetchall()
    mviews: dict[str, MaterializedView] = {
        f"{row[2]}.{row[0]}": MaterializedView(
            doc=row[1],
            columns={},  # Initialize empty columns dict
        )
        for row in mv_rows
    }

    select_mv_columns = """
        SELECT table_name, column_name, comments, owner
        FROM all_col_comments
        WHERE table_name IN (
            SELECT mview_name
            FROM all_mviews
            WHERE mview_name NOT LIKE '%$%'
                AND owner NOT IN (
                    SELECT DISTINCT username
                    FROM all_users
                    WHERE ORACLE_MAINTAINED = 'Y'
                )
        )
        ORDER BY owner, table_name, column_name
    """

    cursor.execute(select_mv_columns)
    mv_column_rows = cursor.fetchall()

    for col in mv_column_rows:
        mv_name = f"{col[3]}.{col[0]}"
        # This assumes that all columns belong to fetched materialized views and skips others
        if mv_name in mviews:
            mviews[mv_name].columns[col[1]] = Column(
                doc=col[2],
                data_type="",  # Data type info not fetched here
                is_nullable=None,  # Nullability info not fetched here
            )

    return mviews


def fetch_oracle_editions(cursor: cursor.Cursor) -> dict[str, Edition]:
    """
    Fetch all editions stored in the database available to the user.

    Args:
        cursor (cursor.Cursor): The Oracle database cursor.

    Returns:
        dict[str, Edition]: A dictionary of Edition objects representing the editions in the database.
    """
    select_editions = """
        SELECT
            aec.edition_name,
            aec.comments,
            ae.parent_edition_name
        FROM all_edition_comments aec
        JOIN all_editions ae ON aec.edition_name = ae.edition_name
        WHERE aec.edition_name NOT LIKE '%$%'
        ORDER BY aec.edition_name
    """
    cursor.execute(select_editions)
    edition_rows = cursor.fetchall()
    editions: dict[str, Edition] = {
        row[0]: Edition(
            doc=row[1],
            definition=f"parent_edition_name: {row[2]}" if row[2] else "No parent edition",
        )
        for row in edition_rows
    }

    return editions


def fetch_oracle_mining_models(cursor: cursor.Cursor) -> dict[str, MiningModel]:
    """
    Fetch the list of mining models from the Oracle database available to the connected user.

    Args:
        cursor (cursor.Cursor): The Oracle database cursor.

    Returns:
        dict[str, MiningModel]: A dictionary of MiningModel objects representing the mining models in the database.
    """
    select_models = """
        SELECT
            owner,
            model_name,
            comments,
            algorithm,
            model_size
        FROM all_mining_models
        WHERE model_name NOT LIKE '%$%'
            AND owner NOT IN (
                SELECT DISTINCT username
                FROM all_users
                WHERE ORACLE_MAINTAINED = 'Y'
            )
        ORDER BY owner, model_name
    """
    cursor.execute(select_models)
    model_rows = cursor.fetchall()
    mining_models: dict[str, MiningModel] = {
        f"{row[0]}.{row[1]}": MiningModel(
            doc=row[2],
            definition=f"algorithm: {row[3]}, model_size: {row[4]}",
        )
        for row in model_rows
    }
    return mining_models


def fetch_oracle_indextypes(cursor: cursor.Cursor) -> dict[str, IndexType]:
    """
    Fetch the list of indextypes from the Oracle database available to the connected user.

    Args:
        cursor (cursor.Cursor): The Oracle database cursor.

    Returns:
        dict[str, IndexType]: A dictionary of IndexType objects representing the indextypes in the database.
    """
    select_indextypes = """
        SELECT
            aitc.owner,
            aitc.indextype_name,
            aitc.comments
        FROM all_indextype_comments aitc
        WHERE aitc.indextype_name NOT LIKE '%$%'
            AND aitc.owner NOT IN (
                SELECT DISTINCT username
                FROM all_users
                WHERE ORACLE_MAINTAINED = 'Y'
            )
        ORDER BY aitc.owner, aitc.indextype_name
    """

    cursor.execute(select_indextypes)
    indextype_rows = cursor.fetchall()
    indextypes: dict[str, IndexType] = {
        f"{row[0]}.{row[1]}": IndexType(
            doc=row[2],
        )
        for row in indextype_rows
    }

    return indextypes


def fetch_oracle_operators(cursor: cursor.Cursor) -> dict[str, Operator]:
    """
    Fetch the list of operators from the Oracle database available to the connected user.

    Args:
        cursor (cursor.Cursor): The Oracle database cursor.

    Returns:
        dict[str, Operator]: A dictionary of Operator objects representing the operators in the database.
    """
    select_operators = """
        SELECT
            owner,
            operator_name,
            comments
        FROM all_operator_comments
        WHERE operator_name NOT LIKE '%$%'
            AND owner NOT IN (
                SELECT DISTINCT username
                FROM all_users
                WHERE ORACLE_MAINTAINED = 'Y'
            )
        ORDER BY owner, operator_name
    """

    cursor.execute(select_operators)
    operator_rows = cursor.fetchall()
    operators: dict[str, Operator] = {
        f"{row[0]}.{row[1]}": Operator(
            doc=row[2],
        )
        for row in operator_rows
    }

    return operators
