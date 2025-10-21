class BaseDBConnector:
    """Abstract base class for database connectors."""

    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string
        self.SUPPORTED_OBJECTS_REGISTRY = {}
        self.schema_structure: dict = {}
        self.connection_library = None  # This will be set in subclasses
        # Initialize the database connection here in subclasses

    def fetch_schema_structure(self) -> dict:
        """
        Fetch the database schema structure for the specific DBMS.

        Returns:
            dict: A dictionary representing the database schema structure.
        """
        with self.connection_library.connect(self.connection_string) as connection:
            cursor = connection.cursor()

            for obj_type, fetch_function in self.SUPPORTED_OBJECTS_REGISTRY.items():
                self.schema_structure[obj_type] = fetch_function(cursor)

        return self.schema_structure
