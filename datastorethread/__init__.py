import databasehelper
import threading
import time
from appmanager import AppManager

class DataStoreThread(threading.Thread):
  def __init__(self, appmanager: AppManager, app_id: int,  interval: float, dbname: str):
    super(DataStoreThread, self).__init__()
    self.interval = interval
    self.__app_id = app_id
    self.__dbname = dbname
    self.__databasehelper = databasehelper.DataBaseHelper()
    self.__appmanager = appmanager

  def __store(self):
    db = self.__databasehelper.get_database(self.__dbname)
    appname = self.__appmanager.find_localapp_name_from_id(self.__app_id)
    col = self.__databasehelper.get_collection(db, appname)
    while self.__isrunning:
      readVal = self.__appmanager.read_app_value(self.__app_id)
      #print(readVal)
      doc = {'time': time.time(), 'value': readVal}
      self.__databasehelper.insert(col, doc)
      time.sleep(self.interval)

  def run(self):
    self.__isrunning = True
    self.__store()

  def kill(self):
    self.__isrunning = False
