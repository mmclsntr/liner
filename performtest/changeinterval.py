import sys
sys.path.append('..')

import databasehelper
from bson.objectid import ObjectId
import configmanager 

def set_interval(interval):
  configmanager.set_value('INTERVALS', 'DatastoreInterval', interval)


if __name__ == "__main__":
  argvs = sys.argv
  if len(argvs) < 2:
    print('Please set interval')
    exit(0)
  
  itv = argvs[1]

  set_interval(itv)
