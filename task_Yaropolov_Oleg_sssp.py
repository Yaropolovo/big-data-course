from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import pyspark.sql.functions as F
from pyspark.sql.types import StructType, IntegerType

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

data_source = '/data/twitter/twitter.txt'
user_s = 34
follower_s = 12

schema = StructType() \
      .add("user", IntegerType(), True) \
      .add("follower", IntegerType(), True)

df = spark.read.format("csv") \
    .options(header=False, delimiter='\t') \
    .schema(schema) \
    .load(data_source)

current_level = 0
user_levels = df.select('user').distinct() \
    .withColumn('level', F.when(col('user') != user_s, F.lit(-1)).otherwise(F.lit(0)))

while user_levels.filter((col('user') == follower_s) & (col('level') >= 0)).count() == 0:
    current_level_users = user_levels.filter(col('level') == current_level).select('user')
    followers_next_level = df.join(current_level_users, 'user', 'inner').select('follower').distinct()

    current_level += 1

    user_levels.createOrReplaceTempView("user_levels")
    followers_next_level.createOrReplaceTempView("followers_next_level")

    query = f'''
    SELECT l.user
        ,IF(n.follower is null, 
            l.level, 
            IF(l.level > -1, l.level, {current_level})                            
            ) AS level
    FROM user_levels l
        LEFT JOIN followers_next_level n
            ON l.user = n.follower
    '''
    user_levels = spark.sql(query)

result = user_levels.filter(col('user') == follower_s).collect()
print(result[0].level)

sc.stop()