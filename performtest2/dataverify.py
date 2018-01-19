import sys
import csv
sys.path.append('..')

import databasehelper
from bson.objectid import ObjectId
import configmanager 


DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')
DB_COLLECTION_LOCALAPPS = configmanager.get_key('DATABASE', 'LocalappsCollection')
DB_COLLECTION_GLOBALAPPS = configmanager.get_key('DATABASE', 'GlobalappsCollection')
DB_COLLECTION_RULES = configmanager.get_key('DATABASE', 'RulesCollection')
DB_COLLECTION_DEVICES = configmanager.get_key('DATABASE', 'DevicesCollection')
DB_COLLECTION_TEMP_DATASTORE = configmanager.get_key('DATABASE', 'DataStoreCollectionTemp')

INTERVAL = float(configmanager.get_key('INTERVALS', 'DatastoreInterval'))

def check_interval_and_count(filename):
  intervals = []
  count = 0
  with open(filename, 'r') as f:
    reader = csv.reader(f)
    time1 = None
    time2 = None
    for row in reader:
      if time1 == None:
        time1 = float(row[0])
      else:
        time2 = float(row[0])
        interval = time2 - time1
        intervals.append(interval)
        time1 = time2
      count += 1

    return {"intervals": intervals, "count": count}


if __name__ == "__main__":
# Arguments
# data numbers and connecting mode (0: neighbors, 1: chains)
  argvs = sys.argv
  if len(argvs) < 2:
    print('Please set 2 files')
    exit(0)
  
  log_1 = argvs[1]
  log_2 = argvs[2]

  print(log_1)   
  res1 = check_interval_and_count(log_1)
  sum1 = 0
  cnt1 = 0
  avg1 = 0
  for interval in res1["intervals"]:
    print(str(cnt1) + "\t" + str(interval) + "\t" + str(interval - INTERVAL))
    sum1 += interval
    cnt1 += 1
  avg1 = sum1 / cnt1
  print("Avg. " + "\t" + str(avg1) + "\t" + str(avg1 - INTERVAL))
  print("Count. " + "\t" + str(res1["count"]))

  print(log_2)   
  res2 = check_interval_and_count(log_2)
  sum2 = 0
  cnt2 = 0
  avg2 = 0
  for interval in res2["intervals"]:
    print(str(cnt2) + "\t" + str(interval) + "\t" + str(interval - INTERVAL))
    sum2 += interval
    cnt2 += 1
  avg2 = sum2 / cnt2
  print("Avg." + "\t" + str(avg2) + "\t" + str(avg2 - INTERVAL))
  print("Count." + "\t" + str(res2["count"]))
