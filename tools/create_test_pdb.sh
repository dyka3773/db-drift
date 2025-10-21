#!/usr/bin/env bash
# Simple helper to create a test PDB inside the project's Oracle container

set -euo pipefail

CONTAINER=${1:-oracle-db}
PDB_NAME=${2:-TESTPDB}
PDB_ADMIN=${3:-testadmin}
PDB_PASS=${4:-admin}
DATAFILE_DIR="/opt/oracle/oradata/XE/${PDB_NAME}"

echo "Creating PDB ${PDB_NAME} in container ${CONTAINER} with admin ${PDB_ADMIN}"

docker exec -i "${CONTAINER}" bash -lc "sqlplus -s / as sysdba <<'SQL'
SET ECHO ON
CREATE PLUGGABLE DATABASE ${PDB_NAME} ADMIN USER ${PDB_ADMIN} IDENTIFIED BY ${PDB_PASS} ROLES=(DBA) DEFAULT TABLESPACE users DATAFILE '${DATAFILE_DIR}/users01.dbf' SIZE 50M FILE_NAME_CONVERT=('/opt/oracle/oradata/XE/pdbseed','${DATAFILE_DIR}');
ALTER PLUGGABLE DATABASE ${PDB_NAME} SAVE STATE;
ALTER PLUGGABLE DATABASE ${PDB_NAME} OPEN;
ALTER PLUGGABLE DATABASE ${PDB_NAME} SAVE STATE;
EXIT
SQL"

echo "Done. To connect from the host:"
echo "  sqlplus ${PDB_ADMIN}/${PDB_PASS}@//localhost:1521/${PDB_NAME}"

exit 0
