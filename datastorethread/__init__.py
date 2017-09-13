import databasehelper
import threading
import time
from apps.node import Node

import configmanager

DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')
DB_COLLECTION_TEMP_DATASTORE = configmanager.get_key('DATABASE', 'DataStoreCollectionTemp')

class DataStoreThread(threading.Thread):
  def __init__(self, node: Node, node_id,  interval: float):
    super(DataStoreThread, self).__init__()
    self.interval = interval
    self.__node = node
    self.__id = node_id

  def __store(self):
    db = databasehelper.get_database(DB_NAME)
    col = databasehelper.get_collection(db, DB_COLLECTION_TEMP_DATASTORE + str(self.__id))
    while self.__isrunning:
      readVal = self.__node.read()
      #print(readVal)
      doc = {'time': time.time(), 'value': readVal}
      databasehelper.insert(col, doc)
      time.sleep(self.interval)

  def run(self):
    self.__isrunning = True
    self.__store()

  def kill(self):
    self.__isrunning = False
