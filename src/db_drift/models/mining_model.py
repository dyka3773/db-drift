from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObjectWithDefinitionAndDoc


@dataclass
class MiningModel(DatabaseObjectWithDefinitionAndDoc): ...


# MiningModel inherits all attributes from DatabaseObjectWithDefinitionAndDoc
# which includes:
# - definition: str
# - doc: str
