#!/bin/bash

if [ "$1" = "" ]; then
    echo 'Please set profiled command'
    exit
fi

CMD="$1"
 
BEGIN_TIME=`date +%s`

# When this is killed
function last () {
  #PID_PROF=`ps -e -o pid,cmd | grep "pidstat .* $CMD" | grep -v grep | awk '{ print $1 }'`
  #echo $PID_PROF
  #kill -15 $PID_PROF
  cat $TMP_FILE | grep "$CMD" > __${TMP_FILE}
  python arrange_perform_result.py __$TMP_FILE 
  status=$?
  rm $TMP_FILE
  rm __$TMP_FILE
  exit $status
}

set -- $CMD
TMP_FILE="tmp_$BEGIN_TIME_$1.log"
trap 'last'  {1,2,3,15}
# Start Profiling
pidstat -u -r -h -l -p ALL -C "$CMD" 1 > $TMP_FILE

last
