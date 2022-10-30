from enum import Enum
from dataclasses import dataclass
import datetime


@dataclass
class Task:
    operator: str
    parameter: int
    time_of_hold: datetime.datetime


class Packet_Headers(Enum):
    INIT = 0
    TASK = 1
    ANS = 2
    END = 3
