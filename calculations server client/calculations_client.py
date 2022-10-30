import json
import socket
import logging
from typing import Callable
from time import sleep
import argparse

from calculations_protocol import Packet_Headers


class Calculations_Client:
    def __init__(self, server_ip: str, server_port: int) -> None:
        self.server_ip = server_ip
        self.server_port = server_port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.calculations = {}

        self.logger = logging.getLogger('root')

    def run(self):
        continue_running = True

        self.sock.connect((self.server_ip, self.server_port))
        self.logger.debug("connected to server")

        self.sock.send(json.dumps(
            {
                'header': Packet_Headers.INIT.value,
                'operators': list(self.calculations.keys())
            }
        ).encode())
        self.logger.debug("sent INIT packet")

        while continue_running:

            packet = json.loads(self.sock.recv(1024).decode())
            header = packet['header']

            if header == Packet_Headers.TASK.value:
                self.logger.debug("recieved TASK packet")
                id = packet['id']
                operator = packet['operator']
                parameter = packet['parameter']

                self.sock.close()
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                self.logger.debug(f"starting to calculate: {operator}")
                answer = self.calculations[operator](parameter)
                self.logger.debug(f"finished calculating: {operator}")

                answer_pack = {
                    'header': Packet_Headers.ANS.value,
                    'task id': id,
                    'operator': operator,
                    'answer': answer
                }

                self.sock.connect((self.server_ip, self.server_port))
                self.logger.debug("connected to server")
                self.sock.send(json.dumps(answer_pack).encode())
                self.logger.debug("sent ANS packet")

            elif header == Packet_Headers.END.value:
                self.logger.debug("got END packet")
                continue_running = False

    def add_calculation(self,
                        operator: str, calculation: Callable[[int], int]
                        ) -> None:
        self.calculations[operator] = calculation
        self.logger.debug(f"added calculation {operator}")


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

    client = Calculations_Client("127.0.0.1", 16166)
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


if __name__ == "__main__":
    main()
