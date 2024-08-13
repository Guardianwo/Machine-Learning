spark-submit \
--master yarn
--deploy-mode client \
--class com.air.data.CleanJob \
--driver-memory 1G \
--driver-cores 1 \
--executor-memory 2G \
--executor-cores 1 \
--num-executors 1 \
./project-data-jar-with-dependencies.jar 