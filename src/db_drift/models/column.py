from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObjectWithDoc


@dataclass
class Column(DatabaseObjectWithDoc):
    """Represents a database column with comprehensive metadata."""

    data_type: str
    is_nullable: bool
