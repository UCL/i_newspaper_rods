#/bin/bash -l

# Load in modules functions
source /shared/ucl/apps/modules/3.2.6/Modules/3.2.6/init/bash

# Load the Java module as SPARK runs on the JVM
module load java
module load rsd-modules
module load spark

# Log to a senseible location
export SPARK_LOG_DIR="/home/${USER}/Scratch/sparklogs/run.${JOB_ID}"

${SPARK_HOME}/sbin/stop-master.sh
