import oracledb

from db_drift.db.connectors.base_connector import BaseDBConnector
from db_drift.db.strategies.oracle import (
    fetch_oracle_editions,
    fetch_oracle_indexes,
    fetch_oracle_indextypes,
    fetch_oracle_materialized_views,
    fetch_oracle_mining_models,
    fetch_oracle_operators,
    fetch_oracle_tables,
    fetch_oracle_triggers,
    fetch_oracle_views,
)


class OracleConnector(BaseDBConnector):
    def __init__(self, connection_string: str) -> None:
        """
        Initialize the OracleConnector with a connection string.

        Args:
            connection_string (str): The connection string for the Oracle database.
        """
        super().__init__(connection_string)

        self.SUPPORTED_OBJECTS_REGISTRY = {
            "tables": fetch_oracle_tables,
            "views": fetch_oracle_views,
            "materialized_views": fetch_oracle_materialized_views,
            "editions": fetch_oracle_editions,
            "mining_models": fetch_oracle_mining_models,
            "indextypes": fetch_oracle_indextypes,
            "operators": fetch_oracle_operators,
            "triggers": fetch_oracle_triggers,
            "indexes": fetch_oracle_indexes,
            # "constraints": fetch_oracle_constraints,  # noqa: ERA001
            # "sequences": fetch_oracle_sequences,  # noqa: ERA001
            # "synonyms": fetch_oracle_synonyms,  # noqa: ERA001
            # "functions": fetch_oracle_functions,  # noqa: ERA001
            # "procedures": fetch_oracle_procedures,  # noqa: ERA001
            # "packages": fetch_oracle_packages,  # noqa: ERA001
            # "types": fetch_oracle_types,  # noqa: ERA001
            # "jobs": fetch_oracle_jobs,  # noqa: ERA001
            # "directories": fetch_oracle_directories,  # noqa: ERA001
        }

        self.connection_library = oracledb
