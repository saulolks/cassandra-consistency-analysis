FROM cassandra:4.0.4
EXPOSE 9042

ENV CASSANDRA_CLUSTER_NAME=MyCluster
ENV CASSANDRA_DC=datacenter1
ENV CASSANDRA_RACK=Rack1
ENV CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch
# ENV CASSANDRA_SEEDS=
# ENV HEAP_NEWSIZE=512M
# ENV MAX_HEAP_SIZE=1024M

RUN ["sleep", "60"]
RUN ["cqlsh", "-e", "CREATEKEYSPACE testvalidation WITHREPLICATION={'class':'SimpleStrategy','replication_factor':1};"]
RUN ["cqlsh", "-e", "CREATETABLE testvalidation.sampletable (identifier int, column1text, column2 text, column3text, column4text, column5 text, column6text, column7 text,c olumn8 text, column9 text, column10 text, PRIMARYKEY(identifier));"]
