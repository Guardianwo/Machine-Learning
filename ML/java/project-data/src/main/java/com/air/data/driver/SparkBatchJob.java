package com.air.data.driver;

import com.air.data.constant.BaseConfig;
import lombok.extern.slf4j.Slf4j;
import org.aeonbits.owner.ConfigFactory;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.SparkSession;

@Slf4j
public abstract class SparkBatchJob implements SparkJob {

  private static final long serialVersionUID = -8233142835013995375L;
  protected BaseConfig baseConfig = ConfigFactory.create(BaseConfig.class);
  protected JavaSparkContext sparkContext;
  protected SparkConf sparkConf;
  protected SparkSession spark;

  public SparkBatchJob() {
    sparkConf = getSparkConf();
    if (baseConfig.appMaster().contains("local")) {
      sparkConf.setMaster(baseConfig.appMaster());
    }
    spark = SparkSession.builder().config(sparkConf).getOrCreate();
    sparkContext = new JavaSparkContext(spark.sparkContext());
  }

  @Override
  public SparkConf getSparkConf() {
    SparkConf sparkConf = new SparkConf();
    sparkConf.setAppName(baseConfig.appName());
    sparkConf.set("spark.broadcast.compress", "true");
    sparkConf.set("spark.io.compression.codec", "snappy");
    sparkConf.set("spark.rdd.compress", "true");
    sparkConf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer");
    sparkConf.set("spark.hadoop.hive.exec.max.dynamic.partitions", "800");
    sparkConf.set("spark.hadoop.mapreduce.job.maps", "800");
    return sparkConf;
  }

  @Override
  public void close() {
    log.info("spark closing ...");
    spark.close();
    log.info("spark closed");
  }
}
