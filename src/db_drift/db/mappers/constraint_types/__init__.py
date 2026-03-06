from db_drift.db.mappers.constraint_types.base import ConstraintTypeMapper
from db_drift.db.mappers.constraint_types.oracle import ORACLE_CONSTRAINT_MAPPER
from db_drift.db.mappers.constraint_types.sqlite import SQLITE_CONSTRAINT_MAPPER
from db_drift.utils.constants import DBConstraintTypeEnum

CONSTRAINT_MAPPER_REGISTRY: dict[str, ConstraintTypeMapper] = {
    "oracle": ORACLE_CONSTRAINT_MAPPER,
    "sqlite": SQLITE_CONSTRAINT_MAPPER,
}


def map_constraint_type(dbms: str, native_value: str) -> DBConstraintTypeEnum | str:
    mapper = CONSTRAINT_MAPPER_REGISTRY[dbms.lower()]
    return mapper.map(native_value)
