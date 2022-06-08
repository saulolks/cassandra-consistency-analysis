from dotenv import dotenv_values, load_dotenv
from numpy import number
from src.monitor import Monitor
import datetime
import docker
import os
import psutil

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
    "container_name",
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
    "container_name",
]


class ProcessMonitor(Monitor):
    def __init__(self, mode: str, container_names: list) -> None:
        self._data = dict((i, []) for i in PS_HEADERS) if mode == "ps" else dict((i, []) for i in TOP_HEADERS)
        self.mode = mode
        self._client = docker.from_env()
        self._containers = self._get_containers_info(container_names)
        self._total_system_memory = self._get_system_total_memory()

        self._config = dotenv_values("./config/.env")

    def collect(self) -> None:
        for container_name in self._containers.keys():
            timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S_%f")

            if self.mode == "top":
                output = self._exec_top(container_name)
                self._format_and_save(output, TOP_HEADERS, timestamp, container_name)
            else:
                output = self._exec_ps(container_name)
                self._format_and_save(output, PS_HEADERS, timestamp, container_name)

    def _exec_top(self, container_name: str) -> str:
        command = (
            f"echo '{self._config['SUDO_PASSWORD']}' | sudo -S docker exec "
            + container_name
            + " top -b -n 1 | sed -n '7, 12{s/^ *//;s/ *$//;s/  */,/gp;};12q' | tail -n +2"
        )
        return os.popen(command).read()

    def _exec_ps(self, container_name: str) -> str:
        command = (
            f"echo '{self._config['SUDO_PASSWORD']}' | sudo -S docker exec "
            + container_name
            + ' ps aux | awk \'{print $1 "," $2 "," $3 "," $4 "," $5 "," $6 "," $11}\' | tail -n +2'
        )
        return os.popen(command).read()

    def _format_and_save(self, output: str, headers: list, timestamp: str, container_name: str) -> None:
        for line in output.split("\n")[:-1]:
            self._data["timestamp"].append(str(timestamp))
            self._data["container_name"].append(str(container_name))

            for i, col in enumerate(line.split(",")):
                if headers[i] == "mem":
                    col = self._process_memory_info(col, self._containers[container_name]["memory"])
                self._data[headers[i]].append(col)

    def _get_containers_info(self, container_names) -> dict:
        containers = {}

        if not container_names:
            containers = self._client.containers.list(filters={"status": "running"})
            for container in containers:
                stats = container.stats(decode=False, stream=False)
                containers[container] = {"memory": stats["memory_stats"]["limit"]}
        else:
            for container in container_names:
                aux = self._client.containers.get(container)
                stats = aux.stats(decode=False, stream=False)
                containers[container] = {"memory": stats["memory_stats"]["limit"]}

        return containers

    def _get_system_total_memory(self) -> int:
        return psutil.virtual_memory().total

    def _process_memory_info(self, container_memory_usage, container_memory_limit) -> number:
        return (float(container_memory_usage) * self._total_system_memory) / container_memory_limit
