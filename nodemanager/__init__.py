import importlib
import logging
import os
import shutil
from bson.objectid import ObjectId

from nodes.node import Node
import datastoremanager
import databasehelper
import configmanager

DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')
DB_COLLECTION_nodeS = configmanager.get_key('DATABASE', 'nodescollection')
DB_COLLECTION_node_moduleS = configmanager.get_key('DATABASE', 'nodemodulescollection')
DIR_nodeS = configmanager.get_key('PATHS', 'Dirnodes')

logging.basicConfig(level=logging.DEBUG)

__nodes = {}

def load_nodes():
  listnodes = list_nodes()
  for listnode in listnodes:
    __load_node(str(listnode['_id']))

def __load_node(node_id: str):
  listnode = find_node_info(node_id)
  node_module = importlib.import_module('nodes.' + listnode['module_name'])
  # Rearrenge configs
  configs = {}
  for config in listnode['configs']:
    configs[config['name']] = eval(config['type'])(config['value'])
  #try:
  node = node_module.NodeAppMain(configs)
  __nodes[node_id] = node
  datastoremanager.run_datastorer(node_id, node)
  logging.debug('load local node: ' + str(listnode))
  #except:
    #logging.error('load local node error: ' + str(listnode))
    

def unload_nodes():
  listnodes = list_nodes()
  for listnode in listnodes:
    __unload_node(str(listnode['_id']))

def __unload_node(node_id: str):
  if node_id in __nodes:
    __nodes[node_id] = None
    del __nodes[node_id]
    datastoremanager.kill_datastorer(node_id)
    logging.debug('unload local node: ' + str(node_id))

def list_nodes() -> list:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_nodeS)
  listnodes = list(databasehelper.find(col, {}))
  return listnodes

def list_node_modules() -> list:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_node_moduleS)
  listnodes = list(databasehelper.find(col, {}))
  return listnodes

def find_node_info(node_id: str) -> dict:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_nodeS)
  nodeinfo = list(databasehelper.find(col, {'_id': ObjectId(node_id)}))
  return nodeinfo[0]

def find_node_module_info(node_module_id: str) -> dict:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_node_moduleS)
  nodeinfo = list(databasehelper.find(col, {'_id': ObjectId(node_module_id)}))
  return nodeinfo[0]

def add(node_module_id: str, new_node: dict) -> None:
  # Add info
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_nodeS)
  node_module_info = find_node_module_info(node_module_id)
  new_node['module_name'] = node_module_info['module_name']
  new_node['global_node_id'] = node_module_id
  if '_id' in new_node:
    new_node["_id"] = ObjectId(new_node["_id"])
  result = databasehelper.insert(col, new_node)
  __load_node(str(new_node['_id']))
  # Add node file
  # TODO: Nest version for node store on cloud

def delete(node_id: str) -> None:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_nodeS)
  result = databasehelper.delete(col, {'_id': ObjectId(node_id)})
  __unload_node(node_id)
  datastoremanager.remove_datastore(node_id)
  return True

def update_node_info(node_id: str, updated_node: dict) -> None:
  # Add info
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_nodeS)
  result = databasehelper.update(col, {'_id': ObjectId(node_id)}, updated_node)
  __load_node(node_id)
  # Add node file
  # TODO: Nest version for node store on cloud

def read_node_value(node_id: str):
  #try:
    readvalue = __nodes[node_id].read()
    return readvalue
  #except:
  #  logging.error('read error: ' + node_id)
    

def write_node_value(node_id, value) -> None:
  try:
    __nodes[node_id].write(value)
  except:
    logging.error('write error: ' + node_id)

def datastore(node_id: str, num: int) -> list:
  return datastoremanager.find_datastore_values(node_id, num)
  
