<!-- omit in toc -->
# Oracle Database Example
This directory contains an example setup for using Oracle Database to demonstrate the capabilities of this project.

<!-- omit in toc -->
## Table of Contents
- [SQL](#sql)
- [Internal Database Structure](#internal-database-structure)
- [Usage](#usage)


## SQL
The folder `SQL` contains 4 example SQL migration files that can be applied to an Oracle database using this project to create a sample schema with tables, indexes, and data.
It is the HR example database shipped by Oracle themselves.

## Internal Database Structure
The tool's internal database structure created by the example SQL files is shown in the [yaml file here](./db-structure.yml)

## Usage
To use this example, ensure you have an Oracle Database instance running and accessible.
You can then run the tool with the appropriate connection strings pointing to your Oracle Database instance.
eg:
```bash
db-drift --source="testadmin/admin@localhost:1521/testpdb" --target="testadmin/admin@localhost:1521/testpdb" --dbms=oracle
```