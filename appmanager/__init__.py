import importlib
import databasehelper
from typing import Any
import logging
import os
import shutil

from apps.node import Node
from datastoremanager import DataStoreManager

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

  def __init__(self):
    logging.basicConfig(level=logging.DEBUG)
    self.__databasehelper = databasehelper.DataBaseHelper()
    self.__datastoremanager = DataStoreManager('dev')

  def set_dbname(self, dbname: str):
    self.__dbname = dbname

  def load_localapps(self) -> dict:
    self.__apps = {}
    listapps = self.list_localapps()
    for listapp in listapps:
      self.__load_localapp(int(listapp['id']))

  def __load_localapp(self, localapp_id):
    listapp = self.find_localapp_info(localapp_id)
    app_module = importlib.import_module('apps.' + listapp['module_name'])
    # Rearrenge configs
    configs = {}
    for config in listapp['configs']:
      configs[config['name']] = eval(config['type'])(config['value'])
    #print(configs)
    app = app_module.NodeAppMain(configs)
    self.__apps[int(localapp_id)] = app
    self.__datastoremanager.run_datastorer(localapp_id, listapp['name'], app)
    logging.debug('load local app: ' + str(listapp))

  def unload_localapps(self):
    listapps = self.list_localapps()
    for listapp in listapps:
      self.__unload_localapp(int(listapp['id']))

  def __unload_localapp(self, localapp_id):
    self.__apps[int(localapp_id)] = None
    del self.__apps[int(localapp_id)]
    self.__datastoremanager.kill_datastorer(localapp_id)
    logging.debug('unload local app: ' + str(localapp_id))

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
    self.__load_localapp(configs['id'])
    # Add app file
    # TODO: Nest version for app store on cloud
    return result

  def delete(self, localapp_id: int) -> bool:
    db = self.__databasehelper.get_database(self.__dbname)
    col = self.__databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
    result = self.__databasehelper.delete(col, {'id': localapp_id})
    self.__unload_localapp(localapp_id)
    return True

  def update_app_info(self, localapp_id: int, configs: dict) -> bool:
    # Add info
    db = self.__databasehelper.get_database(self.__dbname)
    col = self.__databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
    result = self.__databasehelper.update(col, {'id': localapp_id}, configs)
    self.__load_localapp(localapp_id)
    # Add app file
    # TODO: Nest version for app store on cloud
    return True

  def read_app_value(self, localapp_id: int) -> Any:
    readvalue = self.__apps[localapp_id].read()
    return readvalue

  def write_app_value(self, localapp_id: int, value: Any) -> Any:
    self.__apps[localapp_id].write(value)
