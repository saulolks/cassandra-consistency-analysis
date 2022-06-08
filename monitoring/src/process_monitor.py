import datetime
import os
from dotenv import dotenv_values, load_dotenv
import pandas as pd


TOP_HEADERS = [
    "pid",
    "user",
    "pr",
    "ni",
    "virt",
    "res",
    "shr",
    "s",
    "cpu",
    "mem",
    "time",
    "command",
    "timestamp",
    "container_id",
]
PS_HEADERS = [
    "user",
    "pid",
    "cpu",
    "mem",
    "vsz",
    "rss",
    "command",
    "timestamp",
    "container_id",
]


class ProcessMonitor:
    def __init__(self, mode: str, container_ids: list) -> None:
        self._data = dict((i, []) for i in PS_HEADERS) if mode == "ps" else dict((i, []) for i in TOP_HEADERS)
        self.mode = mode
        self.container_ids = container_ids

        self._config = dotenv_values("./config/.env")
        print(self._config)

    def collect(self) -> None:
        for container_id in self.container_ids:
            timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S_%f")

            if self.mode == "top":
                output = self._exec_top(container_id)
                self._format_and_save(output, TOP_HEADERS, timestamp, container_id)
            else:
                output = self._exec_ps(container_id)
                self._format_and_save(output, PS_HEADERS, timestamp, container_id)

    def _exec_top(self, container_id: str) -> str:
        command = (
            f"echo '{self._config['SUDO_PASSWORD']}' | sudo -S docker exec "
            + container_id
            + " top -b -n 1 | sed -n '7, 12{s/^ *//;s/ *$//;s/  */,/gp;};12q' | tail -n +2"
        )
        return os.popen(command).read()

    def _exec_ps(self, container_id: str) -> str:
        command = (
            f"echo '{self._config['SUDO_PASSWORD']}' | sudo -S docker exec "
            + container_id
            + ' ps aux | awk \'{print $1 "," $2 "," $3 "," $4 "," $5 "," $6 "," $11}\' | tail -n +2'
        )
        print(command)
        return os.popen(command).read()

    def _format_and_save(self, output: str, headers: list, timestamp: str, container_id: str) -> None:
        for line in output.split("\n")[:-1]:
            self._data["timestamp"].append(str(timestamp))
            self._data["container_id"].append(str(container_id))

            for i, col in enumerate(line.split(",")):
                self._data[headers[i]].append(col)

    def get_data(self, container_id=None) -> dict:
        data = pd.DataFrame(self._data)

        if container_id:
            data = data[(data["container_id"] == container_id)]

        return data
