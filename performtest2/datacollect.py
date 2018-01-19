import sys
sys.path.append('..')

import databasehelper
from bson.objectid import ObjectId
import configmanager 

DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')
DB_COLLECTION_TEMP_DATASTORE = configmanager.get_key('DATABASE', 'DataStoreCollectionTemp')

def get_data(node_id):
  colname = DB_COLLECTION_TEMP_DATASTORE + str(node_id)
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, colname)
  values = list(databasehelper.find(col, {}, {'sort': [('time', 1)], 'projection': {'_id': False}}))
  return values

def drop_collection(node_id):
  colname = DB_COLLECTION_TEMP_DATASTORE + str(node_id)
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, colname)
  databasehelper.drop(col)

if __name__ == "__main__":
# Arguments
# data numbers and connecting mode (0: neighbors, 1: chains)
  argvs = sys.argv
  if len(argvs) < 2:
    print('Please set app id')
    exit(0)

  app_id = argvs[1]
  values = get_data(app_id)
  for value in values:
    print(str(value["time"]) + "," + str(value["value"])) 
  drop_collection(app_id)
