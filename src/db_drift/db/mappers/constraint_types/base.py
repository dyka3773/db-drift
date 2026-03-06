from abc import ABC, abstractmethod
from dataclasses import dataclass

from db_drift.utils.constants import DBConstraintTypeEnum


class ConstraintTypeMapper(ABC):
    @abstractmethod
    def map(self, native_value: str) -> DBConstraintTypeEnum | str:
        raise NotImplementedError


@dataclass(frozen=True)
class DictConstraintTypeMapper(ConstraintTypeMapper):
    mapping: dict[str, DBConstraintTypeEnum]

    def map(self, native_value: str) -> DBConstraintTypeEnum | str:
        key = native_value.strip().upper()
        try:
            return self.mapping[key]
        except KeyError:
            return native_value
