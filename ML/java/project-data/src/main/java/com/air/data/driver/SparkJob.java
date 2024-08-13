package com.air.data.driver;

import org.apache.spark.SparkConf;

import java.io.Serializable;

public interface SparkJob extends Serializable {

  /** 具体执行的方法。 */
  void run() throws Exception;

  /**
   * get spark config
   *
   * @return
   */
  SparkConf getSparkConf();

  /** close */
  void close();
}
