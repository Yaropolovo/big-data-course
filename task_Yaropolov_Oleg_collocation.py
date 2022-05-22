import math
from pyspark.sql import SparkSession
import re

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

article_rdd = sc.textFile("/data/wiki/en_articles_part")
stop_words = sc.textFile("/data/stop_words/stop_words_en-xpo6.txt")

stop_words_local = stop_words.collect()
broadcast_sw = sc.broadcast(stop_words_local)

words_rdd = article_rdd \
    .map(lambda x: [word for word in re.findall(r"\w+", x.lower())[1:] if word not in broadcast_sw.value]).persist()

total_number_of_bigrams = words_rdd \
    .map(lambda x: len(x)-1) \
    .reduce(lambda x, y: x+y)

word_counter = words_rdd \
    .flatMap(lambda x: x) \
    .map(lambda x: (x, 1)) \
    .reduceByKey(lambda x, y: x+y)

bigram_counter = words_rdd \
    .flatMap(lambda words: [(words[i]+'_'+words[i+1], 1) for i in range(len(words)-1)]) \
    .reduceByKey(lambda x, y: x+y)


def npmi(ab_count: int, a_count: int, b_count: int, total_count: int = total_number_of_bigrams) -> float:
    p_a = a_count/total_count
    p_b = b_count/total_count
    p_ab = ab_count/total_count
    npmi_value = -math.log(p_ab/(p_a*p_b))/math.log(p_ab)
    return round(npmi_value, 3)


npmi_rdd = bigram_counter \
    .filter(lambda x: x[1] >= 500) \
    .map(lambda x: (x[0].split('_')[0], (x[0].split('_')[1], x[1]))) \
    .join(word_counter) \
    .map(lambda x: (x[1][0][0], (x[0], x[1][0][1], x[1][1]))) \
    .join(word_counter) \
    .map(lambda x: (x[1][0][0]+'_'+x[0], x[1][0][1], x[1][0][2], x[1][1])) \
    .map(lambda x: (x[0], npmi(x[1], x[2], x[3])))

output_rows = 39
npmi_local = npmi_rdd.takeOrdered(output_rows, key=lambda x: -x[1])
for k, v in npmi_local:
    print(k, v, sep='\t')

sc.stop()
