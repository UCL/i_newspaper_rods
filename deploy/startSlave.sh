#/bin/bash -l

if [ -z "$1" ]
then
	echo "Failed to provide a sparkmaster. Failing"
	exit 3
fi

sparkmaster="$1"

# Load in modules functions
source /shared/ucl/apps/modules/3.2.6/Modules/3.2.6/init/bash

# Load the Java module as SPARK runs on the JVM
module load java
module load rsd-modules
module load spark

# Log to a senseible location
export SPARK_LOG_DIR="/home/${USER}/Scratch/sparklogs/run.${JOB_ID}"
export SPARK_LOCAL_DIRS="$SPARK_LOG_DIR"
export SPARK_WORKER_DIR="${TMPDIR}/spark"

cd ${SPARK_HOME}  
spark-class org.apache.spark.deploy.worker.Worker "${sparkmaster}" > "${SPARK_LOG_DIR}/worker-${HOSTNAME}.out"
