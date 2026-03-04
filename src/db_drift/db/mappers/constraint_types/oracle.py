from db_drift.db.mappers.constraint_types.base import DictConstraintTypeMapper
from db_drift.utils.constants import DBConstraintType

ORACLE_CONSTRAINT_MAPPER = DictConstraintTypeMapper(
    mapping={
        "P": DBConstraintType.PRIMARY_KEY,
        "R": DBConstraintType.FOREIGN_KEY,
        "U": DBConstraintType.UNIQUE,
        "C": DBConstraintType.CHECK,
        "O": DBConstraintType.READ_ONLY,
        "V": DBConstraintType.CHECK_OPTION,
    },
)
