import databasehelper as dbhelper
import configmanager
import appmanager
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
  if "_id" in info:
    info["_id"] = ObjectId(info["_id"])
  result = dbhelper.insert(col, info)
  return result

def update(device_id: str, info: dict) -> None:
  if "_id" in info:
    del info["_id"]
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  result = dbhelper.update(col, {"_id": ObjectId(device_id)}, info)
  return result

def delete(device_id: str) -> None:
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  result = dbhelper.delete(col, {"_id": ObjectId(device_id)})
  return result

def delete_appid(device_id: str, localapp_id: str) -> None:
  device = find_device_info(device_id)
  device["apps"].remove(localapp_id)
  print(device)
  update(device_id, device)
  
def delete_apps(device_id: str) -> None:
  device = find_device_info(device_id)
  for app in device["apps"]:
    appmanager.delete(app)
    delete_appid(device_id, app)
