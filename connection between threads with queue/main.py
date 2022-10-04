from queue import Queue
from threading import Thread
from time import sleep

from worker import Worker
from tasks import Task, end_task

NUM_OF_WORKERS = 4
NUM_OF_TASKS = 10
NUM_OF_ITERATIONS = 2


def default_task_action() -> None:
    sleep(2)


def tasking(task_queue: Queue) -> None:
    for iteration in range(1, NUM_OF_ITERATIONS + 1):
        print(f"on iteration {iteration}")
        for task in range(1, NUM_OF_TASKS + 1):
            new_task = Task(f"{iteration}.{task} def", default_task_action)
            task_queue.put(new_task)
        print("sleeping to next iteration")
        sleep(5)
    print("done putting tasks")
    task_queue.put(end_task)


def main() -> None:
    task_queue = Queue()
    workers = []

    # creating workers
    for i in range(1, NUM_OF_WORKERS + 1):
        new_worker = Worker(name=f"Worker {i}", task_queue=task_queue)
        workers.append(new_worker)

    # initializing the tasker
    tasker = Thread(name="Tasker", target=tasking, args=(task_queue,))

    # starting the threads
    tasker.start()
    for worker in workers:
        worker.start()

    tasker.join()
    for worker in workers:
        worker.join()


if __name__ == "__main__":
    main()
