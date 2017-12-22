import databasehelper as dbhelper
import configmanager
import nodemanager
import threading
import time
import logging
import pymongo
from bson.objectid import ObjectId

DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')
DB_COLLECTION_RULES = configmanager.get_key('DATABASE', 'RulesCollection')
DB_COLLECTION_TEMP_DATASTORE = configmanager.get_key('DATABASE', 'DataStoreCollectionTemp')
INTERVAL = float(configmanager.get_key('INTERVALS', 'RulebaseInterval'))
 
class RuleBaseLinkageThread(threading.Thread):
  __instance = None

  def __new__(cls, *args, **keys):
    if cls.__instance is None:
      cls.__instance = object.__new__(cls)
    return cls.__instance

  def __init__(self) -> None:
    super(RuleBaseLinkageThread, self).__init__()
    logging.basicConfig(level=logging.DEBUG)
    self.interval = INTERVAL

  def __connectnodes(self) -> None:
    db = dbhelper.get_database(DB_NAME)
    while self.__isrunning:
      connectionscol = dbhelper.get_collection(db, DB_COLLECTION_RULES)
      connections = list(dbhelper.find(connectionscol, {}))

      for connection in connections:
        if connection['on'] == False:
          continue

        event = connection['event']
        if 'type' not in event:
          continue

        eventnodecol = dbhelper.get_collection(db, DB_COLLECTION_TEMP_DATASTORE + str(event['nodeid']))
        eventnodevalues = dbhelper.find(eventnodecol, {}, dict(sort=[('time', pymongo.DESCENDING)], limit=2))
        # Sort with time by desc
        desceventnodevalues = eventnodevalues

        firstvalue = str(desceventnodevalues[0]['value'])
        secondvalue = str(desceventnodevalues[1]['value'])
        eventoperator = str(event['operator'])
        eventvalue = str(event['value'])
        eventtype = str(event['type'])

        firstrule = eventtype + "('" + firstvalue + "') " + eventoperator + " " + eventtype + "('" + eventvalue + "')"
        secondrule = eventtype + "('" + secondvalue + "') " + eventoperator + " " + eventtype + "('" + eventvalue + "')"

        # Rule check
        if eval(firstrule) and not eval(secondrule):
          logging.info('ignite: ' + str(connection))
          action = connection['action']
          if 'type' not in action:
            continue
          node_id = action['nodeid']
          nodemanager.write_node_value(str(node_id), eval(action['type'] + "('" + str(action['value']) + "')"))

      time.sleep(self.interval)

  def run(self) -> None:
    self.__isrunning = True
    self.__connectnodes()

  def kill(self) -> None:
    self.__isrunning = False



rulebase_thread = RuleBaseLinkageThread()

def run() -> None:
  rulebase_thread.start()

def kill() -> None:
  rulebase_thread.kill()

def find_rule(connector_id: str) -> dict:
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_RULES)
  rule = dbhelper.find(col, {'_id': ObjectId(connector_id)})
  return rule[0]

def list_rules() -> list:
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_RULES)
  listrules = list(dbhelper.find(col, {}))
  return listrules

def add(new_rule: dict) -> None:
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_RULES)
  if "_id" in new_rule:
    new_rule["_id"] = ObjectId(new_rule["_id"])
  dbhelper.insert(col, new_rule)

def update(connector_id: str, updated_rule: dict) -> None:
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_RULES)
  dbhelper.update(col, {'_id': ObjectId(connector_id)}, updated_rule)

def delete(connector_id: str) -> None:
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_RULES)
  dbhelper.delete(col, {'_id': ObjectId(connector_id)})
