import sqlite3 as sql  # noqa: INP001

CREATE_DB_TABLES = """
    CREATE TABLE IF NOT EXISTS regions (
        region_id INTEGER PRIMARY KEY,
        region_name TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS countries (
        country_id INTEGER PRIMARY KEY,
        country_name TEXT NOT NULL,
        region_id INTEGER,
        FOREIGN KEY (region_id) REFERENCES regions (region_id)
    );

CREATE TABLE IF NOT EXISTS locations (
        location_id INTEGER PRIMARY KEY,
        street_address TEXT,
        postal_code TEXT,
        city TEXT NOT NULL,
        state_province TEXT,
        country_id INTEGER,
        FOREIGN KEY (country_id) REFERENCES countries (country_id)
    );

CREATE TABLE IF NOT EXISTS departments (
        department_id INTEGER PRIMARY KEY,
        department_name TEXT NOT NULL,
        manager_id INTEGER,
        location_id INTEGER,
        FOREIGN KEY (location_id) REFERENCES locations (location_id)
    );

CREATE TABLE IF NOT EXISTS jobs (
        job_id INTEGER PRIMARY KEY,
        job_title TEXT NOT NULL,
        min_salary REAL,
        max_salary REAL
    );

CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone_number TEXT,
        hire_date TEXT NOT NULL,
        job_id INTEGER,
        salary REAL,
        manager_id INTEGER,
        department_id INTEGER,
        FOREIGN KEY (job_id) REFERENCES jobs (job_id),
        FOREIGN KEY (department_id) REFERENCES departments (department_id)
    );

    CREATE TABLE IF NOT EXISTS job_history (
        employee_id INTEGER,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        job_id INTEGER,
        department_id INTEGER,
        PRIMARY KEY (employee_id, start_date),
        FOREIGN KEY (employee_id) REFERENCES employees (employee_id),
        FOREIGN KEY (job_id) REFERENCES jobs (job_id),
        FOREIGN KEY (department_id) REFERENCES departments (department_id)
    );
"""

UPDATE_DB_TABLES = """
    ALTER TABLE employees ADD COLUMN date_of_birth TEXT;
    ALTER TABLE employees ADD COLUMN gender TEXT;
"""


def create_database(db_name: str, create_tables_sql: str, update_tables_sql: str = None) -> None:
    conn = sql.connect(db_name)
    cursor = conn.cursor()
    cursor.executescript(create_tables_sql)
    if update_tables_sql:
        cursor.executescript(update_tables_sql)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database("example1.db", CREATE_DB_TABLES)
    create_database("example2.db", CREATE_DB_TABLES, UPDATE_DB_TABLES)
    print("Databases 'example1.db' and 'example2.db' created successfully.")  # noqa: T201
