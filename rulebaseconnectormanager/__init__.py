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

  def run(self):
    self.__nodeconnectorthread = RuleBaseConnectorThread(self.__app_manager, 0.5, self.__dbname)
    self.__nodeconnectorthread.start()

  def kill(self):
    self.__nodeconnectorthread.kill()

  def find_rule(self, connector_id: int):
    db = self.__dbhelper.get_database(self.__dbname)
    col = self.__dbhelper.get_collection(db, DB_COLLECTION_RULES)
    rule = self.__dbhelper.find(col, {'id': connector_id})
    return rule[0]

  def list_rules(self):
    db = self.__dbhelper.get_database(self.__dbname)
    col = self.__dbhelper.get_collection(db, DB_COLLECTION_RULES)
    listrules = list(self.__dbhelper.find(col, {}))
    return listrules

  def add(self, configs: dict):
    db = self.__dbhelper.get_database(self.__dbname)
    col = self.__dbhelper.get_collection(db, DB_COLLECTION_RULES)
    configs['id'] = self.__dbhelper.nextseq(col)
    self.__dbhelper.insert(col, configs)

  def update(self, connector_id: int, configs: dict):
    db = self.__dbhelper.get_database(self.__dbname)
    col = self.__dbhelper.get_collection(db, DB_COLLECTION_RULES)
    self.__dbhelper.update(col, {'id': connector_id}, configs)

  def delete(self, connector_id):
    db = self.__dbhelper.get_database(self.__dbname)
    col = self.__dbhelper.get_collection(db, DB_COLLECTION_RULES)
    self.__dbhelper.delete(col, {'id': connector_id})
