from abc import ABC, abstractmethod


class BaseDBConnector(ABC):
    """Abstract base class for database connectors."""

    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string
        # Initialize the database connection here in subclasses

    @abstractmethod
    def fetch_schema_structure(self) -> dict:
        """
        Fetch the database schema structure.

        This method should be implemented by subclasses to return
        the schema structure of the connected database.

        Returns:
            dict: A dictionary representing the database schema structure.
        """
        msg = "Subclasses must implement this method."
        raise NotImplementedError(msg)
