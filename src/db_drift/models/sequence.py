from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObjectWithDefinition


@dataclass
class Sequence(DatabaseObjectWithDefinition): ...


# Sequence inherits all attributes from DatabaseObjectWithDefinition
