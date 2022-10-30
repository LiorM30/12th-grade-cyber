from asyncio import tasks
from dataclasses import dataclass
import socket
import json
import logging
from threading import Thread
from typing import List, Dict

from calculations_protocol import Task


class Calculations_Server:
    def __init__(self, ip: str, port: int, tasks_path: str) -> None:
        self.ip = ip
        self.port = port
        self.tasks_path = tasks_path

        self.tasks: List[Task] = []

        self._parse_tasks()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(
            (socket.gethostbyname(socket.gethostname()), port)
        )

        self.logger = logging.getLogger('root')

    def _parse_tasks(self) -> None:
        with open(self.tasks_path, 'r') as tasks_file:
            for line in tasks_file:
                par_line = line.split()
                self.tasks.append(Task(number=par_line[0],
                                       parameter=par_line[1]))

    def run(self) -> None:
        # listener_thread = Thread(target=self._listen_continously, args=())
        # listener_thread.start()

        while True:
            if len(self.tasks) > 0:
                self.sock.listen()
                new_cli, addr = self.sock.accept()
                connection_msg: Dict = json.loads(new_cli.recv(1024).decode())

                for task in self.tasks:
                    pass
                    

    def _listen_continously(self) -> None:
        self.sock.listen()

        while True:
            new_cli, addr = self.sock.accept()
            self.clients.append(new_cli)
            connection_msg: Dict = json.loads(new_cli.recv(1024).decode())

    def _handle_client(client: socket.socket) -> None:
        for task in tasks:
            pass
