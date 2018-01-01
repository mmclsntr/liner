#!/bin/bash

for connector in 1 10 20 30 40 50 ; 
do
  for interval in 0.5 1.5 1 2 ;
   do
    DIRNAME="result_100_"$interval"_"$connector"_"
    ls | grep $DIRNAME | head -n 5 | while read dir
    do
      echo $dir
      rm -r $dir
    done
  done
done
# Connectors doesn't exist
for num in 1 10 50 100 150 200 250 ; 
do
  for interval in 0.5 1.5 1 2 ;
   do
    DIRNAME="result_"$num"_"$interval"_0_"
    ls | grep $DIRNAME | head -n 5 | while read dir
    do
      echo $dir
      rm -r $dir
    done
  done
done
