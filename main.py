from pyspark.sql import SparkSession
spark = SparkSession.builder \
                    .master("local") \
                    .appName("spark_opt") \
                    .config("spark.eventLog.enabled", "true")\
                    .config("spark.eventLog.dir","/tmp/spark-events")\
                    .config("spark.history.fs.logDirectory","/tmp/spark-events")
target_file = "/opt/bitnami/spark/data/test_data.json"
df = spark.read.format("json").option("multiLine",True).load(target_file)
df.printSchema()
