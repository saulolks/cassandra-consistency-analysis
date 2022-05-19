import { Client } from "./node_modules/cassandra-driver/index.js";

export default function (){

    // const cassandra = require("cassandra-driver");
    const client = Client({
        contactPoints: ["localhost:9042"],
        localDataCenter: "datacenter1",
        keyspace: "testvalidation"
    })

    client.connect()

    const query = "SELECT * FROM sampletable LIMIT 1";
    client.execute(query).then(  result => console.log('Row from Keyspaces %s', result.rows[0]) )
};