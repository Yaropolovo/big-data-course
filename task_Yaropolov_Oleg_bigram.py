import re
from pyspark.sql import SparkSession

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

first_word = 'narodnaya'
article_rdd = sc.textFile("/data/wiki/en_articles_part")
words_rdd = article_rdd.map(lambda x: re.findall(r"\w+", x.lower())[1:])
required_bigrams_rdd = words_rdd \
    .flatMap(lambda words: [(words[i]+'_'+words[i+1]) for i in range(len(words)-1) if words[i] == first_word]) \
    .map(lambda x: (x, 1)) \
    .reduceByKey(lambda x, y: x+y)

result_output = required_bigrams_rdd.collect()
for k, v in sorted(result_output, key=lambda x: x[0]):
    print(k, v, sep='\t')

sc.stop()
