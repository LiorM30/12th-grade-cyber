from dataclasses import dataclass
from typing import Callable


@dataclass
class Task:
    name: str
    action: Callable

end_task = Task("stop working", lambda:True)
