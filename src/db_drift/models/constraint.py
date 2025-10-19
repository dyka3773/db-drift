from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObjectIndexLike
from db_drift.utils.constants import DBConstraintType


@dataclass
class Constraint(DatabaseObjectIndexLike):
    constraint_type: DBConstraintType
    rule: str | None = None  # For FOREIGN KEY constraints
    condition: str | None = None  # For CHECK constraints
