from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObjectWithDefinition


@dataclass
class Type(DatabaseObjectWithDefinition): ...


# Type inherits all attributes from DatabaseObjectWithDefinition
# which includes:
# - name: str
# - definition: str

# NOTE: Type's definition IS EXPECTED to be hashed
