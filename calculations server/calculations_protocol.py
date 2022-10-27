from enum import Enum
from dataclasses import dataclass
from typing import List


@dataclass
class Task:
    number: str
    parameter: int


@dataclass
class Init_Packet:
    numbers: List[int]
