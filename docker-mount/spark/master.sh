#!/bin/bash

export SPARK_MASTER_HOST=${SPARK_MASTER_HOST:-`hostname`}

export SPARK_HOME=/spark

. "/spark/sbin/spark-config.sh"

. "/spark/bin/load-spark-env.sh"

mkdir -p $SPARK_MASTER_LOG

ln -sf /dev/stdout $SPARK_MASTER_LOG/spark-master.out

./spark/sbin/start-thriftserver.sh \
  --hiveconf hive.server2.thrift.port=10001 \
  --hiveconf hive.metastore.uris=thrift://8.210.27.71:19083 \
  --master spark://spark-master:7077 \
  --conf spark.sql.catalogImplementation=hive \
  --conf spark.hadoop.hive.metastore.uris=thrift://8.210.27.71:19083 \
  --conf spark.hadoop.fs.s3a.access.key=ZiLXIPoCS2Sg3fmYYcRe \
  --conf spark.hadoop.fs.s3a.secret.key=1XgvMSAs9BH5MO5JNJqQWoUIvgh4ll7DKSwR4XuE \
  --conf spark.hadoop.fs.s3a.endpoint=minio.ack-hk-hackathon.k8s.openprojectx.org \
  --conf spark.hadoop.fs.s3a.path.style.access=true \
  --conf spark.hadoop.fs.s3a.connection.ssl.enabled=true \
  --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
  --name "OpenLineageSparkJob"

cd /spark/bin && /spark/sbin/../bin/spark-class org.apache.spark.deploy.master.Master \
    --ip $SPARK_MASTER_HOST --port $SPARK_MASTER_PORT --webui-port $SPARK_MASTER_WEBUI_PORT >> $SPARK_MASTER_LOG/spark-master.out