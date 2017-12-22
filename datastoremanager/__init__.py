from bson.objectid import ObjectId
import pymongo

import databasehelper
import threading
import time
from nodes.node import Node
import configmanager
import logmanager

DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')
DB_COLLECTION_TEMP_DATASTORE = configmanager.get_key('DATABASE', 'DataStoreCollectionTemp')

INTERVAL = float(configmanager.get_key('INTERVALS', 'DatastoreInterval'))

TAG = 'DataStoreManager'

class DataStoreThread(threading.Thread):
  def __init__(self, node: Node, node_id: str) -> None:
    super(DataStoreThread, self).__init__()
    self.interval = INTERVAL
    self.__node = node
    self.__id = node_id

  def __store(self) -> None:
    db = databasehelper.get_database(DB_NAME)
    colname = DB_COLLECTION_TEMP_DATASTORE + str(self.__id)
    if not databasehelper.isExistCollection(db, colname):
      col = databasehelper.create_collection(db, colname)
    else:
      col = databasehelper.get_collection(db, colname)
    while self.__isrunning:
      try:
        readVal = self.__node.read()
        doc = {'time': time.time(), 'value': readVal}
        databasehelper.insert(col, doc)
        time.sleep(self.interval)
      except:
        logmanager.error(TAG, sys.exc_info())

  def run(self) -> None:
    self.__isrunning = True
    self.__store()

  def kill(self) -> None:
    self.__isrunning = False

  def is_running() -> bool:
    return self.__isrunning




data_stores = {}

def run_datastorer(node_id: str, node: Node) -> None:
  datastorethread = DataStoreThread(node, node_id)
  datastorethread.start()
  data_stores[node_id] = datastorethread

def is_running(node_id: str) -> bool:
  if node_id in data_stores:
    return data_stores[node_id].is_running()
  else:
    return False

def kill_datastorer(node_id: str) -> None:
  if node_id in data_stores:
    data_stores[node_id].kill()
    data_stores[node_id] = None
    del data_stores[node_id]

def killall() -> None:
  for node_id in data_stores.keys():
    kill_datastorer(node_id)

def remove_datastore(node_id: str) -> None:
  colname = DB_COLLECTION_TEMP_DATASTORE + str(node_id)
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, colname)
  databasehelper.drop(col)

def find_datastore_values(node_id: str, limit: int) -> list:
  colname = DB_COLLECTION_TEMP_DATASTORE + str(node_id)
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, colname)
  values = list(databasehelper.find(col, {}, {'sort': [('time', -1)], 'limit': limit, 'projection': {'_id': False}}))
  return values
  
