from threading import Thread
from queue import Queue
from time import sleep

from tasks import Task, end_task


class Tasker(Thread):
    def __init__(self, name: str, task_queue: Queue[Task], number_of_tasks: int, number_of_iterations: int) -> None:
        super().__init__()

        self.name = name
        self.task_queue = task_queue

        self.number_of_tasks = number_of_tasks
        self.number_of_iterations = number_of_iterations
    

    def run(self) -> None:
        for iteration in range(1, self.number_of_iterations + 1):
            print(f"[{self.name}] on iteration {iteration}")
            for task in range(1, self.number_of_tasks + 1):
                new_task = Task(f"{iteration}.{task} sleep", self._sleep_action, self.name)
                self.task_queue.put(new_task)
            print(f"[{self.name}] sleeping to next iteration")
            sleep(4)
        print(f"[{self.name}] done putting tasks")
    
    
    def _sleep_action(self) -> None:
        sleep(2)
