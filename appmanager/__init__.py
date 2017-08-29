import importlib
import databasehelper
from typing import Any

DB_COLLECTION_APPS = 'local_apps'

class AppManager:
  __instance = None

  def __new__(cls, *args, **keys):
    if cls.__instance is None:
      cls.__instance = object.__new__(cls)
    return cls.__instance

  def __init__(self, dbname: str):
    self.__dbname = dbname
    self.__databasehelper = databasehelper.DataBaseHelper()
    self.__apps = self.__load_localapps()

  def __load_localapps(self) -> dict:
    apps = {}
    listapps = self.list_localapps()
    for listapp in listapps:
      app_module = importlib.import_module('apps.' + listapp['module_name'])
      # Rearrenge configs
      configs = {}
      for config in listapp['configs']:
        configs[config['name']] = eval(config['type'])(config['value'])
      print(configs)
      apps[listapp['id']] = app_module.NodeAppMain(configs)
    return apps

  def get_localapps(self) -> dict:
    return self.__apps

  def list_localapps(self) -> list:
    db = self.__databasehelper.get_database(self.__dbname)
    col = self.__databasehelper.get_collection(db, DB_COLLECTION_APPS)
    listapps = list(self.__databasehelper.find(col, {}))
    return listapps
    

  def list_globalapps(self) -> list:
    pass

  def find_globalapp_info(self, globalapp_id) -> dict:
    pass
  
  def find_localapp_info(self, localapp_id: int) -> dict:
    pass

  def add(self, globalapp_id: int, config: dict) -> dict:
    pass

  def delete(self, localapp_id: int) -> bool:
    pass

  def edit_app_info(self, localapp_id: int) -> bool:
    pass

  def read_app_value(self, localapp_id: int) -> Any:
    pass

  def write_app_value(self, localapp_id: int) -> Any:
    pass
