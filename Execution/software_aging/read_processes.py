#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 15:11:27 2019

@author: ermesonandrade
"""

#https://psutil.readthedocs.io/en/latest/

#https://www.thepythoncode.com/article/get-hardware-system-information-python

import os
import time
import datetime

#-----------------------------------------------------------------------
aux = 0

while True:

    currentDT = datetime.datetime.now().time()
    print ("Current time:", str(currentDT))
    
    output = os.popen('sudo docker exec -it cas1 ps -auxf | awk \'{print $1 "," $2 "," $3 "," $4 "," $5 "," $6 "," $11}\'').read()
    file = open('processes/ProcessesInformation_{0}_{1}.txt'.format(aux, str(currentDT)),'w')
    file.write(output)
    file.close()
    
    #time.sleep(3600) #Espera 1 hora para coletar novamente
    aux = aux + 1 
    time.sleep(1) 

