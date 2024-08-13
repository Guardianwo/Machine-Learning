package com.air.data.service;

import com.air.data.constant.BaseConfig;
import org.aeonbits.owner.ConfigFactory;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

public class DataService {

  protected BaseConfig baseConfig = ConfigFactory.create(BaseConfig.class);
  SparkSession spark;

  public DataService(SparkSession spark) {
    this.spark = spark;
  }

  public Dataset<Row> getTask3() {
    Dataset<Row> data =
        spark
            .read()
            .option("header", "true")
            // 自动推断schema
            .option("inferSchema", "true")
            .option("encoding", "utf-8")
            .csv(baseConfig.basePath() + "/task3.csv")
            // 序号,门禁卡号,进出时间,进出地点,是否通过,描述
            .withColumnRenamed("序号", "id")
            .withColumnRenamed("门禁卡号", "card_id")
            .withColumnRenamed("进出时间", "entry_exit_time")
            .withColumnRenamed("进出地点", "entry_exit_address")
            .withColumnRenamed("是否通过", "is_passed")
            .withColumnRenamed("描述", "desc");
    return data;
  }

  public Dataset<Row> getTask4() {
    Dataset<Row> data =
        spark
            .read()
            .option("header", "true")
            // 自动推断schema
            .option("inferSchema", "true")
            .option("encoding", "utf-8")
            .csv(baseConfig.basePath() + "/task4.csv")
            // 序号,校园卡号,性别,专业名称,门禁卡号,流水号,校园卡编号,消费时间,消费金额,存储金额,余额,消费次数,消费类型,消费项目编码,操作编码,消费地点
            .withColumnRenamed("序号", "id")
            .withColumnRenamed("校园卡号", "school_card_id")
            .withColumnRenamed("性别", "sex")
            .withColumnRenamed("专业名称", "major")
            .withColumnRenamed("门禁卡号", "card_id")
            .withColumnRenamed("流水号", "serial_number")
            .withColumnRenamed("校园卡编号", "school_card_no")
            .withColumnRenamed("消费时间", "consume_time")
            .withColumnRenamed("消费金额", "consume_money")
            .withColumnRenamed("存储金额", "save_money")
            .withColumnRenamed("余额", "balance")
            .withColumnRenamed("消费次数", "consume_nums")
            .withColumnRenamed("消费类型", "consume_type")
            .withColumnRenamed("消费项目编码", "consume_item_id")
            .withColumnRenamed("操作编码", "operation_code")
            .withColumnRenamed("消费地点", "consume_address");
    return data;
  }

  public Dataset<Row> getTask5() {
    Dataset<Row> data =
        spark
            .read()
            .option("header", "true")
            // 自动推断schema
            .option("inferSchema", "true")
            .option("encoding", "utf-8")
            .csv(baseConfig.basePath() + "/task5.csv")
            // 序号_x,校园卡号,性别,专业名称,门禁卡号,序号_y,进出时间,进出地点,是否通过,描述
            .withColumnRenamed("序号_x", "id_x")
            .withColumnRenamed("校园卡号", "school_card_id")
            .withColumnRenamed("性别", "sex")
            .withColumnRenamed("专业名称", "major")
            .withColumnRenamed("门禁卡号", "card_id")
            .withColumnRenamed("序号_y", "id_y")
            .withColumnRenamed("进出时间", "entry_exit_time")
            .withColumnRenamed("进出地点", "entry_exit_address")
            .withColumnRenamed("是否通过", "is_passed")
            .withColumnRenamed("描述", "desc");
    return data;
  }
}
