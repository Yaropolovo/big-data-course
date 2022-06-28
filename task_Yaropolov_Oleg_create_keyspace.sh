#!/usr/bin/env bash
set -x

CASSANDRA_ENDPOINT=${1}
KEYSPACE_NAME=${2}

QUERY_TEXT="CREATE KEYSPACE IF NOT EXISTS ${KEYSPACE_NAME} WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 2};"

cqlsh $CASSANDRA_ENDPOINT -e "$QUERY_TEXT"