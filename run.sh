#!/usr/bin/env bash
set -x

HADOOP_STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming.jar
HDFS_INPUT_DIR=${1}
HDFS_OUTPUT_DIR=${2}
JOB_NAME=${3}

hdfs dfs -rm -r -skipTrash $HDFS_OUTPUT_DIR

yarn jar $HADOOP_STREAMING_JAR \
        -D mapreduce.job.name=$JOB_NAME \
        -files mapper_hw2.py,reducer_hw2.py \
        -mapper 'python3 mapper_hw2.py' \
        -reducer 'python3 reducer_hw2.py' \
        -input $HDFS_INPUT_DIR \
        -output $HDFS_OUTPUT_DIR \
		-numReduceTasks 2

hdfs dfs -cat $HDFS_OUTPUT_DIR/part-00000 | head -n 50