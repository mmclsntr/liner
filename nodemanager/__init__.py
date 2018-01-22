import importlib
import os
import sys
import shutil
from bson.objectid import ObjectId

from nodes.node import Node
import datastoremanager
import databasehelper
import configmanager
import logmanager

DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')
DB_COLLECTION_NODES = configmanager.get_key('DATABASE', 'nodescollection')
DB_COLLECTION_NODE_MODULES = configmanager.get_key('DATABASE', 'nodemodulescollection')
DB_COLLECTION_PARENT_NODE_MODULES = configmanager.get_key('DATABASE', 'parentnodemodulescollection')
DB_COLLECTION_PARENT_NODES = configmanager.get_key('DATABASE', 'parentnodescollection')
DIR_NODES = configmanager.get_key('PATHS', 'Dirnodes')

TAG = 'NodeManager'

__nodes = {}
__parent_nodes = {}

sys.path.append(os.getcwd() + '/nodes')

def load_nodes():
  listnodes = list_nodes()
  for listnode in listnodes:
    __load_node(str(listnode['_id']))

def __load_node(node_id: str):
  listnode = find_node_info(node_id)
  # Import parent node module
  parent_node = None
  if 'parent_module_name' in listnode and listnode['parent_module_name'] != '' and listnode['parent_module_name'] != None:
    parent_module_name = listnode['parent_module_name']
    listparentmodules = find_parent_node_module_info_list_w_name(parent_module_name)
    listparentmodule = listparentmodules[0]
    parent_module_id = str(listparentmodule['_id'])
    if parent_module_id in __parent_nodes:
      parent_node = __parent_nodes[parent_module_id]
    else:
      parent_module = importlib.import_module(parent_module_name)
      listparentnodes = find_parent_node_info_list_w_module_id(parent_module_id)
      listparentnode = listparentnodes[0]
      configs = {}
      for config in listparentnode['configs']:
        configs[config['name']] = eval(config['type'])(config['value'])
      try:
        parent_node = parent_module.ParentMain(configs)
        __parent_nodes[parent_module_id] = parent_node
        logmanager.log(TAG, 'Loaded parent node: ' + str(listparentnode))
      except:
        logmanager.error(TAG, sys.exc_info())
  # Import node module
  node_module = importlib.import_module(listnode['module_name'])
  # Rearrenge configs
  configs = {}
  for config in listnode['configs']:
    configs[config['name']] = eval(config['type'])(config['value'])
  try:
    node = node_module.NodeMain(configs, parent=parent_node)
    __nodes[node_id] = node
    # Load datastore
    if 'readtype' in listnode:
      datastoremanager.run_datastorer(node_id, node)
    logmanager.log(TAG, 'Loaded node: ' + str(listnode))
  except:
    logmanager.error(TAG, sys.exc_info())

def unload_nodes():
  listnodes = list_nodes()
  for listnode in listnodes:
    __unload_node(str(listnode['_id']))

def __unload_node(node_id: str):
  if node_id in __nodes:
    __nodes[node_id] = None
    del __nodes[node_id]
    datastoremanager.kill_datastorer(node_id)
    logmanager.log(TAG, 'Unloaded node: ' + str(listnode))

def list_nodes() -> list:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_NODES)
  listnodes = list(databasehelper.find(col, {}))
  return listnodes

def list_node_modules() -> list:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_NODE_MODULES)
  listnodes = list(databasehelper.find(col, {}))
  return listnodes

def find_node_info(node_id: str) -> dict:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_NODES)
  nodeinfo = list(databasehelper.find(col, {'_id': ObjectId(node_id)}))
  return nodeinfo[0]

def find_parent_node_info(node_id: str) -> dict:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_PARENT_NODES)
  nodeinfo = list(databasehelper.find(col, {'_id': ObjectId(node_id)}))
  return nodeinfo[0]

def find_parent_node_info_list_w_module_id(parent_module_id: str) -> list:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_PARENT_NODES)
  nodeinfo = list(databasehelper.find(col, {'parent_node_module_id': parent_module_id}))
  return nodeinfo

def find_node_module_info(node_module_id: str) -> dict:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_NODE_MODULES)
  nodeinfo = list(databasehelper.find(col, {'_id': ObjectId(node_module_id)}))
  return nodeinfo[0]

def find_parent_node_module_info(node_module_id: str) -> dict:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_PARENT_NODE_MODULES)
  nodeinfo = list(databasehelper.find(col, {'_id': ObjectId(node_module_id)}))
  return nodeinfo[0]

def find_parent_node_module_info_list_w_name(parent_module_name: str) -> list:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_PARENT_NODE_MODULES)
  nodeinfo = list(databasehelper.find(col, {'module_name': parent_module_name}))
  return nodeinfo
  


def add(node_module_id: str, new_node: dict) -> None:
  # Add info
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_NODES)
  node_module_info = find_node_module_info(node_module_id)
  new_node['module_name'] = node_module_info['module_name']
  new_node['node_module_id'] = node_module_id
  if '_id' in new_node:
    new_node["_id"] = ObjectId(new_node["_id"])
  result = databasehelper.insert(col, new_node)
  __load_node(str(new_node['_id']))

def delete(node_id: str) -> None:
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_NODES)
  result = databasehelper.delete(col, {'_id': ObjectId(node_id)})
  __unload_node(node_id)
  datastoremanager.remove_datastore(node_id)
  return True

def update_node_info(node_id: str, updated_node: dict) -> None:
  # Add info
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_NODES)
  result = databasehelper.update(col, {'_id': ObjectId(node_id)}, updated_node)
  __load_node(node_id)

def read_node_value(node_id: str):
  try:
    readvalue = __nodes[node_id].read()
    return readvalue
  except:
    logmanager.error(TAG, sys.exc_info())
    

def write_node_value(node_id, value) -> None:
  try:
    __nodes[node_id].write(value)
  except:
    logmanager.error(TAG, sys.exc_info())

def datastore(node_id: str, num: int) -> list:
  return datastoremanager.find_datastore_values(node_id, num)
  
