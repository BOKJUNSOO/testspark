from pyspark.sql import SparkSession, Window
import pyspark.sql.functions as F
spark = SparkSession.builder \
                    .master("local") \
                    .appName("spark_opt") \
                    .config("spark.eventLog.enabled", "true")\
                    .config("spark.eventLog.dir","/opt/bitnami/spark/spark-events")\
                    .config("spark.history.fs.logDirectory","/opt/bitnami/spark/spark-events")\
                    .getOrCreate()
target_file = "/opt/bitnami/spark/data/test_data.json"
df = spark.read.format("json").option("multiLine",True).load(target_file)
df = df.select(F.explode("ranking").alias("user"))
df = df.select("user.character_name",
               "user.date",
               "user.class_name",
               "user.sub_class_name",
               "user.character_level",
               "user.character_exp")
spark_df = df.withColumn("class",df["sub_class_name"])
spark_df = spark_df.withColumn("class",F.when(spark_df["sub_class_name"]== "", spark_df["class_name"]) \
                                             .otherwise(spark_df["class"]))
spark_df = spark_df.drop("class_name","sub_class_name")
# 각 유저가 위치한 지역정보 컬럼 추가
df = spark_df.withColumn("status",
                   F.when(spark_df["character_level"]>=290,"Tallahart") \
                    .when((spark_df["character_level"]<=289)&(spark_df["character_level"]>=285),"Carcion") \
                    .when((spark_df["character_level"]<=284)&(spark_df["character_level"]>=280),"Arteria") \
                    .when((spark_df["character_level"]<=279)&(spark_df["character_level"]>=275),"Dowonkyung") \
                    .when((spark_df["character_level"]<=274)&(spark_df["character_level"]>=270),"Odium") \
                    .when((spark_df["character_level"]<=269)&(spark_df["character_level"]>=265),"HotelArcs") \
                    .when((spark_df["character_level"]<=264)&(spark_df["character_level"]>=260),"Cernium") \
                    .otherwise("AcaneRiver"))


df = df.groupBy("class","status","date").agg(F.max(df.character_exp).alias("max_exp"),
                                             F.sum(df.character_exp).alias("sum_exp"),
                                             F.mean(df.character_exp).alias("mean_exp"))
df.show()
hunt = Window.partitionBy("status").orderBy(F.desc("sum_exp"))
df = df.withColumn("hunt_rank",F.rank().over(hunt))
df.show()