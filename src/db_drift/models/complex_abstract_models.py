from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObject
from db_drift.models.column import Column


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
