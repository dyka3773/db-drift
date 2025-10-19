from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObjectWithHashedBody


@dataclass
class StoredProcedure(DatabaseObjectWithHashedBody): ...


# StoredProcedure inherits all attributes from DatabaseObjectWithHashedBody
# which includes:
# - name: str
# - body: str
# - definition: str
# NOTE: body is expected to be hashed
