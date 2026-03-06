import os
from unittest.mock import Mock, patch

import pytest
from db_drift.db.connectors.oracle import OracleConnector
from db_drift.db.strategies.oracle import fetch_oracle_tables, fetch_oracle_views
from db_drift.models.column import Column

ORACLE_TEST_CONN_ENV_VAR = "DB_DRIFT_ORACLE_TEST_CONN_STRING"


@pytest.fixture(scope="module")
def oracle_connector_from_env() -> OracleConnector:
    conn_str = os.getenv(ORACLE_TEST_CONN_ENV_VAR)
    if not conn_str:
        pytest.skip(
            "Oracle integration tests require DB_DRIFT_ORACLE_TEST_CONN_STRING; they are skipped in CI when Oracle credentials are unavailable.",
        )

    return OracleConnector(conn_str)


@pytest.fixture(scope="module")
def oracle_schema_from_env(oracle_connector_from_env: OracleConnector) -> dict:
    return oracle_connector_from_env.fetch_schema_structure()


def test_oracle_connector_registers_expected_object_fetchers() -> None:
    connector = OracleConnector("user/password@localhost:1521/testpdb")

    expected_keys = {
        "tables",
        "views",
        "materialized_views",
        "editions",
        "mining_models",
        "indextypes",
        "operators",
        "triggers",
        "indexes",
        "constraints",
        "sequences",
        "synonyms",
        "functions",
        "procedures",
        "packages",
        "types",
        "directories",
    }

    assert set(connector.SUPPORTED_OBJECTS_REGISTRY.keys()) == expected_keys


def test_oracle_connector_fetch_schema_structure_executes_registered_fetchers() -> None:
    connector = OracleConnector("user/password@localhost:1521/testpdb")
    fetch_tables = Mock(return_value={"HR.EMPLOYEES": Mock()})
    fetch_views = Mock(return_value={"HR.ACTIVE_EMPLOYEES": Mock()})
    connector.SUPPORTED_OBJECTS_REGISTRY = {
        "tables": fetch_tables,
        "views": fetch_views,
    }

    mock_cursor = Mock()
    mock_connection = Mock()
    mock_connection.cursor.return_value = mock_cursor

    with patch.object(connector.connection_library, "connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_connection

        schema = connector.fetch_schema_structure()

    fetch_tables.assert_called_once_with(mock_cursor)
    fetch_views.assert_called_once_with(mock_cursor)
    assert set(schema.keys()) == {"tables", "views"}


def test_fetch_oracle_tables_maps_rows_to_table_models() -> None:
    cursor = Mock()
    table_rows = [
        ("EMPLOYEES", "Employee table", "HR"),
    ]
    column_rows = [
        ("EMPLOYEES", "EMPLOYEE_ID", "PK", "HR", "NUMBER", "N", 22),
        ("EMPLOYEES", "NAME", "Full name", "HR", "VARCHAR2", "Y", 200),
        ("NOT_FETCHED", "IGNORED", "ignored", "HR", "VARCHAR2", "Y", 10),
    ]
    cursor.fetchall.side_effect = [table_rows, column_rows]

    tables = fetch_oracle_tables(cursor)

    assert list(tables.keys()) == ["HR.EMPLOYEES"]
    assert tables["HR.EMPLOYEES"].doc == "Employee table"
    assert tables["HR.EMPLOYEES"].columns["EMPLOYEE_ID"] == Column(
        doc="PK",
        data_type="NUMBER",
        is_nullable=False,
    )
    assert tables["HR.EMPLOYEES"].columns["NAME"] == Column(
        doc="Full name",
        data_type="VARCHAR2",
        is_nullable=True,
    )
    assert "IGNORED" not in tables["HR.EMPLOYEES"].columns


def test_fetch_oracle_views_maps_rows_to_view_models() -> None:
    cursor = Mock()
    view_rows = [
        ("ACTIVE_EMPLOYEES", "Active employees only", "HR"),
    ]
    column_rows = [
        ("ACTIVE_EMPLOYEES", "EMPLOYEE_ID", "PK", "HR", "NUMBER", "N", 22),
    ]
    cursor.fetchall.side_effect = [view_rows, column_rows]

    views = fetch_oracle_views(cursor)

    assert list(views.keys()) == ["HR.ACTIVE_EMPLOYEES"]
    assert views["HR.ACTIVE_EMPLOYEES"].columns["EMPLOYEE_ID"].data_type == "NUMBER"
    assert views["HR.ACTIVE_EMPLOYEES"].columns["EMPLOYEE_ID"].is_nullable is False


@pytest.mark.skipif(
    not os.getenv(ORACLE_TEST_CONN_ENV_VAR),
    reason=(
        "Oracle integration test requires DB_DRIFT_ORACLE_TEST_CONN_STRING; "
        "it is intentionally skipped in CI environments without Oracle credentials."
    ),
)
def test_oracle_connector_can_open_connection_with_env_provided_connection_string() -> None:
    conn_str = os.environ[ORACLE_TEST_CONN_ENV_VAR]
    connector = OracleConnector(conn_str)

    with connector.connection_library.connect(connector.connection_string) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM DUAL")
        row = cursor.fetchone()

    # python-oracledb can return a tuple-like row or scalar depending on cursor settings.
    if isinstance(row, tuple):
        assert row[0] == 1
    else:
        assert row == 1


def test_oracle_schema_extraction_from_env_returns_expected_object_groups(
    oracle_connector_from_env: OracleConnector,
    oracle_schema_from_env: dict,
) -> None:
    assert set(oracle_schema_from_env.keys()) == set(oracle_connector_from_env.SUPPORTED_OBJECTS_REGISTRY.keys())
    assert all(isinstance(extracted_group, dict) for extracted_group in oracle_schema_from_env.values())


def test_oracle_schema_extraction_is_stable_across_repeated_calls(
    oracle_connector_from_env: OracleConnector,
    oracle_schema_from_env: dict,
) -> None:
    first_counts = {group_name: len(group_data) for group_name, group_data in oracle_schema_from_env.items()}

    second_schema = oracle_connector_from_env.fetch_schema_structure()
    second_counts = {group_name: len(group_data) for group_name, group_data in second_schema.items()}

    assert first_counts == second_counts


def test_oracle_table_extraction_has_well_formed_table_keys_and_columns_when_available(
    oracle_schema_from_env: dict,
) -> None:
    extracted_tables = oracle_schema_from_env["tables"]
    if not extracted_tables:
        pytest.skip("No user tables were visible in the Oracle schema for this integration run.")

    table_key, table_model = next(iter(extracted_tables.items()))

    assert "." in table_key
    assert isinstance(table_model.columns, dict)

    if not table_model.columns:
        pytest.skip(f"Table {table_key} had no extracted columns in this environment.")

    _, first_column = next(iter(table_model.columns.items()))
    assert isinstance(first_column.data_type, str)
    assert first_column.data_type != ""
    assert isinstance(first_column.is_nullable, bool)
