from threading import Thread
from queue import Queue
import logging

from tasks import Task, end_task


class Worker(Thread):
    def __init__(self, name: str, task_queue: Queue[Task]) -> None:
        super().__init__()

        self.logger = logging.getLogger('root')

        self.name = name
        self.task_queue = task_queue


    def run(self) -> None:
        while True:
            current_task = self.task_queue.get()

            # reached the end of the queue and the tasker will no longer put new tasks in the queue
            if current_task == end_task:
                self.task_queue.put(current_task)
                break

            self.logger.info(f"[{self.name}] starting task: {current_task.name} from {current_task.source}")
            current_task.action()

        self.logger.info(f"[{self.name} done]")

