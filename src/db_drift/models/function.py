from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObjectWithHashedBody


@dataclass
class Function(DatabaseObjectWithHashedBody): ...


# Function inherits all attributes from DatabaseObjectWithHashableBody
# which includes:
# - name: str
# - body: str
# - definition: str
# NOTE: body is expected to be hashed
