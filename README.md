# cassandra-consistency-analysis
This project focus on evaluate the consistency levels of the Cassandra database in terms of response time and success rate.

## Monitoring
We also use a python script to monitor the containers. The script provide two possible commands to read this information: ps or top. The parameters can be passed at the running command, none of them are optional and you should respect the following order:

1. mode: command used to monitor (ps or top)
2. interval: interval in seconds to monitor
3. container ids: name or identifier of the docker containers

Example:
`python read_processes.py top 10 cassandra-node-1 cassandra-node-2`

## Run with Locust
First of all, you should configure the enviroment, creating a virtualenv:
`virtualenv path/to/venv --python=python3.8`

After that, you have to activate virtualenv and install the dependencies:
`source path/to/venv/bin/activate`

`pip install -r requirements.txt`

Now, you can run the test plan. If you want to run with locust to evaluate cassandra is preferrable running without web interface. To do this, you can use the following commands:

`locust -f locustfile.py --headless --users=10 --run-time=20m`

| Parameter | Description |
| - | - |
| --headless | run without web interface |
| --autostart | run automatically without disabling web interface |
| --users | number of users (concurrency) |
| --run-time | test duration (10s/30m/1h30m) |
