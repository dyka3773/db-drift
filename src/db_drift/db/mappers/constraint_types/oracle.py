from db_drift.db.mappers.constraint_types.base import DictConstraintTypeMapper
from db_drift.utils.constants import DBConstraintTypeEnum

ORACLE_CONSTRAINT_MAPPER = DictConstraintTypeMapper(
    mapping={
        "P": DBConstraintTypeEnum.PRIMARY_KEY,
        "R": DBConstraintTypeEnum.FOREIGN_KEY,
        "U": DBConstraintTypeEnum.UNIQUE,
        "C": DBConstraintTypeEnum.CHECK,
        "O": DBConstraintTypeEnum.READ_ONLY,
        "V": DBConstraintTypeEnum.CHECK_OPTION,
    },
)
