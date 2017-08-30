from datastoremanager import DataStoreManager
from nodeconnectormanager import NodeConnectorManager
from appmanager import AppManager

DB_NAME = 'dev'

class CentralManager:
  __instance = None

  def __new__(cls, *args, **keys):
    if cls.__instance is None:
      cls.__instance = object.__new__(cls)
    return cls.__instance

  def __init__(self):
    self.__appmanager = AppManager('dev')
    #apps = appmanager.get_localapps()
    #for app in apps.values():
    #  print(app)
    self.__datastoremanager = DataStoreManager(self.__appmanager, 'dev')
    self.__nodeconnectormanager = NodeConnectorManager(self.__appmanager, 'dev')

  def destroy(self):
    self.__datastoremanager.killall()
    self.__nodeconnectormanager.kill()
