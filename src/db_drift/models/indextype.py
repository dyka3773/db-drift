from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObjectWithDoc


@dataclass
class IndexType(DatabaseObjectWithDoc):
    """Represents a database index type with comprehensive metadata."""


# IndexType inherits all attributes from DatabaseObjectWithDoc,
# which includes:
# - doc: str
