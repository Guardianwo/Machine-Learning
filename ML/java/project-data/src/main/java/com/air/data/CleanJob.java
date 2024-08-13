package com.air.data;

import com.air.data.constant.BaseConfig;
import com.air.data.driver.SparkBatchJob;
import com.air.data.service.DataService;
import java.util.Properties;
import lombok.extern.slf4j.Slf4j;
import org.aeonbits.owner.ConfigFactory;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SaveMode;
import org.apache.spark.sql.execution.datasources.jdbc.JDBCOptions;

@Slf4j
public class CleanJob extends SparkBatchJob {

  private static final long serialVersionUID = 1120533081741700060L;
  protected BaseConfig baseConfig = ConfigFactory.create(BaseConfig.class);

  /** 具体执行的方法。 */
  @Override
  public void run() throws Exception {
    DataService dataService = new DataService(spark);
    Dataset<Row> task3 = dataService.getTask3().na().fill(0);
    task3.show(false);
    writeDb(task3, "task3");
    Dataset<Row> task4 = dataService.getTask4().na().fill(0);
    task4.show(false);
    writeDb(task4, "task4");
    Dataset<Row> task5 = dataService.getTask5().na().fill(0);
    task5.show(false);
    writeDb(task5, "task5");
  }

  private void writeDb(Dataset<Row> data, String tableName) {
    // data.show(false);
    Properties properties = new Properties();
    properties.setProperty("user", baseConfig.mysqlUser());
    properties.setProperty("password", baseConfig.mysqlPassword());
    properties.put("driver", "com.mysql.jdbc.Driver");
    data.write()
        .mode(SaveMode.Overwrite)
        .option(JDBCOptions.JDBC_BATCH_INSERT_SIZE(), 500)
        .jdbc(baseConfig.mysqlUrl(), tableName, properties);
  }

  public static void main(String[] args) {
    CleanJob batchJob = new CleanJob();
    try {
      batchJob.run();
    } catch (Exception e) {
      log.error("error:{}", e.getMessage());
      e.printStackTrace();
    } finally {
      batchJob.close();
    }
  }
}
