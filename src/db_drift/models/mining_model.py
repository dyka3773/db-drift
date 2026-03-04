from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObjectWithDefinition


@dataclass
class MiningModel(DatabaseObjectWithDefinition): ...


# MiningModel inherits all attributes from DatabaseObjectWithDefinition
# which includes:
# - definition: str
