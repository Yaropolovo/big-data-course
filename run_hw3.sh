#!/usr/bin/env bash
set -x

HADOOP_STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming.jar
NUM_REDUCERS=2
HDFS_INPUT_DIR=${1}
HDFS_OUTPUT_DIR=${2}
JOB_NAME=${3}

hdfs dfs -rm -r -skipTrash ${HDFS_OUTPUT_DIR}*

# Wordcount
( yarn jar $HADOOP_STREAMING_JAR \
    -D mapreduce.job.name=${JOB_NAME}_Phase_1 \
    -D stream.num.map.output.key.fields=2 \
    -D stream.num.reduce.output.key.fields=2 \
    -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
    -D mapreduce.partition.keycomparator.options="-k1,1n -k2,2" \
    -files mapper1_hw3.py,reducer1_hw3.py \
    -mapper 'python3 mapper1_hw3.py' \
    -combiner 'python3 reducer1_hw3.py' \
    -reducer 'python3 reducer1_hw3.py' \
    -input $HDFS_INPUT_DIR \
    -numReduceTasks $NUM_REDUCERS \
    -output ${HDFS_OUTPUT_DIR}_tmp &&

yarn jar $HADOOP_STREAMING_JAR \
    -D mapreduce.job.name=${JOB_NAME}_Phase_2 \
    -D stream.num.map.output.key.fields=2 \
    -D stream.num.reduce.output.key.fields=2 \
    -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
    -D mapreduce.partition.keycomparator.options="-k1,1n -k2,2nr" \
    -files mapper2_hw3.py,reducer2_hw3.py \
    -mapper 'python3 mapper2_hw3.py' \
    -reducer 'python3 reducer2_hw3.py' \
    -numReduceTasks 1 \
    -input ${HDFS_OUTPUT_DIR}_tmp \
    -output ${HDFS_OUTPUT_DIR}
) || echo "Error happens"

hdfs dfs -rm -r -skipTrash ${HDFS_OUTPUT_DIR}_tmp

hdfs dfs -cat ${HDFS_OUTPUT_DIR}/*