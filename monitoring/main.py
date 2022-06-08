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


from src.monitoring_plotter import MonitoringPlotter
from src.container_monitor import ContainerMonitor
from src.process_monitor import ProcessMonitor
import argparse
import datetime
import os
import pandas as pd
import threading
import time

# -----------------------------------------------------------------------


def write_to_csv(data: pd.DataFrame, directory: str, filename: str) -> dict:
    directory = directory + ("/" if directory and directory[:-1] != "/" else "")
    data.to_csv(f"{directory}{filename}.csv")


def monitor_processes(mode, interval, duration, container_names, start_at, directory):
    process_monitor = ProcessMonitor(mode, container_names)

    while True:
        print("Collecting process data at:", datetime.datetime.now())
        process_monitor.collect()

        now = datetime.datetime.now()
        if (now - start_at).total_seconds() > duration:
            break

        time.sleep(interval)

    for container_name in container_names:
        container_dir = f"{directory}/{container_name}"
        if not os.path.exists(container_dir):
            os.mkdir(container_dir)

        data = process_monitor.get_data(container_name=container_name)
        write_to_csv(data, container_dir, "processes_report")


def monitor_containers(interval, duration, start_at, directory, container_names=[]):
    container_monitor = ContainerMonitor(container_names)

    while True:
        print("Collecting container data at:", datetime.datetime.now())
        container_monitor.collect()

        now = datetime.datetime.now()
        if (now - start_at).total_seconds() > duration:
            break

        time.sleep(interval)

    for container_name in container_names:
        container_dir = f"{directory}/{container_name}"
        if not os.path.exists(container_dir):
            os.mkdir(container_dir)

        data = container_monitor.get_data(container_name=container_name)
        write_to_csv(data, container_dir, "container_report")


def generate_charts(directory, container_names):
    plotter = MonitoringPlotter()

    for container in container_names:
        container_chart_dir = f"{directory}/{container}/charts"
        os.mkdir(container_chart_dir)

        container_report_filename = f"{directory}/{container}/container_report.csv"
        process_report_filename = f"{directory}/{container}/processes_report.csv"

        process_df = pd.read_csv(process_report_filename)
        container_df = pd.read_csv(container_report_filename)

        plotter.multiline_plot(process_df, "timestamp", ["cpu", "mem"], f"{container_chart_dir}/processes_cpu_mem.png")
        plotter.line_plot(container_df, "timestamp", "mem_per", f"{container_chart_dir}/container_mem.png")


def run(mode, interval, duration, container_names):
    directory = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")
    directory = f"results/{directory}"
    os.mkdir(directory)
    print("Start monitoring. Save data in folder: " + directory)

    start_at = datetime.datetime.now()
    processes_thread = threading.Thread(
        target=monitor_processes, args=(mode, interval, duration, container_names, start_at, directory)
    )
    monitor_thread = threading.Thread(
        target=monitor_containers, args=(interval, duration, start_at, directory, container_names)
    )

    processes_thread.start()
    monitor_thread.start()

    while processes_thread.is_alive() or monitor_thread.is_alive():
        time.sleep(1)

    print("Monitoring finished. Generating charts...")
    generate_charts(directory, container_names)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Containers Monitor", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--mode", help="Mode to read processes (ps or top)", default="top")
    parser.add_argument("--interval", help="Interval to read processes (in seconds)", type=int, default=1)
    parser.add_argument("--duration", help="Total duration of the monitoring (in seconds)", type=int, default=10)
    parser.add_argument(
        "--container-names",
        help="Names of the containers to monitor (default: all the active ones)",
        nargs="+",
        default=[],
    )

    args = parser.parse_args()
    config = vars(args)

    mode = config["mode"]
    interval = config["interval"]
    duration = config["duration"]
    container_names = config["container_names"]

    run(mode, interval, duration, container_names)
