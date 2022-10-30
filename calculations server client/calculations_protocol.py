from enum import Enum
from dataclasses import dataclass


@dataclass
class Task:
    operator: str
    parameter: int
    time_on_hold: int


class Packet_Type(Enum):
    INIT = 0
    TASK = 1
    ANS = 2
    END = 3
