# Currently Supported DB Objects
The following database objects are currently supported (at least partially) by db-drift for comparison and drift detection:
- [x] Tables
- [x] Views
- [x] Materialized Views
- [x] Indexes
- [x] Sequences
- [x] Functions
- [x] Triggers
- [x] Stored Procedures
- [x] Custom Types
- [x] Constraints
- [x] Directories
- [x] Packages/Packages Bodies
- [x] Synonyms
- [x] Editions
- [x] Mining Models
- [x] Custom Operators
- [x] Index Types
- [ ] Audit Policies
- [ ] Scheduler Jobs

## Oracle
The following Oracle object types are currently extracted by `db-drift`:
- [x] Tables
- [x] Views
- [x] Materialized Views
- [x] Indexes
- [x] Sequences
- [x] Functions
- [x] Triggers
- [x] Stored Procedures
- [x] Custom Types
- [x] Constraints
- [x] Directories
- [x] Packages/Packages Bodies
- [x] Synonyms
- [x] Editions
- [x] Mining Models
- [x] Custom Operators
- [x] Index Types
- [ ] Audit Policies
- [ ] Scheduler Jobs

Notes:
- Oracle support is under active development and should be treated as evolving.
- Object-level support does not guarantee complete parity for every object attribute in all Oracle versions/environments.
- See [`docs/oracle-support.md`](oracle-support.md) for implementation details and known caveats.

## SQLite
The following objects are fully supported for SQLite databases:
- [ ] Tables
- [ ] Views
- [ ] Indexes
- [ ] Sequences
- [x] Triggers
- [ ] Custom Types
- [ ] Constraints
- [ ] Directories
- [ ] Packages/Packages Bodies
- [ ] Synonyms
- [ ] Editions
- [ ] Mining Models
- [ ] Custom Operators
- [ ] Index Types
- [ ] Audit Policies
- [ ] Scheduler Jobs