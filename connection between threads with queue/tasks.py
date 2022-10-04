from dataclasses import dataclass
from typing import Callable


@dataclass
class Task:
    name: str
    action: Callable
    source: str

end_task = Task("Stop Working", lambda:True, "Main Thread")
