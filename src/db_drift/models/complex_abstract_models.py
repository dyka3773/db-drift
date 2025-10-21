from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObject
from db_drift.models.column import Column


@dataclass
class DatabaseObjectWithColumns(DatabaseObject):
    """Database object that contains columns (tables, views, etc.)."""

    columns: dict[str, Column]


@dataclass
class DatabaseObjectIndexLike(DatabaseObjectWithColumns):
    """Base class for index-like objects (indexes, constraints)."""

    table_name: str
