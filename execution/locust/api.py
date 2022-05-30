
from cassandra.cluster import Cluster
from cassandra.policies import RoundRobinPolicy
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import DowngradingConsistencyRetryPolicy
from cassandra.query import tuple_factory
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement

from locust import User, events

from dotenv import load_dotenv

import os
import time

@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--consistency-level", type=str, env_var="CONSISTENCY_LEVEL", default="ONE", help="Consistency level")


class CassandraClient(object):
    _consistency_map = {
        "ONE": ConsistencyLevel.ONE,
        "QUORUM": ConsistencyLevel.QUORUM,
        "ALL": ConsistencyLevel.ALL
    }

    def __init__(self, host, consistency_level):
        self.consistency_level = consistency_level
        cluster = Cluster([host], port=9042, load_balancing_policy=RoundRobinPolicy())
        self.session = cluster.connect("testvalidation")
        self.session.default_timeout = 15
        load_dotenv()
    
    def execute(self, query, name=None):
        name = query if not name else name

        start_time = time.time()
        try:
            query = SimpleStatement(query, consistency_level=self._get_consistency())
            self.session.execute(query)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="query", name=name, response_time=total_time, exception=e, response_length=0)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="query", name=name, response_time=total_time, response_length=0)

    def _get_consistency(self):
        return self._consistency_map.get(self.consistency_level)

class CassandraLocust(User):
    abstract = True

    def __init__(self, *args, **kwargs):
        super(CassandraLocust, self).__init__(*args, **kwargs)
        self.client = CassandraClient(self.host, self.environment.parsed_options.consistency_level)