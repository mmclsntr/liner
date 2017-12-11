#!/bin/bash

for i in {1..20} ;
do
  for num in 1 5 10 20 50 80 100 150 200 ; 
  do
    for interval in 0.5 1 2 ;
     do
      echo "Count: "$i"  Number: "$num"  Interval: "$interval
      ./test.sh $num 0 $interval
    done
  done
done

