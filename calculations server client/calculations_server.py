import socket
import json
import logging
from threading import Thread
from typing import Dict, Tuple, List
import datetime
import argparse
import os

from calculations_protocol import Task, Packet_Headers


class Calculations_Server:
    def __init__(self, ip: str, port: int, tasks_path: str) -> None:
        self.ip = ip
        self.port = port
        self.tasks_path = tasks_path
        self.logger = logging.getLogger('root')

        # {
        #   operator: {
        #       ID: task,
        #       ...
        #       },
        #   ...
        # }
        self.tasks_table: Dict[str, Dict[int, Task]] = {}
        self._parse_tasks()
        self.logger.debug("parsed tasks")

        self.client_cache: Dict[str, List[str]] = {}

        file_dir = os.path.dirname(__file__)
        file_path = os.path.join(file_dir, ".\\known_operators.json")
        with open(file_path) as op:
            self.operators: Dict[str, Dict[str, int]] = json.load(op)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(
            (self.ip, port)
        )

        self.answers = []

    def _parse_tasks(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), self.tasks_path), 'r') as tasks_file:
            task_id = 0
            for line in tasks_file:
                par_line = line.split()
                operator = par_line[0]
                parameter = par_line[1]

                if operator in self.tasks_table:
                    self.tasks_table[operator][task_id] = Task(
                        operator=operator
                        parameter=parameter,
                        time_of_hold=None
                    )
                else:
                    self.tasks_table[operator] = {}
                    self.tasks_table[operator][task_id] = Task(
                        operator=operator,
                        parameter=parameter,
                        time_of_hold=None
                    )

                task_id += 1

    def run(self) -> None:
        while not all(len(tasks) == 0 for operators, tasks in self.tasks_table.items()):
            self.sock.listen(1)
            self.logger.debug("listening")
            new_cli, addr = self.sock.accept()
            self.logger.debug("new client")
            handler = Thread(target=self._handle_client, args=(new_cli,))
            handler.start()

        self.logger.info(self.answers)

    def _possible_task(self,
                       possible_operators: List[str]) -> Tuple[int, Task]:
        """
        returns an unhandled task and its id.
        also resets tasks with hold times above the defined ones.
        """
        for operator, tasks in self.tasks_table.items():
            self.logger.debug(tasks)
            if operator not in possible_operators or len(tasks) == 0:
                # has no tastks with the operator or
                # all the tasks with the operator are done
                next

            for id, task in tasks.items():
                if task.time_of_hold:
                    now = datetime.datetime.now()
                    delta = (now - task.time_of_hold).total_seconds()
                    out_of_date = delta >= self.operators[operator]['min time']

                    # the selected task has been on hold for too long
                    if out_of_date:
                        return (id, task)
                else:
                    return (id, task)

        return (None, None)

    def _handle_client(self, client: socket.socket) -> None:
        self.logger.debug(self.client_cache)

        connection_msg: Dict[str, int] = json.loads(client.recv(1024).decode())
        self.logger.debug(f'connection message: {connection_msg}')
        client_ip = client.getpeername()[0]

        match connection_msg['header']:
            case Packet_Headers.INIT.value:
                self.logger.debug("init packet")

                # adding the client to the client "cache"
                self.client_cache[client_ip] = connection_msg['operators']

                task_id, task = self._possible_task(connection_msg['operators'])

                if task:
                    packet = {
                        'header': Packet_Headers.TASK.value,
                        'id': task_id,
                        'operator': task.operator,
                        'parameter': task.parameter
                    }

                    self.tasks_table[task.operator][task_id].time_of_hold = datetime.datetime.now()  # noqa

                else:
                    self.logger.debug('client has no operators of use after INIT')
                    self.logger.debug('sent END packet')
                    # as no task for the client
                    packet = {
                        'header': Packet_Headers.END.value
                    }

            case Packet_Headers.ANS.value:
                self.logger.debug("ans packet")

                ans_operator = connection_msg['operator']
                answer = connection_msg['answer']
                ans_id = connection_msg['task id']
                self.answers.append(
                    (ans_operator, answer)
                )

                # got the answer for the task -> remove the task
                self.tasks_table[ans_operator].pop(ans_id, None)

                # self.logger.debug(self._possible_task(self.client_cache[client_ip]))
                # self.logger.debug(f"items: {self.tasks_table.items()}")

                task_id, task = self._possible_task(self.client_cache[client_ip])

                if task:
                    #  if there is another task avalible for the client
                    packet = {
                        'header': Packet_Headers.TASK.value,
                        'id': task_id,
                        'operator': task.operator,
                        'parameter': task.parameter
                    }

                    # renewing the hold
                    self.tasks_table[task.operator][task_id].time_of_hold = datetime.datetime.now()  # noqa

                else:
                    self.logger.debug("client has no operators of use")
                    self.logger.debug("sent end packet")
                    # client has no more tasks avalible
                    packet = {
                        'header': Packet_Headers.END.value
                    }

        # sends the packet and closes the connection
        client.send(json.dumps(packet).encode())
        self.logger.debug(f'sent to client: {packet}')
        client.close()
        self.logger.debug("closed client")


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

    server = Calculations_Server("127.0.0.1", 16166,
                                 "tasks.txt")
    server.run()


if __name__ == "__main__":
    main()
