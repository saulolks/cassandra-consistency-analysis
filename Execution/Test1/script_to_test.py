import os
import pandas as pd
import time
from progress.bar import Bar

tests = pd.read_csv("scenarios.csv", encoding = "ISO-8859-1")
test_name = ".\testplan-cassandra.jmx"


len = tests.shape[0]
bar = Bar("progress", max=len)

for i in range(len):
    command = ""
    command = \
        r"C:\Users\T-Gamer\Documents\apache-jmeter-5.4.1\apache-jmeter-5.4.1\bin\jmeter " + \
        r"-n -t .\testplan-cassandra.jmx -l " + r"results\test002.jtl " + \
        f"-Jname=test_{tests['name'][i]} -Jinterval={tests['interval'][i]} " + \
        f"-Jusers={tests['users'][i]} -Jlines={tests['lines'][i]} -Jconsistency={tests['consistency'][i]}"

    print(" id", i, "command", command)
    bar.next()
    os.system(command)
bar.finish()