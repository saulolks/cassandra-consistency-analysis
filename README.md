# Cassandra Consistency Analysis
This project focus on evaluate the consistency levels of the Cassandra database in terms of response time and success rate.

## Setup
To setup the environment with all the tools needed for this work, it is necessary to install Docker and its Docker Compose plugin. Once installed, you can navigate to the setup folder and execute the service with the command bellow:
 
`docker-compose up -d`

The compose file is configured to start cassandra nodes with 1 cpu and 4GB of memory, exposing 9042 port and exporting the setup file stored in the config folder to inside of container. After start up services, you can run the following command to configure the keyspaces and tables needed for tests.

`docker exec -it mycassandra1 sh /var/config/setup.sh`

To check if it is all ok, you can run `docker exec -it mycassandra1 cqlsh -e "describe keyspaces;"` and verify if there some keyspace named "testvalidation".

## Run with Locust
First of all, you should configure the enviroment, creating a virtualenv:
`virtualenv path/to/venv --python=python3.8`

After that, you have to activate virtualenv and install the dependencies:
`source path/to/venv/bin/activate`

`pip install -r requirements.txt`

Now, you can run the test plan. If you want to run with locust to evaluate cassandra is preferrable running without web interface. To do this, you can use the following commands:

`locust -f locustfile.py --headless --users=10 --run-time=20m`

| Parameter   | Description                                       |
| ----------- | ------------------------------------------------- |
| --headless  | run without web interface                         |
| --autostart | run automatically without disabling web interface |
| --users     | number of users (concurrency)                     |
| --run-time  | test duration (10s/30m/1h30m)                     |

### Run with scenarios
The scenarios model is a csv file with some columns used to indicate the parameters of a sequence of tests should be executed. The parameters is indicated down bellow:

| Parameter   | Description                            |
| ----------- | -------------------------------------- |
| id          | test identifier                        |
| users       | concurrent users should be started     |
| duration    | test duration (in seconds)             |
| lines       | quantity of lines should be queried    |
| consistency | consistency adopted (ONE, QUORUM, ALL) |

Once you have the scenario, you can execute the test with the following command:

`python run.py --test-type=software_aging --scenario=scenarios/software_aging/scenario_1.csv`

The arguments descriptions are:

| Argument  | Description                                                                               |
| --------- | ----------------------------------------------------------------------------------------- |
| test-type | description of the tests for identification purposes (stress, software_aging or analysis) |
| scenario  | path to the scenario file                                                                 |

## Monitoring
We also use a python script to monitor the containers. The script provide two possible commands to read this information: ps or top. The parameters can be passed at the running command, none of them are optional and you should respect the following order:

1. mode: command used to monitor (ps or top)
2. interval: interval in seconds to monitor
3. container ids: name or identifier of the docker containers

Example:
`python read_processes.py top 10 cassandra-node-1 cassandra-node-2`