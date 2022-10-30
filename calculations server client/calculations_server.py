from dataclasses import dataclass
import socket
import json
import logging
from threading import Thread
from typing import List, Dict, Tuple

from calculations_protocol import Task, Packet_Type


class Calculations_Server:
    def __init__(self, ip: str, port: int, tasks_path: str) -> None:
        self.ip = ip
        self.port = port
        self.tasks_path = tasks_path

        # {
        #   operator: {
        #       ID: task,
        #       ...
        #       },
        #   ...
        # }
        self.tasks_table: Dict[str, Dict[int, Task]] = {}
        self._parse_tasks()

        with open("calculations server client\\known_operators.json") as op:
            self.operators: Dict[str, Dict[str, int]] = json.load(op)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(
            (socket.gethostbyname(socket.gethostname()), port)
        )

        self.logger = logging.getLogger('root')

    def _parse_tasks(self) -> None:
        with open(self.tasks_path, 'r') as tasks_file:
            task_id = 0
            for line in tasks_file:
                par_line = line.split()
                operator = par_line[0]
                parameter = par_line[1]

                self.tasks_table[operator][task_id] = Task(
                    operator=operator, parameter=parameter
                )

                task_id += 1

    def run(self) -> None:
        while not all(len(tasks) == 0 for tasks in self.tasks_table):
            self.sock.listen()
            new_cli, addr = self.sock.accept()
            handler = Thread(target=self._handle_client, args=(new_cli,))
            handler.start()

    def _possible_task(self, possible: Dict[int, str]) -> Task:
        pass

    def _handle_client(self, client: socket.socket) -> None:
        connection_msg: Dict[str, int] = json.loads(client.recv(1024).decode())

        match connection_msg['header']:
            case Packet_Type.INIT:
                if any(connection_msg['operators'] in operators
                       for operators in self.tasks_table.keys()):
                    task: Task = self._possible_task()
                    packet = {
                        'header': Packet_Type.TASK,
                        'operator': task.operator,
                        'parameter': task.parameter
                    }

                    self.tasks_table
                else:
                    packet = {
                        'header': Packet_Type.END
                    }
            case Packet_Type.ANS:
                pass

        client.send(json.dumps(packet).encode())
        client.close()
