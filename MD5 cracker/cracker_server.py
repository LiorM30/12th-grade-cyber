import argparse
import logging
import datetime
import socket
from typing import Dict, Any, Tuple, List
from dataclasses import dataclass


core_wait_time = 5


@dataclass
class Range_Task:
    ID: int
    time_of_hold: datetime.datetime
    ranges: list[Tuple[int, int]]


class cracker_Server:
    def __init__(self, port: int, local: bool, combinations_per_client: int) -> None:
        self._port = port
        self._combinations_per_client = combinations_per_client

        self._used_IDs: List[int] = []
        self._ranges_tasks: Dict[int, Range_Task] = {}
        self._unhandled_range: Tuple[int, int] = []

        self._sock = socket.socket()
        if local:
            self._sock.bind("127.0.0.1", self._port)
        else:
            self._sock.bind(socket.gethostname(), self._port)

        self.logger = logging.getLogger('root')

    def _get_unused_ID(self) -> int:
        """
        get an unused task ID

        :return: an ID that isnt used by other tasks
        :rtype: int
        """

        current_ID = 0
        while current_ID in self._used_IDs:
            current_ID += 1

        return current_ID

    def _get_task(self, cores: int) -> Range_Task:
        """
        returns a range task to send to a client based on the
        number of cores the client can use.

        additionally, removes the range from the unhandled range.

        :param cores: the number of cores the client has
        :type cores: int
        :return: the range task
        :rtype: Range_Task
        """

        new_ID = self._get_unused_ID()
        self._used_IDs.append(new_ID)
        ranges = []
        for IDs, task in self._ranges_tasks.items():
            dt = datetime.datetime.now() - task.time_of_hold
            if dt >= datetime.timedelta(seconds=core_wait_time) and \
                    len(ranges) < cores:
                # task took too long
                ranges.append(task.ranges)

    def run(self):
        pass


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--log-level', action='store', type=int, default=20,
        help='Log level (50=Critical, 40=Error, 30=Warning ,20=Info ,10=Debug, 0=None)'  # noqa
    )
    parser.add_argument(
        '--combinations', '-c', action='store', type=int, default=500,
        help='The number of combinations a client can do per core'
    )
    parser.add_argument(
        '--local', '-l', action='store_true',
        help='Whether to run the server on local host'
    )

    args: Dict[str, Any] = parser.parse_args()

    logging.basicConfig(
        level=args.log_level,
        format='[%(asctime)s.%(msecs)03d]: %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
    )

    logging.getLogger('root').addHandler(logging.FileHandler('exercise_log.log'))  # noqa

    server = cracker_Server(16166, args.local, args.combinations)
    server.run()


if __name__ == "__main__":
    main()
