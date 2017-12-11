#!/bin/bash

if [ "$1" = "" -o "$2" = "" -o "$3" = "" ]; then
  echo "Please set number, and 2 intervals"
  exit
fi

NUM=$1
INTERVAL=$2
INTERVAL2=$3

START_TIME=`date +%s`
RESULT_DIR="result_"$1"_"$2"_"$3"_"$START_TIME

mkdir $RESULT_DIR

## Data set
echo "Preparing data set..."
APP_IDS_FILE="appids.txt"
#python dataset.py $NUM $MODE > $APP_IDS_FILE
python dataset.py $NUM 0 > $APP_IDS_FILE
echo "Done"
echo ""


## Interval set
echo "Setting interval"
python changeinterval.py $INTERVAL $INTERVAL2
echo "Done"
echo ""

## Profile
DIRNAME=`pwd`
PROFILE_SCRIPT="profile_perform.sh"
RUN_TIME=20
MAIN_CMD="python main.py"
MONGO_CMD="mongodb.conf"

LOG_USAGE_MAIN=$RESULT_DIR"/usage_main.log"
LOG_USAGE_DB=$RESULT_DIR"/usage_mongo.log"

echo "Running main and profiling..."
# Run profiling for main
timeout $RUN_TIME bash $PROFILE_SCRIPT $MAIN_CMD > $LOG_USAGE_MAIN &
# Run profiling for mongodb
timeout $RUN_TIME bash $PROFILE_SCRIPT $MONGO_CMD > $LOG_USAGE_DB & 
cd ..
# Run main script
timeout $RUN_TIME $MAIN_CMD &
cd $DIRNAME


sleep 10

#######

cat $APP_IDS_FILE | awk 'NR%2==1' | while read appid
do
  echo 1 > ../apps/testapp/io/${appid}.io
  sleep 1
done &

#######


sleep $(($RUN_TIME - 10))
sleep 2

echo "Done"
echo ""

echo "Collecting and Calculating datastores..."
#
#DATASTORE_CALC_DB=$RESULT_DIR/datastore_calc_db.rst
#DATASTORE_CALC_APP=$RESULT_DIR/datastore_calc_app.rst
#
#echo -n "" > $DATASTORE_CALC_DB
#echo -n "" > $DATASTORE_CALC_APP
#
#
cat $APP_IDS_FILE | while read appid
do
  DATASTORE_FILE_DB=$RESULT_DIR/datastore_${appid}_db.log
  DATASTORE_FILE_APP=$RESULT_DIR/datastore_${appid}_app.log

  python datacollect.py $appid > $DATASTORE_FILE_DB
  mv ../apps/testapp/logs/${appid}.log $DATASTORE_FILE_APP
#  rm ../apps/testapp/io/${appid}.io
#
#  # calc
#  python datacalc.py $DATASTORE_FILE_DB >> $DATASTORE_CALC_DB
#  python datacalc.py $DATASTORE_FILE_APP>> $DATASTORE_CALC_APP
done
#
#echo "Done"
#echo ""
#
#echo "Integrating datastore result..."
#
#python datarst_integrate.py $DATASTORE_CALC_DB > $RESULT_DIR/datastore_avg_db.rst
#python datarst_integrate.py $DATASTORE_CALC_APP > $RESULT_DIR/datastore_avg_app.rst
#
#echo "Done"
#echo ""



echo ""
echo "Done"

exit
