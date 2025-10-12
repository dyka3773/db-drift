from enum import Enum, unique


@unique
class ExitCode(Enum):
    SUCCESS = 0
    GENERAL_ERROR = 1
    USAGE_ERROR = 2
    UNAVAILABLE = 69
    NO_PERMISSION = 77
    CONFIG_ERROR = 78
    SIGINT = 130
