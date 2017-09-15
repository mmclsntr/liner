import databasehelper as dbhelper
import configmanager
from bson.objectid import ObjectId

DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')
DB_COLLECTION_DEVICES = configmanager.get_key('DATABASE', 'DevicesCollection')

def list_devices() -> list:
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  listdevices = list(dbhelper.find(col, {}))
  return listdevices

def find_device_info(device_id: str) -> dict:
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  listdevices = list(dbhelper.find(col, {'_id': ObjectId(device_id)}))
  return listdevices[0]

def add(info: dict) -> None:
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  result = dbhelper.insert(col, info)
  return result

def update(device_id: str, info: dict) -> None:
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  result = dbhelper.update(col, {"_id": ObjectId(device_id)}, info)
  return result

def delete(device_id: str) -> None:
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  result = dbhelper.delete(col, {"_id": ObjectId(device_id)})
