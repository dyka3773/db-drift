<!-- omit in toc -->
# SQLite Database Example
This directory contains an example setup for using SQLite Database to demonstrate the capabilities of this project.

<!-- omit in toc -->
## Table of Contents
- [Creating the Example Databases](#creating-the-example-databases)
- [Usage](#usage)


## Creating the Example Databases
The script `create_2_example_sqlite_dbs.py` can be run to create 2 example SQLite databases with sample schemas and data to be used with this project.

The internal database structure created by the example SQL files is similar to the one created for the Oracle example and is shown in the [yaml file there](../oracle/db-structure.yml)

## Usage
To use the example databases with this project, simply point the connection strings to the created SQLite database files and specify `--dbms=sqlite` when running the tool.
eg:
```bash
db-drift --source="example1.db" --target="example2.db" --dbms=sqlite
```