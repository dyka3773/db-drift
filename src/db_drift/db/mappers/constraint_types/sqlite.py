from db_drift.db.mappers.constraint_types.base import DictConstraintTypeMapper
from db_drift.utils.constants import DBConstraintType

SQLITE_CONSTRAINT_MAPPER = DictConstraintTypeMapper(
    mapping={
        "PRIMARY KEY": DBConstraintType.PRIMARY_KEY,
        "FOREIGN KEY": DBConstraintType.FOREIGN_KEY,
        "UNIQUE": DBConstraintType.UNIQUE,
        "CHECK": DBConstraintType.CHECK,
        "NOT NULL": DBConstraintType.NOT_NULL,
    },
)
