from appmanager import AppManager
from rulebaseconnectormanager import RuleBaseConnectorManager
from devicemanager import DeviceManager
from webmanager import WebManager

import time

DB_NAME = 'dev'

class CentralManager:
  __instance = None

  def __new__(cls, *args, **keys):
    if cls.__instance is None:
      cls.__instance = object.__new__(cls)
    return cls.__instance

  def __init__(self):
    self.__appmanager = AppManager()
    self.__appmanager.set_dbname('dev')
    self.__devicemanager = DeviceManager(self.__appmanager, 'dev')
    self.__rulebaseconnectormanager = RuleBaseConnectorManager(self.__appmanager, 'dev')
    self.__webmanager = WebManager('dev')

  def run(self):
    self.__appmanager.load_localapps()
    print('Locaded apps')
    time.sleep(3)
    print('rulebase')
    self.__rulebaseconnectormanager.run()
    print('webmanager')
    self.__webmanager.run(True)

  def destroy(self):
    self.__appmanager.unload_localapps()
    self.__rulebaseconnectormanager.kill()
