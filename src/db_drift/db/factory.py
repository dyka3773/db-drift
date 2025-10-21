from collections.abc import Callable

from db_drift.db.connectors.base_connector import BaseDBConnector
from db_drift.utils.constants import SUPPORTED_DBMS_REGISTRY


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
    if dbms not in SUPPORTED_DBMS_REGISTRY:
        # This should not happen due to argparse choices, but we double-check here.
        msg = f"Unsupported DBMS type: {dbms}"
        raise ValueError(msg)

    return SUPPORTED_DBMS_REGISTRY[dbms]
