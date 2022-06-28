#!/usr/bin/env bash
set -x

HADOOP_STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming.jar
NUM_REDUCERS=2
HDFS_INPUT_DIR=${1}
HDFS_OUTPUT_DIR=${2}
JOB_NAME=${3}

hdfs dfs -rm -r -skipTrash ${HDFS_OUTPUT_DIR}*

# Wordcount
yarn jar $HADOOP_STREAMING_JAR \
    -D mapreduce.job.name=${JOB_NAME}_Phase_1 \
    -D stream.num.map.output.key.fields=2 \
    -D stream.num.reduce.output.key.fields=2 \
    -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
    -D mapreduce.partition.keycomparator.options="-k1,1n -k2,2" \
    -files test_mapper.py\
    -mapper 'python3 test_mapper.py' \
    -input $HDFS_INPUT_DIR \
    -numReduceTasks $NUM_REDUCERS \
    -output ${HDFS_OUTPUT_DIR}

hdfs dfs -cat ${HDFS_OUTPUT_DIR}/*