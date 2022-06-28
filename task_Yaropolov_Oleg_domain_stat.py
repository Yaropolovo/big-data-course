import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import count, approx_count_distinct

parser = argparse.ArgumentParser()
parser.add_argument("--kafka-brokers", required=True)
parser.add_argument("--topic-name", required=True)
parser.add_argument("--starting-offsets", default='latest')

group = parser.add_mutually_exclusive_group()
group.add_argument("--processing-time", default='0 seconds')
group.add_argument("--once", action='store_true')

args = parser.parse_args()
if args.once:
    args.processing_time = None
else:
    args.once = None

DEPLOYMENT = "yarn"

if DEPLOYMENT == "yarn":
    spark = SparkSession.builder \
        .master("yarn") \
        .appName("spark-course") \
        .config("spark.driver.memory", "512m") \
        .config("spark.driver.cores", "1") \
        .config("spark.executor.instances", "3") \
        .config("spark.executor.cores", "1") \
        .config("spark.executor.memory", "1g") \
        .getOrCreate()
elif DEPLOYMENT == "local":
    spark = SparkSession.builder \
        .master("local[2]") \
        .appName("spark-course") \
        .config("spark.driver.memory", "512m") \
        .getOrCreate()
else:
    raise NotImplementedError("Deployment {d} is not supported!".format(d=DEPLOYMENT))

sc = spark.sparkContext

spark.conf.set("spark.sql.shuffle.partitions", 32)

input_df = spark \
    .readStream \
    .format('kafka') \
    .option('kafka.bootstrap.servers', args.kafka_brokers) \
    .option('subscribe', args.topic_name) \
    .option("startingOffsets", args.starting_offsets) \
    .load()

casted_df = input_df \
    .selectExpr("cast(value as string)") \
    .selectExpr("split(value, '\t')[1] as uid",
                "parse_url(split(value, '\t')[2], 'HOST') as domain")

grouped_df = casted_df \
    .groupBy('domain') \
    .agg(count("*").alias('view'),
         approx_count_distinct('uid').alias('unique')) \
    .sort('view', ascending=False)

grouped_df.createOrReplaceTempView('gr_df')
res = spark.sql("SELECT domain, view, unique FROM gr_df ORDER BY view DESC LIMIT 10")

query = res \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .trigger(once=args.once, processingTime=args.processing_time) \
    .option("truncate", "false") \
    .start()

query.awaitTermination()

spark.stop()
