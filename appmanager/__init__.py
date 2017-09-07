import importlib
import databasehelper
from typing import Any
import logging
import os
import shutil

DB_COLLECTION_LOCALAPPS = 'local_apps'
DB_COLLECTION_GLOBALAPPS = 'global_apps'
DIR_APP_STORE = 'appstore'
DIR_APPS = 'apps'

class AppManager:
  __instance = None

  def __new__(cls, *args, **keys):
    if cls.__instance is None:
      cls.__instance = object.__new__(cls)
    return cls.__instance

  def __init__(self, dbname: str):
    logging.basicConfig(level=logging.DEBUG)
    self.__dbname = dbname
    self.__databasehelper = databasehelper.DataBaseHelper()
    self.__apps = self.__load_localapps()

  def __load_localapps(self) -> dict:
    apps = {}
    listapps = self.list_localapps()
    _debug_listapps = ""
    for listapp in listapps:
      app_module = importlib.import_module('apps.' + listapp['module_name'])
      # Rearrenge configs
      configs = {}
      for config in listapp['configs']:
        configs[config['name']] = eval(config['type'])(config['value'])
      #print(configs)
      apps[int(listapp['id'])] = app_module.NodeAppMain(configs)
      _debug_listapps += "\n" + str(listapp)
    logging.debug('local apps: ' + _debug_listapps)
    return apps

  def get_localapps(self) -> dict:
    return self.__apps

  def get_localapp(self, _id: int) -> Any:
    return self.__apps[_id]

  def list_localapps(self) -> list:
    db = self.__databasehelper.get_database(self.__dbname)
    col = self.__databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
    listapps = list(self.__databasehelper.find(col, {}))
    return listapps

  def list_globalapps(self) -> list:
    db = self.__databasehelper.get_database(self.__dbname)
    col = self.__databasehelper.get_collection(db, DB_COLLECTION_GLOBALAPPS)
    listapps = list(self.__databasehelper.find(col, {}))
    return listapps

  def find_globalapp_info(self, globalapp_id) -> dict:
    db = self.__databasehelper.get_database(self.__dbname)
    col = self.__databasehelper.get_collection(db, DB_COLLECTION_GLOBALAPPS)
    appinfo = list(self.__databasehelper.find(col, {'id': globalapp_id}))
    return appinfo[0]
  
  def find_localapp_info(self, localapp_id: int) -> dict:
    db = self.__databasehelper.get_database(self.__dbname)
    col = self.__databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
    appinfo = list(self.__databasehelper.find(col, {'id': localapp_id}))
    return appinfo[0]

  def find_localapp_info_with_deviceid(self, device_id: int) -> dict:
    db = self.__databasehelper.get_database(self.__dbname)
    col = self.__databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
    appinfo = list(self.__databasehelper.find(col, {'device_id': device_id}))
    return appinfo[0]
  
  def find_localapp_id_from_name(self, name: str) -> int:
    db = self.__databasehelper.get_database(self.__dbname)
    col = self.__databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
    listapps = list(self.__databasehelper.find(col, {'name': name}))
    localapp_id = listapps[0]['id']
    return int(localapp_id)

  def find_localapp_name_from_id(self, _id: int) -> str:
    db = self.__databasehelper.get_database(self.__dbname)
    col = self.__databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
    listapps = list(self.__databasehelper.find(col, {'id': _id}))
    localapp_name = listapps[0]['name']
    return localapp_name

  def add(self, globalapp_id: int, configs: dict) -> dict:
    # Add info
    db = self.__databasehelper.get_database(self.__dbname)
    col = self.__databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
    configs['id'] = self.__databasehelper.nextseq(col)
    globalapp_info = self.find_globalapp_info(globalapp_id)
    configs['module_name'] = globalapp_info['module_name']
    configs['global_app_id'] = globalapp_id
    result = self.__databasehelper.insert(col, configs)
    # Add app file
    # TODO: Nest version for app store on cloud
    return result

  def delete(self, localapp_id: int) -> bool:
    db = self.__databasehelper.get_database(self.__dbname)
    col = self.__databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
    result = self.__databasehelper.delete(col, {'id': localapp_id})
    return True

  def update_app_info(self, localapp_id: int, configs: dict) -> bool:
    # Add info
    db = self.__databasehelper.get_database(self.__dbname)
    col = self.__databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
    result = self.__databasehelper.update(col, {'id': localapp_id}, configs)
    # Add app file
    # TODO: Nest version for app store on cloud
    return True

  def read_app_value(self, localapp_id: int) -> Any:
    readvalue = self.__apps[localapp_id].read()
    return readvalue

  def write_app_value(self, localapp_id: int, value: Any) -> Any:
    self.__apps[localapp_id].write(value)
