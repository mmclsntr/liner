import databasehelper as dbhelper
import configmanager

DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')
DB_COLLECTION_DEVICES = configmanager.get_key('DATABASE', 'DevicesCollection')

def list_devices():
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  listdevices = list(dbhelper.find(col, {}))
  return listdevices

def find_device_info(device_id: int):
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  listdevices = list(dbhelper.find(col, {'id': device_id}))
  return listdevices[0]

def add(self, configs: dict) -> dict:
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  configs['id'] = dbhelper.nextseq(col)
  result = dbhelper.insert(col, configs)
  return result

def update(self, device_id: int, configs: dict):
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  result = dbhelper.update(col, {"id": device_id}, configs)
  return result

def delete(self, device_id: int):
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
  result = dbhelper.delete(col, {"id": device_id})
