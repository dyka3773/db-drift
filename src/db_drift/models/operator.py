from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObjectWithDoc


@dataclass
class Operator(DatabaseObjectWithDoc):
    """Represents a database operator with comprehensive metadata."""


# Operator inherits all attributes from DatabaseObjectWithDoc,
# which includes:
# - doc: str
