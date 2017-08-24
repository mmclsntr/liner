import databasehelper
import devicemanager
import threading
import time

class DataCollectorThread(threading.Thread):
  def __init__(self, device_manager: devicemanager.DeviceManager, interval, dbname):
    super(DataCollectorThread, self).__init__()
    self.interval = interval
    self.__databasename = dbname
    self.__device_manager = device_manager
    self.__databasehelper = databasehelper.DataBaseHelper()

  def __collectdata(self):
    db = self.__databasehelper.get_database(self.__databasename)
    col = self.__databasehelper.get_collection(db, self.__device_manager.name)
    while self.__isrunning:
      readVal = self.__device_manager.read()
      doc = {'time': time.time(), 'value': readVal}
      self.__databasehelper.insert(col, doc)
      time.sleep(self.interval)

  def run(self):
    self.__isrunning = True
    self.__collectdata()

  def kill(self):
    self.__isrunning = False
