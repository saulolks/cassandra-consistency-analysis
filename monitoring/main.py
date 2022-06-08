#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sauloferreira

args:
1. mode: command used to monitor (ps or top)
2. interval: interval in seconds to monitor
3. duration: total duration of test
3. container id: name or identifier of docker container

example: python read_processes.py top 10 200 cas1
"""

import argparse
from json.tool import main
import datetime
import os
import pandas as pd
import sys
import time
import threading
from src.container_monitor import ContainerMonitor

from src.process_monitor import ProcessMonitor

# -----------------------------------------------------------------------


def write_to_csv(data: pd.DataFrame, directory: str, filename: str) -> dict:
    directory = directory + ("/" if directory and directory[:-1] != "/" else "")
    data.to_csv(f"{directory}{filename}.csv")


def monitor_processes(mode, interval, duration, container_ids, start_at, directory):
    process_monitor = ProcessMonitor(mode, container_ids)

    while True:
        print("Collecting process data at:", datetime.datetime.now())
        process_monitor.collect()

        now = datetime.datetime.now()
        if (now - start_at).total_seconds() > duration:
            break

        time.sleep(interval)

    for container_id in container_ids:
        container_dir = f"{directory}/{container_id}"
        if not os.path.exists(container_dir):
            os.mkdir(container_dir)

        data = process_monitor.get_data(container_id=container_id)
        write_to_csv(data, container_dir, "processes_report")


def monitor_containers(interval, duration, start_at, directory, container_ids=[]):
    container_monitor = ContainerMonitor(container_ids)

    while True:
        print("Collecting container data at:", datetime.datetime.now())
        container_monitor.collect()

        now = datetime.datetime.now()
        if (now - start_at).total_seconds() > duration:
            break

        time.sleep(interval)

    for container_id in container_ids:
        container_dir = f"{directory}/{container_id}"
        if not os.path.exists(container_dir):
            os.mkdir(container_dir)

        data = container_monitor.get_data(container_id=container_id)
        write_to_csv(data, container_dir, "container_report")


def run_monitoring(mode, interval, duration, container_ids):
    dir = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")
    dir = f"results/{dir}"
    os.mkdir(dir)
    print("Start monitoring. Save data in folder: " + dir)

    start_at = datetime.datetime.now()
    processes_thread = threading.Thread(
        target=monitor_processes, args=(mode, interval, duration, container_ids, start_at, dir)
    )
    monitor_thread = threading.Thread(
        target=monitor_containers, args=(interval, duration, start_at, dir, container_ids)
    )

    processes_thread.start()
    monitor_thread.start()

    while processes_thread.is_alive() or monitor_thread.is_alive():
        time.sleep(1)

    print("Monitoring finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Containers Monitor", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--mode", help="Mode to read processes (ps or top)", default="top")
    parser.add_argument("--interval", help="Interval to read processes (in seconds)", type=int, default=1)
    parser.add_argument("--duration", help="Total duration of the monitoring (in seconds)", type=int, default=10)
    parser.add_argument(
        "--container-ids",
        help="Container ids to monitor (default: all the active ones)",
        nargs="+",
        default=[],
    )

    args = parser.parse_args()
    config = vars(args)

    mode = config["mode"]
    interval = config["interval"]
    duration = config["duration"]
    container_ids = config["container_ids"]

    run_monitoring(mode, interval, duration, container_ids)
