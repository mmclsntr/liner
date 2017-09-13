import importlib
from typing import Any
import logging
import os
import shutil

from apps.node import Node
import datastoremanager
import databasehelper
import configmanager

DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')
DB_COLLECTION_LOCALAPPS = configmanager.get_key('DATABASE', 'LocalappsCollection')
DB_COLLECTION_GLOBALAPPS = configmanager.get_key('DATABASE', 'GlobalappsCollection')
DIR_APPS = configmanager.get_key('PATHS', 'DirApps')

logging.basicConfig(level=logging.DEBUG)

__apps = {}

def load_localapps():
  listapps = list_localapps()
  for listapp in listapps:
    __load_localapp(int(listapp['id']))

def __load_localapp(localapp_id):
  listapp = find_localapp_info(localapp_id)
  app_module = importlib.import_module('apps.' + listapp['module_name'])
  # Rearrenge configs
  configs = {}
  for config in listapp['configs']:
    configs[config['name']] = eval(config['type'])(config['value'])
  #print(configs)
  app = app_module.NodeAppMain(configs)
  __apps[int(localapp_id)] = app
  datastoremanager.run_datastorer(localapp_id, listapp['name'], app)
  logging.debug('load local app: ' + str(listapp))

def unload_localapps():
  listapps = list_localapps()
  for listapp in listapps:
    __unload_localapp(int(listapp['id']))

def __unload_localapp(localapp_id):
  __apps[int(localapp_id)] = None
  del __apps[int(localapp_id)]
  datastoremanager.kill_datastorer(localapp_id)
  logging.debug('unload local app: ' + str(localapp_id))

def list_localapps() -> list:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
  listapps = list(databasehelper.find(col, {}))
  return listapps

def list_globalapps() -> list:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_GLOBALAPPS)
  listapps = list(databasehelper.find(col, {}))
  return listapps

def find_globalapp_info(globalapp_id) -> dict:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_GLOBALAPPS)
  appinfo = list(databasehelper.find(col, {'id': globalapp_id}))
  return appinfo[0]

def find_localapp_info(localapp_id) -> dict:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
  appinfo = list(databasehelper.find(col, {'id': localapp_id}))
  return appinfo[0]

def find_localapp_info_with_deviceid(device_id: int) -> dict:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
  appinfo = list(databasehelper.find(col, {'device_id': device_id}))
  return appinfo[0]

def add(globalapp_id: int, configs: dict) -> dict:
  # Add info
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
  configs['id'] = databasehelper.nextseq(col)
  globalapp_info = find_globalapp_info(globalapp_id)
  configs['module_name'] = globalapp_info['module_name']
  configs['global_app_id'] = globalapp_id
  result = databasehelper.insert(col, configs)
  __load_localapp(configs['id'])
  # Add app file
  # TODO: Nest version for app store on cloud
  return result

def delete(localapp_id: int) -> bool:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
  result = databasehelper.delete(col, {'id': localapp_id})
  __unload_localapp(localapp_id)
  return True

def update_app_info(localapp_id: int, configs: dict) -> bool:
  # Add info
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
  result = databasehelper.update(col, {'id': localapp_id}, configs)
  __load_localapp(localapp_id)
  # Add app file
  # TODO: Nest version for app store on cloud
  return True

def read_app_value(localapp_id: int) -> Any:
  readvalue = __apps[localapp_id].read()
  return readvalue

def write_app_value(self, localapp_id: int, value: Any) -> Any:
  __apps[localapp_id].write(value)
