#!/bin/bash

if [ "$1" = "" -o "$2" = "" -o "$3" = "" ]; then
    echo "Please set number, max count, mode."
    exit
fi

if [ ! "$3" = "a" -a ! "$3" = "b" ]; then
    echo "Please set mode 'a' or 'b'."
    exit
fi

SAME_NUM=$1
MAX_COUNT=$2
MODE=$3

## Initialize
PROFILE_PERFORM_SCRIPT="./profile_perform.sh"
NODE_SCRIPT_V1='sentence_v1_'$MODE'.js'
CLIENT_RESULT_V1="result_client_v1_w_${SAME_NUM}_${MODE}.log"
CLIENT_ERROR_V1="result_client_v1_w_${SAME_NUM}_${MODE}.err"
CMD_V1="apache"
CMD_DB_V1="mysql"
SERVER_RESULT_V1="result_server_v1_w_${SAME_NUM}_${MODE}.log"
SERVER_RESULT_DB_V1="result_server_v1_db_w_${SAME_NUM}_${MODE}.log"
echo -n "" > $CLIENT_RESULT_V1
echo -n "" > $CLIENT_ERROR_V1
echo -n "" > $SERVER_RESULT_V1
echo -n "" > $SERVER_RESULT_DB_V1

NODE_SCRIPT_V2='sentence_v2_'$MODE'.js'
CLIENT_RESULT_V2="result_client_v2_w_${SAME_NUM}_${MODE}.log"
CLIENT_ERROR_V2="result_client_v2_w_${SAME_NUM}_${MODE}.err"
CMD_V2="node api.js"
CMD_DB_V2="mongo"
SERVER_RESULT_V2="result_server_v2_w_${SAME_NUM}_${MODE}.log"
SERVER_RESULT_DB_V2="result_server_v2_db_w_${SAME_NUM}_${MODE}.log"
echo -n "" > $CLIENT_RESULT_V2
echo -n "" > $CLIENT_ERROR_V2
echo -n "" > $SERVER_RESULT_V2
echo -n "" > $SERVER_RESULT_DB_V2


## Run tests in 4 devided terms
## v1
$PROFILE_PERFORM_SCRIPT $CMD_V1 > $SERVER_RESULT_V1 &
$PROFILE_PERFORM_SCRIPT $CMD_DB_V1 > $SERVER_RESULT_DB_V1 &
echo "TEST v1: "$SAME_NUM
COUNT_V1=0
while [ $COUNT_V1 -lt $MAX_COUNT ];
do
    COUNT_V1=`expr $COUNT_V1 + 1`
    echo 'Count: '$COUNT_V1
    node $NODE_SCRIPT_V1 $SAME_NUM 1>> $CLIENT_RESULT_V1  2>> $CLIENT_ERROR_V1
done
ps | grep "pidstat" | grep -v grep | awk '{ print $1 }' | while read pid;
do
    kill -SIGINT $pid
done



## v2
$PROFILE_PERFORM_SCRIPT $CMD_V2 > $SERVER_RESULT_V2 &
$PROFILE_PERFORM_SCRIPT $CMD_DB_V2 > $SERVER_RESULT_DB_V2 &
echo "TEST v2: "$SAME_NUM
COUNT_V2=0
while [ $COUNT_V2 -lt $MAX_COUNT ];
do
    COUNT_V2=`expr $COUNT_V2 + 1`
    echo 'Count: '$COUNT_V2
    node $NODE_SCRIPT_V2 $SAME_NUM 1>> $CLIENT_RESULT_V2  2>> $CLIENT_ERROR_V2
done
ps | grep "pidstat" | grep -v grep | awk '{ print $1 }' | while read pid;
do
    kill -SIGINT $pid
done

exit
