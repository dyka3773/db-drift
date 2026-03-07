import sqlite3
from pathlib import Path

from db_drift.db.connectors.sqlite import SQLiteConnector
from db_drift.db.strategies.sqlite import fetch_sqlite_indexes, fetch_sqlite_tables, fetch_sqlite_triggers, fetch_sqlite_views
from db_drift.models.column import Column
from db_drift.models.index import Index
from db_drift.models.table import Table
from db_drift.models.trigger import Trigger
from db_drift.models.view import View
from db_drift.utils.string import hash_body


def test_sqlite_connector_registers_expected_object_fetchers() -> None:
    connector = SQLiteConnector(":memory:")

    assert set(connector.SUPPORTED_OBJECTS_REGISTRY.keys()) == {"indexes", "tables", "triggers", "views"}


def test_fetch_sqlite_tables_maps_rows_to_table_models() -> None:
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.executescript(
        """
        CREATE TABLE employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            salary REAL,
            hired_on TEXT DEFAULT CURRENT_DATE
        );
        """,
    )

    tables = fetch_sqlite_tables(cursor)

    assert tables == {
        "employees": Table(
            doc="",
            columns={
                "employee_id": Column(doc="", data_type="INTEGER", is_nullable=False),
                "name": Column(doc="", data_type="TEXT", is_nullable=False),
                "salary": Column(doc="", data_type="REAL", is_nullable=True),
                "hired_on": Column(doc="", data_type="TEXT", is_nullable=True),
            },
        ),
    }
    assert "sqlite_sequence" not in tables


def test_fetch_sqlite_views_maps_rows_to_view_models() -> None:
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.executescript(
        """
        CREATE TABLE employees (
            employee_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            salary REAL
        );

        CREATE VIEW employee_directory AS
        SELECT employee_id, name, salary
        FROM employees;
        """,
    )

    views = fetch_sqlite_views(cursor)

    assert views == {
        "employee_directory": View(
            doc="",
            columns={
                "employee_id": Column(doc="", data_type="INTEGER", is_nullable=True),
                "name": Column(doc="", data_type="TEXT", is_nullable=True),
                "salary": Column(doc="", data_type="REAL", is_nullable=True),
            },
        ),
    }


def test_fetch_sqlite_indexes_maps_rows_to_index_models() -> None:
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.executescript(
        """
        CREATE TABLE employees (
            employee_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department_id INTEGER
        );

        CREATE UNIQUE INDEX employees_email_uq
        ON employees (email);

        CREATE INDEX employees_department_name_ix
        ON employees (department_id, name);
        """,
    )

    indexes = fetch_sqlite_indexes(cursor)

    assert indexes == {
        "employees_department_name_ix": Index(
            table_name="employees",
            uniqueness="NONUNIQUE",
            columns={"department_id", "name"},
        ),
        "employees_email_uq": Index(
            table_name="employees",
            uniqueness="UNIQUE",
            columns={"email"},
        ),
    }


def test_fetch_sqlite_triggers_maps_rows_to_trigger_models() -> None:
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.executescript(
        """
        CREATE TABLE employees (
            employee_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            updated_at TEXT
        );

        CREATE TRIGGER employees_touch_updated_at
        AFTER UPDATE ON employees
        FOR EACH ROW
        BEGIN
            UPDATE employees
            SET updated_at = CURRENT_TIMESTAMP
            WHERE employee_id = NEW.employee_id;
        END;
        """,
    )

    triggers = fetch_sqlite_triggers(cursor)

    trigger_sql = next(
        row[0]
        for row in connection.execute(
            "SELECT sql FROM sqlite_master WHERE type = 'trigger' AND name = 'employees_touch_updated_at'",
        )
    )

    assert triggers == {
        "employees_touch_updated_at": Trigger(
            body=hash_body(trigger_sql),
            definition="table: employees",
        ),
    }


def test_sqlite_connector_fetch_schema_structure_returns_triggers(tmp_path: Path) -> None:
    database_path = tmp_path / "sqlite_trigger_test.db"
    setup_connection = sqlite3.connect(database_path)
    setup_connection.executescript(
        """
        CREATE TABLE employees (
            employee_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            updated_at TEXT
        );

        CREATE TRIGGER employees_touch_updated_at
        AFTER UPDATE ON employees
        FOR EACH ROW
        BEGIN
            UPDATE employees
            SET updated_at = CURRENT_TIMESTAMP
            WHERE employee_id = NEW.employee_id;
        END;

        CREATE UNIQUE INDEX employees_name_uq
        ON employees (name);

        CREATE VIEW employee_directory AS
        SELECT employee_id, name, updated_at
        FROM employees;
        """,
    )
    setup_connection.commit()
    setup_connection.close()

    connector = SQLiteConnector(str(database_path))
    schema = connector.fetch_schema_structure()

    assert set(schema.keys()) == {"indexes", "tables", "triggers", "views"}
    assert "employees_name_uq" in schema["indexes"]
    assert "employees" in schema["tables"]
    assert "employees_touch_updated_at" in schema["triggers"]
    assert "employee_directory" in schema["views"]
