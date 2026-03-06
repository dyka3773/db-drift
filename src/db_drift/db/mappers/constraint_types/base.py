from abc import ABC, abstractmethod
from dataclasses import dataclass

from db_drift.utils.constants import DBConstraintType


class ConstraintTypeMapper(ABC):
    @abstractmethod
    def map(self, native_value: str) -> DBConstraintType:
        raise NotImplementedError


@dataclass(frozen=True)
class DictConstraintTypeMapper(ConstraintTypeMapper):
    mapping: dict[str, DBConstraintType]

    def map(self, native_value: str) -> str:
        key = native_value.strip().upper()
        try:
            return self.mapping[key].value
        except KeyError as exc:
            msg = f"Unsupported constraint type: {native_value!r}"
            raise ValueError(msg) from exc
