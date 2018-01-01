#!/bin/bash

for i in {1..100} ;
do
# Connectors exist
  for connector in 1 10 20 30 40 50 ; 
  do
    for interval in 0.5 1.5 1 2 ;
     do
      echo "Count: "$i"  Connector: "$connector"  Interval: "$interval
      ./test.sh 100 $interval $connector
    done
  done

# Connectors doesn't exist
  for num in 1 10 50 100 150 200 250 ; 
  do
    for interval in 0.5 1.5 1 2 ;
     do
      echo "Count: "$i"  Number: "$num"  Interval: "$interval
      ./test.sh $num $interval 0
    done
  done
done

