from dataclasses import dataclass

from db_drift.models.complex_abstract_models import DatabaseObjectIndexLike
from db_drift.utils.constants import DBConstraintTypeEnum


@dataclass
class Constraint(DatabaseObjectIndexLike):
    constraint_type: DBConstraintTypeEnum | str
    rule: str | None = None  # For FOREIGN KEY constraints
    condition: str | None = None  # For CHECK constraints
