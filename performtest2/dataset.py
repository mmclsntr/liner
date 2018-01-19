import sys
sys.path.append('..')

import databasehelper
from bson.objectid import ObjectId
import configmanager 


DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')
DB_COLLECTION_LOCALAPPS = configmanager.get_key('DATABASE', 'NodesCollection')
DB_COLLECTION_GLOBALAPPS = configmanager.get_key('DATABASE', 'NodeModulesCollection')
DB_COLLECTION_RULES = configmanager.get_key('DATABASE', 'RulesCollection')
DB_COLLECTION_DEVICES = configmanager.get_key('DATABASE', 'DevicesCollection')
DB_COLLECTION_TEMP_DATASTORE = configmanager.get_key('DATABASE', 'DataStoreCollectionTemp')
INTERVAL = float(configmanager.get_key('INTERVALS', 'RulebaseInterval'))


# Drop global apps
def drop_globalapps():
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_GLOBALAPPS)
  databasehelper.drop(col)

# Add global apps
def add_globalapp():
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_GLOBALAPPS)
  
  app_id = ObjectId()
  globalapp = {
    "_id": app_id,
    "name": 'test app int-int',
    "note": '',
    "module_name": 'testapp',
    "readtype": 'int',
    "writetype": 'int',
    "required_configs": [
      {
        "name": 'iofile',
        "type": 'str'
      },
      {
        "name": 'logfile',
        "type": 'str'
      }
    ]
  }
  databasehelper.insert(col, globalapp)
  return str(app_id)


# Drop local apps
def drop_localapps():
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
  databasehelper.drop(col)

# Add local apps
def add_localapp(global_id):
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
  
  app_id = ObjectId()
  io_name = str(app_id) + '.io'
  log_name = str(app_id) + '.log'
  
  localapp = {
    "_id": app_id,
    "name": "test app int-int",
    "note": "",
    "module_name": "testapp",
    "readtype": 'int',
    "writetype": 'int',
    "node_module_id": global_id,
    "configs": [
      {
        "name": 'iofile',
        "value": io_name,
        "type": 'str'
      },
      {
        "name": 'logfile',
        "value": log_name,
        "type": 'str'
      }
    ]
  }
  databasehelper.insert(col, localapp)
  return str(app_id) 

# Drop devices
def drop_devices():
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_DEVICES)
  databasehelper.drop(col)

# Add devices
def add_device(localapps):
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_DEVICES)
  
  device = {
    "name": "test",
    "note": "",
    "apps": localapps
  }
  databasehelper.insert(col, device)

# Drop linkage rules
def drop_rules():
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_RULES)
  databasehelper.drop(col)

# App linkage rules
# neighbors or chains
def add_rule(event_node, action_node):
  db = databasehelper.get_database(DB_NAME)
  col = databasehelper.get_collection(db, DB_COLLECTION_RULES)
  
  rule = {
    "name": "rule",
    "on": True,
    "event": {
      "nodeid": event_node,
      "operator": "==",
      "value": 1,
      "type": "int"
    },
    "action": {
      "nodeid": action_node,
      "value": 1,
      "type": "int"
    }
  }
  databasehelper.insert(col, rule)




if __name__ == "__main__":
# Arguments
# data numbers and connecting mode (0: neighbors, 1: chains)
  argvs = sys.argv
  if len(argvs) < 2:
    print('Please set number of apps and mode')
    exit(0)

  num = argvs[1]
  connectors_num = int(argvs[2])

  drop_globalapps() 
  global_id = add_globalapp()
  drop_localapps()

  localapps = []
  for i in range(int(num)):
    local_id = add_localapp(global_id)
    localapps.append(local_id)
  
  drop_devices()
  add_device(localapps)

  drop_rules()
  
  event_id = ''
  action_id = ''
  count = 0
  for app in localapps:
    if count >= connectors_num:
      break
    if event_id == '':
      event_id = app
    else:
      action_id = app
      add_rule(event_id, action_id)
      event_id = ''
      count += 1
        
  for app in localapps:
    print(app)     

