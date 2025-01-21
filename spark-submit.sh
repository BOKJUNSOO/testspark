#!/bin/bash

echo = 'submit spark application'
File="jobs/main.py"
docker exec -it testspark-spark-master-1 spark-submit \
       	--master spark://spark-master:7077 \
        --executor-cores 2 \
	--executor-memory 2g \
	$File
#	--executor-cores 2 \

#	--executor-memory 2G\
#	$File
	#	--conf spark.executor.memory=2G\
	#$File
	#--conf spark.sql.shuffle.partitions=200 \
	#$File
	#--executor-cores 2
