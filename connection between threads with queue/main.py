from queue import Queue

from worker import Worker
from tasker import Tasker
from tasks import end_task

NUM_OF_TASKERS = 1
NUM_OF_WORKERS = 10
NUM_OF_TASKS = 10
NUM_OF_ITERATIONS = 1


def main() -> None:
    task_queue = Queue()
    workers = []
    taskers = []

    # creating workers
    for i in range(1, NUM_OF_WORKERS + 1):
        new_worker = Worker(name=f"Worker {i}", task_queue=task_queue)
        workers.append(new_worker)

    # creating the taskers
    for i in range(1, NUM_OF_TASKERS + 1):
        new_tasker = Tasker(name=f"Tasker {i}", task_queue=task_queue,
                            number_of_tasks=NUM_OF_TASKS, number_of_iterations=NUM_OF_ITERATIONS)
        taskers.append(new_tasker)

    # starting the threads
    for tasker in taskers:
        tasker.start()
    for worker in workers:
        worker.start()

    # waiting for the taskers to end and then telling the workers to stop too
    for tasker in taskers:
        tasker.join()
    task_queue.put(end_task)

    for worker in workers:
        worker.join()


if __name__ == "__main__":
    main()
