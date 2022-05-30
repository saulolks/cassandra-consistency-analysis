from api import CassandraLocust
from locust import Locust, events, task, TaskSet
import random

@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--test-name", type=str, env_var="TEST_NAME", default="default-test", help="Test name")
    parser.add_argument("--rows-len", type=str, env_var="ROWS_LEN", default="1", help="Quantity of rows")


class SimpleUser(CassandraLocust):
    min_wait = 10
    max_wait = 500
    host = "localhost"

    @task
    def select_task(self):
        rows_quantity = self.environment.parsed_options.rows_len
        test_name = self.environment.parsed_options.test_name

        query = f"select * from testvalidation.sampletable limit {rows_quantity}"
        self.client.execute(query, f"[READ] {test_name}")


class PopulateUser(CassandraLocust):
    min_wait = 10
    max_wait = 500
    host = "localhost"

    @task
    def select_task(self):
        test_name = self.environment.parsed_options.test_name

        id = random.randint(1, 1000000000)
        query = f"insert into testvalidation.sampletable (\"identifier\", \"column1\", \"column2\", \"column3\", \"column4\", \"column5\", \"column6\", \"column7\", \"column8\", \"column9\", \"column10\") values ('{id}', 'teste', 'teste', 'teste', 'teste', 'teste', 'teste', 'teste', 'teste', 'teste', 'teste');"
        self.client.execute(query, f"[WRITE] {test_name}")