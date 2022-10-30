import argparse
import logging
from threading import Thread
from typing import List
from time import sleep

from calculations_server import Calculations_Server
from calculations_client import Calculations_Client


def run_client():
    client = Calculations_Client("127.0.0.1", 16666)
    print("test")
    client.add_calculation(
        "1", lambda x: sleep(1)
    )
    client.add_calculation(
        "2", lambda x: sleep(1)
    )
    client.add_calculation(
        "3", lambda x: sleep(1)
    )
    client.add_calculation(
        "4", lambda x: sleep(1)
    )
    client.add_calculation(
        "5", lambda x: sleep(1)
    )
    client.run()


def run_server():
    server = Calculations_Server("127.0.0.1", 16666, "calculations server client\\tasks.txt")
    server.run()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--log-level', action='store', type=int, default=20,
        help='Log level (50=Critical, 40=Error, 30=Warning ,20=Info ,10=Debug, 0=None)'  # noqa
    )

    parser.add_argument(
        '--tasks-path', '-tp', action='store', type=str, default="tasks.txt",
        help='the location of the tasks file'
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level,
        format='[%(asctime)s.%(msecs)03d]: %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
    )

    logging.getLogger('root').addHandler(logging.FileHandler('exercise_log.log'))  # noqa

    logger = logging.getLogger('root')

    server_thread = Thread(target=run_server, args=())
    server_thread.start()
    logger.debug("server created and running")

    sleep(2)
    clients: List[Thread] = []
    for _ in range(3):
        clients.append(Thread(target=run_client, args=()))

    for client in clients:
        client.start()
        logger.debug("all clients are running")

    for client in clients:
        client.join()

    server_thread.join()

    logger.debug("program ended")


if __name__ == "__main__":
    main()
    # TODO fix structure to add the task IDs
    # with open("calculations server client\known_operators.json") as op:
    #     print(json.load(op))
    # a = [1, 2, 3, 4, 5, 6]
    # p = struct.pack('!i', a)
    # print(struct.unpack('!i', p))
    # d = {
    #     "k": 12
    # }
    # d = [     1, 2]

    # print(json.loads(json.dumps(d)))
