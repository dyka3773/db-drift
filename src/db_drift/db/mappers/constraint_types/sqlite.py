from db_drift.db.mappers.constraint_types.base import DictConstraintTypeMapper
from db_drift.utils.constants import DBConstraintTypeEnum

SQLITE_CONSTRAINT_MAPPER = DictConstraintTypeMapper(
    mapping={
        "PRIMARY KEY": DBConstraintTypeEnum.PRIMARY_KEY,
        "FOREIGN KEY": DBConstraintTypeEnum.FOREIGN_KEY,
        "UNIQUE": DBConstraintTypeEnum.UNIQUE,
        "CHECK": DBConstraintTypeEnum.CHECK,
        "NOT NULL": DBConstraintTypeEnum.NOT_NULL,
    },
)
