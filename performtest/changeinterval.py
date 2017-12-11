import sys
sys.path.append('..')

import databasehelper
from bson.objectid import ObjectId
import configmanager 

def set_datastore_interval(interval):
  configmanager.set_value('INTERVALS', 'DatastoreInterval', interval)

def set_connector_interval(interval):
  configmanager.set_value('INTERVALS', 'RulebaseInterval', interval)

if __name__ == "__main__":
  argvs = sys.argv
  if len(argvs) < 2:
    print('Please set interval')
    exit(0)
  
  ditv = argvs[1]
  ritv = argvs[2]

  set_datastore_interval(ditv)
  set_connector_interval(ritv)
