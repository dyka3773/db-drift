import sqlite3
from pathlib import Path

from db_drift.db.connectors.sqlite import SQLiteConnector
from db_drift.db.strategies.sqlite import fetch_sqlite_indexes, fetch_sqlite_triggers
from db_drift.models.index import Index
from db_drift.models.trigger import Trigger
from db_drift.utils.string import hash_body


def test_sqlite_connector_registers_expected_object_fetchers() -> None:
    connector = SQLiteConnector(":memory:")

    assert set(connector.SUPPORTED_OBJECTS_REGISTRY.keys()) == {"indexes", "triggers"}


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
        """,
    )
    setup_connection.commit()
    setup_connection.close()

    connector = SQLiteConnector(str(database_path))
    schema = connector.fetch_schema_structure()

    assert set(schema.keys()) == {"indexes", "triggers"}
    assert "employees_name_uq" in schema["indexes"]
    assert "employees_touch_updated_at" in schema["triggers"]
