from queue import Queue
import logging
import argparse
from sys import stdout

from worker import Worker
from tasker import Tasker
from tasks import end_task


def main() -> None:

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--log-level', action='store', type=int, default=20,
        help='Log level (50=Critical, 40=Error, 30=Warning ,20=Info ,10=Debug, 0=None)'  # noqa
    )

    parser.add_argument(
        '--tasker-count', '-tr', action='store', type=int, default=1,
        help='the number of taskers that will run'
    )
    parser.add_argument(
        '--worker-count', '-w', action='store', type=int, default=4,
        help='the number of workers that will run'
    )
    parser.add_argument(
        '--task-count', '-t', action='store', type=int, default=10,
        help='the number of tasks each tasker will distribute'
    )
    parser.add_argument(
        '--iteration-count', '-i', action='store', type=int, default=2,
        help='the number of iterations that every tasker will go through'
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level,
        format='[%(asctime)s.%(msecs)03d]: %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
    )

    logging.getLogger('root').addHandler(logging.StreamHandler(stdout))
    logging.getLogger('root').addHandler(logging.FileHandler('exercise_log.log'))

    logger = logging.getLogger('root')

    task_queue = Queue()
    workers = []
    taskers = []

    # creating workers
    for i in range(1, args.worker_count + 1):
        new_worker = Worker(name=f"Worker {i}", task_queue=task_queue)
        workers.append(new_worker)

    # creating the taskers
    for i in range(1, args.tasker_count + 1):
        new_tasker = Tasker(name=f"Tasker {i}", task_queue=task_queue,
                            number_of_tasks=args.task_count, number_of_iterations=args.iteration_count)
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
