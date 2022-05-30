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

import os
import time
import datetime
import sys

#-----------------------------------------------------------------------

# params
mode = sys.argv[1]
interval = int(sys.argv[2])
duration = int(sys.argv[3])
container_ids = sys.argv[4:]

# running
aux = 0
dir = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")
os.mkdir(f"results/{dir}")
print("Start monitoring. Save data in folder: results/" + dir)

for container_id in container_ids:
    os.mkdir(f"results/{dir}/{container_id}")

start_at = datetime.datetime.now()

while True:
    for container_id in container_ids:
        currentDT = datetime.datetime.now().time()
        print("Running. Current time: " + str(currentDT))
        
        if mode == "top":
            output = os.popen("sudo docker exec -it " + container_id + " top -b -n 3 | sed -n '7, 12{s/^ *//;s/ *$//;s/  */,/gp;};12q'").read()
        else:
            output = os.popen('sudo docker exec -it ' + container_id + ' ps -auxf | awk \'{print $1 "," $2 "," $3 "," $4 "," $5 "," $6 "," $11}\'').read()

        file = open('results/{0}/{1}/ProcessesInformation_{2}_{3}.csv'.format(dir, container_id, aux, str(currentDT)),'w')
        file.write(output)
        file.close()

    now = datetime.datetime.now()
    if (now - start_at).total_seconds() > duration:
        break

    time.sleep(interval) 
    aux = aux + interval

