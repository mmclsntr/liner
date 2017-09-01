from appmanager import AppManager
import databasehelper

DB_COLLECTION_DEVICES = 'devices'

class DeviceManager:
  __instance = None

  def __new__(cls, *args, **keys):
    if cls.__instance is None:
      cls.__instance = object.__new__(cls)
    return cls.__instance

  def __init__(self, appmanager: AppManager, dbname: str):
    self.__dbname = dbname
    self.__appmanager = appmanager
    self.__dbhelper = databasehelper.DataBaseHelper()

  def list_devices(self):
    db = self.__dbhelper.get_database(self.__dbname)
    col = self.__dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
    listdevices = list(self.__dbhelper.find(col, {}))
    return listdevices

  def find_device_info(self, device_id: int):
    db = self.__dbhelper.get_database(self.__dbname)
    col = self.__dbhelper.get_collection(db, DB_COLLECTION_DEVICES)
    listdevices = list(self.__dbhelper.find(col, {'id': device_id}))
    return listdevices[0]
