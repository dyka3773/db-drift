from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObjectWithHashedBody


@dataclass
class Trigger(DatabaseObjectWithHashedBody): ...


# Trigger inherits all attributes from DatabaseObjectWithHashedBody
# which includes:
# - body: str
# - definition: str
