import os
import pandas as pd
import time
from progress.bar import Bar

JMETER_PATH = "~/study/apache-jmeter/apache-jmeter-5.4.3/bin/jmeter"

tests = pd.read_csv("scenarios_stress.csv", encoding = "ISO-8859-1")

len = tests.shape[0]
bar = Bar("progress", max=len)

for i in range(len):
    #if i < 29:
    #    bar.next()
    #    continue

    command = ""
    command = \
        f"{JMETER_PATH} " + \
        r"-n -t ./stress-cassandra.jmx -l " + r"results/test001.jtl " + \
        f"-Jname=test_{tests['id'][i]} -Jlifetime={tests['duration'][i]} " + \
        f"-Jusers={tests['users'][i]} -Jlines={tests['lines'][i]} -Jconsistency={tests['consistency'][i]}"

    print(" id", i, "command", command)
    bar.next()
    os.system(command)
    time.sleep(30)
bar.finish()
