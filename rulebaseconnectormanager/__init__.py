from rulebaseconnectorthread import RuleBaseConnectorThread
from appmanager import AppManager
from databasehelper import DataBaseHelper

DB_COLLECTION_RULES = 'rules'

class RuleBaseConnectorManager:
  __instance = None

  def __new__(cls, *args, **keys):
    if cls.__instance is None:
      cls.__instance = object.__new__(cls)
    return cls.__instance

  def __init__(self, app_manager: AppManager, dbname: str):
    self.__app_manager = app_manager
    self.__dbhelper = DataBaseHelper()
    self.__dbname = dbname
    self.__nodeconnectorthread = RuleBaseConnectorThread(app_manager, 0.5, dbname)
    #self.__nodeconnectorthread.start()

  def kill(self):
    self.__nodeconnectorthread.kill()

  def list_rules(self):
    db = self.__dbhelper.get_database(self.__dbname)
    col = self.__dbhelper.get_collection(db, DB_COLLECTION_RULES)
    listrules = list(self.__dbhelper.find(col, {}))
    print(listrules)
    return listrules
