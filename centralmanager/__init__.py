from datastoremanager import DataStoreManager
from rulebaseconnectormanager import RuleBaseConnectorManager
from appmanager import AppManager
from devicemanager import DeviceManager

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
    self.__devicemanager = DevicdeManager(self.__appmanager, 'dev')
    self.__datastoremanager = DataStoreManager(self.__appmanager, 'dev')
    self.__rulebaseconnectormanager = RuleBaseConnectorManager(self.__appmanager, 'dev')

  def destroy(self):
    self.__datastoremanager.killall()
    self.__rulebaseconnectormanager.kill()
