from enum import Enum, unique


@unique
class ExitCode(Enum):
    SUCCESS = 0
    GENERAL_ERROR = 1
    USAGE_ERROR = 2
    DATA_ERROR = 65
    NO_INPUT = 66
    UNAVAILABLE = 69
    SOFTWARE_ERROR = 70
    NO_PERMISSION = 77
    CONFIG_ERROR = 78
    SIGINT = 130


SUPPORTED_DBMS: list[str] = [
    # "postgresql",
    # "mysql",
    "sqlite",
    # "oracle",
]
