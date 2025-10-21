from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObjectWithDefinition


@dataclass
class Type(DatabaseObjectWithDefinition): ...


# Type inherits all attributes from DatabaseObjectWithDefinition
# which includes:
# - definition: str

# NOTE: Type's definition IS EXPECTED to be hashed
