from executon.locust.analysis.api import CassandraLocust
from locust import Locust, events, task, TaskSet

class SimpleUser(CassandraLocust):
    min_wait = 10
    max_wait = 500
    host = "localhost"

    @task
    def select_task(self):
        self.client.execute("select * from testvalidation.sampletable", "test001")


