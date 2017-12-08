#!/bin/bash

if [ "$1" = "" -o "$2" = "" ]; then
    echo "Please set number, mode."
    exit
fi

NUM=$1
MODE=$2

START_TIME=`date +%s`
RESULT_DIR="result_"$1"_"$2"_"$START_TIME

mkdir $RESULT_DIR

## Data set
APP_IDS_FILE="appids.txt"
python dataset.py $NUM $MODE > $APP_IDS_FILE

## Profile
DIRNAME=`pwd`
PROFILE_SCRIPT="profile_perform.sh"
RUN_TIME=20
PROFILE_TIME=10
MAIN_CMD="python main.py"
MONGO_CMD="mongodb.conf"

LOG_USAGE_MAIN=$RESULT_DIR"/usage_main.log"
LOG_USAGE_DB=$RESULT_DIR"/usage_mongo.log"

cd ..
# Run main script
timeout $RUN_TIME $MAIN_CMD &
cd $DIRNAME
sleep 1
# Run profiling for main
timeout $RUN_TIME bash $PROFILE_SCRIPT $MAIN_CMD > $LOG_USAGE_MAIN &
# Run profiling for mongodb
timeout $RUN_TIME bash $PROFILE_SCRIPT $MONGO_CMD > $LOG_USAGE_DB & 

sleep $RUN_TIME

cat $APP_IDS_FILE | while read appid
do
  python datacollect.py $appid > $RESULT_DIR"/datastore_"$appid"_db.log"
  mv ../apps/testapp/logs/${appid}.log $RESULT_DIR/datastore_${appid}_app.log
done

exit
