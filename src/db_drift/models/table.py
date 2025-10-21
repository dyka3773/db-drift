from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObjectWithDoc
from db_drift.models.complex_abstract_models import DatabaseObjectWithColumns


@dataclass
class Table(
    DatabaseObjectWithDoc,
    DatabaseObjectWithColumns,
): ...


# Table inherits all attributes from DatabaseObjectWithColumns
# which includes:
# - name: str
# - columns: list[Column]
