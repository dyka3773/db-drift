<!-- omit in toc -->
# Oracle Support (Work in Progress)

Oracle support is available in `db-drift`, but it is still under heavy development.
This page documents what currently exists so users can set the right expectations.

<!-- omit in toc -->
## Table of Contents
- [Current Scope](#current-scope)
- [How Oracle Is Enabled](#how-oracle-is-enabled)
- [Connection String](#connection-string)
- [Known Gaps and Caveats](#known-gaps-and-caveats)
- [Quick Example](#quick-example)
- [Related Docs](#related-docs)

## Current Scope

At the moment, the Oracle connector is wired to fetch and compare the following object groups:

- Tables
- Views
- Materialized Views
- Editions
- Mining Models
- Index Types
- Operators
- Triggers
- Indexes
- Constraints
- Sequences
- Synonyms
- Functions
- Stored Procedures
- Packages
- Types
- Directories

Planned but not implemented in the Oracle registry yet:

- Scheduler Jobs
- Audit Policies

## How Oracle Is Enabled

Oracle support is provided through:

- `src/db_drift/db/connectors/oracle.py`
- `src/db_drift/db/strategies/oracle.py`
- `src/db_drift/utils/constants.py` (`get_supported_dbms_registry`)

CLI usage:

```bash
db-drift --dbms oracle --source "<source-conn-str>" --target "<target-conn-str>"
```

## Connection String

`db-drift` passes the connection string directly to `python-oracledb`.
A practical format is:

```text
user/password@host:port/service_name
```

Example used in this repository docs:

```text
testadmin/admin@localhost:1521/testpdb
```

## Known Gaps and Caveats

Oracle support should currently be treated as best-effort, not complete parity.
Important caveats:

- Some metadata fields are intentionally incomplete today.
  Materialized view columns are fetched without data type and nullability details.
- Column length and precision are not fully modeled for all object flows yet.
- Queries intentionally skip Oracle-maintained users and many system-style objects.
  This helps reduce noise, but it can hide objects you may expect in a full inventory.
- Object support is broad, but behavior can still vary across Oracle versions, privileges, and environment setup.

## Quick Example

```bash
db-drift \
  --dbms oracle \
  --source "testadmin/admin@localhost:1521/testpdb" \
  --target "testadmin/admin@localhost:1521/testpdb" \
  --output "oracle_drift_report.html"
```

## Related Docs

- `docs/supported-db-objects.md`
- `examples/oracle/README.md`
- `docs/create_test_pdb.md`
