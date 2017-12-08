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

def calc_avg(filename):
  interval=0
  count=0
  dif=0
  cnt=0
  with open(filename, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
      interval += float(row[0])
      count += float(row[1])
      dif += float(row[3])
      cnt += 1

  return {"interval": interval / cnt, "count": count / cnt, "dif": dif / cnt}


if __name__ == "__main__":
# Arguments
# data numbers and connecting mode (0: neighbors, 1: chains)
  argvs = sys.argv
  if len(argvs) < 2:
    print('Please set filename')
    exit(0)
  
  rstfile = argvs[1]

  res = calc_avg(rstfile)

  print(str(res["interval"]) + ',' + str(res["count"]) + ',' + str(INTERVAL) + ',' + str(res["dif"]))
