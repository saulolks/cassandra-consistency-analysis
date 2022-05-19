import os
import pandas as pd
import time
from progress.bar import Bar

tests = pd.read_csv("scenarios_stress.csv", encoding = "ISO-8859-1")
test_name = ".\stress-cassandra.jmx"


len = tests.shape[0]
bar = Bar("progress", max=len)

for i in range(len):
    #if i < 29:
    #    bar.next()
    #    continue

    command = ""
    command = \
        r"C:\Users\T-Gamer\Documents\apache-jmeter-5.4.1\apache-jmeter-5.4.1\bin\jmeter " + \
        r"-n -t .\stress-cassandra.jmx -l " + r"results\test009.jtl " + \
        f"-Jname=test_{tests['id'][i]} -Jlifetime={tests['duration'][i]} " + \
        f"-Jusers={tests['users'][i]} -Jlines={tests['lines'][i]} -Jconsistency={tests['consistency'][i]}"

    print(" id", i, "command", command)
    bar.next()
    os.system(command)
    time.sleep(30)
bar.finish()