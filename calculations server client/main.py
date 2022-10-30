import argparse
import json
import logging
import struct
from threading import Thread
from sys import stdout
from typing import List

from calculations_server import Calculations_Server
from calculations_client import Calculations_Client


def run_client():
    client = Calculations_Client()
    client.run()


def run_server():
    server = Calculations_Server()
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

    parser.add_argument(
        '--answers-path', '-ap', action='store', type=str, default="answers.txt",  # noqa
        help='the location of the answers file'
    )

    parser.add_argument(
        '--local', '-l', action='store_true', type=bool,
        help='whether to run the clients locally'
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level,
        format='[%(asctime)s.%(msecs)03d]: %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
    )

    logging.getLogger('root').addHandler(logging.StreamHandler(stdout))
    logging.getLogger('root').addHandler(logging.FileHandler('exercise_log.log'))  # noqa

    logger = logging.getLogger('root')

    if args.local:
        server_thread = Thread(targert=run_server, args=())
        server_thread.start()
        logger.debug("server created and running")

        clients: List[Thread] = []
        for _ in range(3):
            clients.append(Thread(target=run_client, args=()))

        for client in clients:
            client.start()
            logger.debug("all clients are running")

        for client in clients:
            client.join()

        server_thread.join()

    else:
        run_server()

    logger.debug("program ended")


if __name__ == "__main__":
    main()
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
