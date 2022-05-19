import http from 'k6/http';
import { Client } from 'cassandra-driver';
import { sleep } from 'k6';

export default function () {
  http.get('https://test.k6.io');
  sleep(1);
}