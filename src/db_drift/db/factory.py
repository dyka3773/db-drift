from collections.abc import Callable

from db_drift.db.connectors.base_connector import BaseDBConnector
from db_drift.utils.constants import get_supported_dbms_registry


def get_connector(dbms: str) -> Callable[[str], BaseDBConnector]:
    """
    Get the appropriate DB connector class based on the DBMS type.
    Factory function pattern.

    Args:
        dbms (str): The type of DBMS (e.g., 'sqlite', 'postgresql', 'mysql', 'oracle').

    Returns:
        Callable[[str], BaseDBConnector]: A callable that takes a connection string and returns a DB connector instance.

    Raises:
        ValueError: If the specified DBMS is not supported.
    """
    supported_dbms_registry = get_supported_dbms_registry()

    if dbms not in supported_dbms_registry:
        # This should not happen due to argparse choices, but we double-check here.
        msg = f"Unsupported DBMS type: {dbms}"
        raise ValueError(msg)

    return supported_dbms_registry[dbms]
