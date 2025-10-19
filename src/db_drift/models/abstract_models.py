from dataclasses import dataclass

from db_drift.models.column import Column


@dataclass
class DatabaseObject:
    """Base class for all database objects."""

    name: str


@dataclass
class DatabaseObjectWithDoc(DatabaseObject):
    """Database object that can have documentation/comments."""

    doc: str = ""


@dataclass
class DatabaseObjectWithHashedBody(DatabaseObject):
    """Database object with executable code (functions, procedures, etc.)."""

    body: str  # body is expected to be hashed
    definition: str  # definition may not be hashed


@dataclass
class DatabaseObjectWithDefinition(DatabaseObject):
    """Database object defined by a simple definition string."""

    definition: str


@dataclass
class DatabaseObjectWithColumns(DatabaseObject):
    """Database object that contains columns (tables, views, etc.)."""

    columns: list[Column]

    def __post_init__(self) -> None:
        """Validate the object after initialization."""
        super().__post_init__()
        if not isinstance(self.columns, list):
            msg = "Columns must be a list"
            raise TypeError(msg)


@dataclass
class DatabaseObjectIndexLike(DatabaseObjectWithColumns):
    """Base class for index-like objects (indexes, constraints)."""

    table_name: str
