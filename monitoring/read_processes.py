#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sauloferreira

args:
1. mode: command used to monitor (ps or top)
2. interval: interval in seconds to monitor
3. container id: name or identifier of docker container

example: python read_processes.py top 10 cas1
"""

import os
import time
import datetime
import logging
import sys

logging.getLogger().setLevel(logging.INFO)

#-----------------------------------------------------------------------

# params
mode = sys.argv[1]
interval = int(sys.argv[2])
container_ids = sys.argv[3:]

# running
aux = 0
dir = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")
os.mkdir(f"results/{dir}")
logging.info("Start monitoring. Save data in folder: results/" + dir)

for container_id in container_ids:
    os.mkdir(f"results/{dir}/{container_id}")

while True:
    for container_id in container_ids:
        currentDT = datetime.datetime.now().time()
        logging.info("Running. Current time: " + str(currentDT))
        
        if mode == "top":
            output = os.popen("sudo docker exec -it " + container_id + " top -b -n 3 | sed -n '7, 12{s/^ *//;s/ *$//;s/  */,/gp;};12q'").read()
        else:
            output = os.popen('sudo docker exec -it ' + container_id + ' ps -auxf | awk \'{print $1 "," $2 "," $3 "," $4 "," $5 "," $6 "," $11}\'').read()

        file = open('results/{0}/{1}/ProcessesInformation_{2}_{3}.csv'.format(dir, container_id, aux, str(currentDT)),'w')
        file.write(output)
        file.close()

    aux = aux + 1 
    if aux > 3:
        break;

    time.sleep(interval) 

