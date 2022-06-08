import datetime
import docker
import psutil
from src.monitor import Monitor

DOCKER_STATS_HEADERS = [
    "container_name",
    "cpu_per",
    "mem_usage",
    "mem_per",
    "block_read",
    "block_write",
    "pids",
    "timestamp",
]


class ContainerMonitor(Monitor):
    bytes_converter = {
        "B": 1,
        "KB": 1024,
        "MB": 1024**2,
        "GB": 1024**3,
    }

    def __init__(self, container_names=[]) -> None:
        self._data = dict((i, []) for i in DOCKER_STATS_HEADERS)
        self._client = docker.from_env()

        if not container_names:
            self._containers = self._client.containers.list(filters={"status": "running"})
        else:
            self._containers = [self._client.containers.get(id) for id in container_names]

    def collect(self) -> None:
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        for container in self._containers:
            stats = container.stats(decode=False, stream=False)
            self._format_and_save(stats, timestamp)

    def _format_and_save(self, stats: dict, timestamp: str) -> None:
        self._data["container_name"].append(stats["name"].replace("/", ""))
        self._data["cpu_per"].append(stats["cpu_stats"]["cpu_usage"]["total_usage"])
        self._data["mem_usage"].append(stats["memory_stats"]["usage"])
        self._data["mem_per"].append(100 * (stats["memory_stats"]["usage"] / stats["memory_stats"]["limit"]))
        self._data["block_read"].append(
            self._process_block_io(stats["blkio_stats"]["io_service_bytes_recursive"][0]["value"])
        )
        self._data["block_write"].append(
            self._process_block_io(stats["blkio_stats"]["io_service_bytes_recursive"][1]["value"])
        )
        self._data["pids"].append(stats["pids_stats"]["current"])
        self._data["timestamp"].append(timestamp)

    def _process_block_io(self, data: int) -> float:
        return data / self.bytes_converter["MB"]
