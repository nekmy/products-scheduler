from enum import Enum, auto


class JobType(Enum):
    ROOT = auto()
    PROJECT = auto()
    TASK = auto()
