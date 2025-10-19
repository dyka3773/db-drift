from dataclasses import dataclass

from db_drift.models.abstract_models import DatabaseObjectWithColumns


@dataclass
class Table(DatabaseObjectWithColumns): ...


# Table inherits all attributes from DatabaseObjectWithColumns
# which includes:
# - name: str
# - columns: list[Column]
