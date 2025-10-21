from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObjectWithHashedBody


@dataclass
class Package(DatabaseObjectWithHashedBody): ...


# Package inherits all attributes from DatabaseObjectWithHashedBody
# which includes:
# - body: str
# - definition: str

# NOTE: Package's body AND definition are both expected to be hashed
