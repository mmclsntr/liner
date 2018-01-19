#!/bin/bash

if [ "$1" = "" ]; then
    echo 'Please set profiled command'
    exit
fi

CMD="$1"
 
BEGIN_TIME=`date +%s`

# When this is killed
function last () {
    cat $TMP_FILE | grep "$CMD" > __${TMP_FILE}
    python arrange_perform_result.py __$TMP_FILE 
    status=$?
    rm $TMP_FILE
    rm __$TMP_FILE
    exit $status
}

trap 'last'  {1,2,3,15}
set -- $CMD
TMP_FILE="tmp_$BEGIN_TIME_$1.log"
# Start Profiling
pidstat -u -r -h -l -p ALL -C "$1" 1 > $TMP_FILE

last
