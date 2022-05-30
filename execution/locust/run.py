import os
import pandas as pd
import argparse
from progress.bar import Bar
import datetime

parser = argparse.ArgumentParser(description="Cassandra Locust Test", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--scenario", help="Path to the CSV scenario file")
parser.add_argument("--test-type", help="Type of the test: software-aging, stress or analysis")

args = parser.parse_args()
config = vars(args)
print(config)

scenarios = pd.read_csv(config["scenario"], encoding = "ISO-8859-1")

dir_datetime = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")
result_dir = f"results/{config['test_type']}/{dir_datetime}"
os.mkdir(result_dir)
os.system(f"cp {config['scenario']} {result_dir}/executed_scenario.csv")

len = scenarios.shape[0]
bar = Bar("progress", max=len)


for i in range(len):
    os.mkdir(f"{result_dir}/test_{scenarios['id'][i]}")

    command = f"locust --users={scenarios['users'][i]} --run-time={scenarios['duration'][i]}s " +\
        f"--rows={scenarios['lines'][i]} --consistency-level={scenarios['consistency'][i]} " +\
        f"--test-name={scenarios['id'][i]} --html={result_dir}/test_{scenarios['id'][i]}/result.html " +\
        f"--csv={result_dir}/test_{scenarios['id'][i]}/result SimpleUser"

    print(" id", i, "command\n\n", command, "\n\n")
    bar.next()
    os.system(command)

bar.finish()