cqlsh -e "CREATE KEYSPACE testvalidation WITH REPLICATION={'class':'SimpleStrategy','replication_factor':1};"
cqlsh -e "CREATE TABLE testvalidation.sampletable (identifier text, column1 text, column2 text, column3 text, column4 text, column5 text, column6 text, column7 text, column8 text, column9 text, column10 text, PRIMARY KEY (identifier));"
