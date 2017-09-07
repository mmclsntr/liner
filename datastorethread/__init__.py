import databasehelper
import threading
import time
from apps.node import Node

class DataStoreThread(threading.Thread):
  def __init__(self, node: Node, name: str,  interval: float, dbname: str):
    super(DataStoreThread, self).__init__()
    self.interval = interval
    self.__dbname = dbname
    self.__databasehelper = databasehelper.DataBaseHelper()
    self.__node = node
    self.__name = name

  def __store(self):
    db = self.__databasehelper.get_database(self.__dbname)
    appname = self.__name
    col = self.__databasehelper.get_collection(db, appname)
    while self.__isrunning:
      readVal = self.__node.read()
      #print(readVal)
      doc = {'time': time.time(), 'value': readVal}
      self.__databasehelper.insert(col, doc)
      time.sleep(self.interval)

  def run(self):
    self.__isrunning = True
    self.__store()

  def kill(self):
    self.__isrunning = False
