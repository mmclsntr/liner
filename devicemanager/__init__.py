import databasehelper as dbhelper
import configmanager
from bson.objectid import ObjectId

DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')
DB_COLLECTION_DEVICES = configmanager.get_key('DATABASE', 'DevicesCollection')

def list_devices():
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  listdevices = list(dbhelper.find(col, {}))
  return listdevices

def find_device_info(device_id):
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  listdevices = list(dbhelper.find(col, {'_id': ObjectId(device_id)}))
  return listdevices[0]

def add(self, configs: dict) -> dict:
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  result = dbhelper.insert(col, configs)
  return result

def update(self, device_id, configs: dict):
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  result = dbhelper.update(col, {"_id": ObjectId(device_id)}, configs)
  return result

def delete(self, device_id):
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  result = dbhelper.delete(col, {"_id": ObjectId(device_id)})
