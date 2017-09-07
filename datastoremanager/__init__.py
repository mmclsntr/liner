from datastorethread import DataStoreThread
from appmanager import AppManager

class DataStoreManager:
  __instance = None

  def __new__(cls, *args, **keys):
    if cls.__instance is None:
      cls.__instance = object.__new__(cls)
    return cls.__instance
  
  def __init__(self, app_manager: AppManager, dbname: str):
    self.__app_manager = app_manager
    self.data_stores = {}
    self.__dbname = dbname

  def run(self):
    listapps = self.__app_manager.list_localapps()
    for listapp in listapps:
      _id = listapp['id']
      datastorethread = DataStoreThread(self.__app_manager, _id, 1.0, self.__dbname)
      datastorethread.start()
      self.data_stores[_id] = datastorethread

  def killall(self):
    for datastore in self.data_stores.values():
      datastore.kill()

