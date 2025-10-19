## Creating a test PDB in the project's Oracle Docker container

This guide explains how to create a test Pluggable Database (PDB) inside the Oracle XE container used by this project.
It assumes you have the same setup as the repository: the Oracle service is defined in `tools/docker-compose.yml` and runs as `oracle-db` with the environment variable `ORACLE_PWD` set.

Prerequisites
- Docker and Docker Compose (or Docker Desktop) installed and running on your machine
- The repository checked out and your working directory at the repository root
- The Oracle container started via the provided compose file:

```sh
docker compose -f tools/docker-compose.yml up -d --build oracle-db
```

Steps

1. Confirm the container is running

```sh
docker ps --filter name=oracle-db
```

2. Create a PDB from the seed

The container ships with `pdbseed`; you can clone that to make a test PDB. The example below creates a PDB named `TESTPDB` and a PDB-local admin user `testadmin` with password `admin`.

```sh
docker exec -it oracle-db bash -lc "sqlplus -s / as sysdba <<'SQL'
CREATE PLUGGABLE DATABASE TESTPDB
  ADMIN USER testadmin IDENTIFIED BY admin
  ROLES=(DBA)
  DEFAULT TABLESPACE users
  DATAFILE '/opt/oracle/oradata/XE/TESTPDB/users01.dbf' SIZE 50M
  FILE_NAME_CONVERT=('/opt/oracle/oradata/XE/pdbseed','/opt/oracle/oradata/XE/TESTPDB');
ALTER PLUGGABLE DATABASE TESTPDB SAVE STATE;
ALTER PLUGGABLE DATABASE TESTPDB OPEN;
EXIT
SQL"
```

Notes
- If you prefer different names/sizes/passwords, edit the CREATE PLUGGABLE DATABASE command accordingly.
- The example maps `pdbseed` to `/opt/oracle/oradata/XE/TESTPDB`. If your image or data locations differ, update the `FILE_NAME_CONVERT` and `DATAFILE` path.

3. Verify the PDB

Run the following to see the PDB list and open modes:

```sh
docker exec -it oracle-db bash -lc "echo 'SELECT NAME, OPEN_MODE FROM V\$PDBS;' | sqlplus -s / as sysdba"
```

4. Connect to the new PDB as the PDB-local admin

From a client (on the host), use the connection string with the PDB service name:

```sh
sqlplus testadmin/admin@//localhost:1521/TESTPDB
```

Troubleshooting
- If SQL*Plus returns ORA-65019 (already open) when opening the PDB, it's already open and ready to use.
- If `V$PDBS` or other dictionary views return ORA-00942 in non-interactive runs, try running SQL*Plus interactively inside the container:

```sh
docker exec -it oracle-db bash
sqlplus / as sysdba
-- then run: SELECT NAME, OPEN_MODE FROM V$PDBS;
```

Automation
- See `tools/create_test_pdb.sh` for a small helper script to create a PDB with configurable name and admin credentials.

Safety
- The script clones `pdbseed`. It is safe for creating disposable test PDBs but not intended for production provisioning.
