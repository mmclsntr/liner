import threading
import databasehelper
import time
import logging
from appmanager import AppManager

CONNECTER_COLLECTION_NAME = 'rules'

class RuleBaseConnectorThread(threading.Thread):
  __instance = None

  def __new__(cls, *args, **keys):
    if cls.__instance is None:
      cls.__instance = object.__new__(cls)
    return cls.__instance

  def __init__(self, app_manager, interval, dbname):
    super(RuleBaseConnectorThread, self).__init__()
    logging.basicConfig(level=logging.DEBUG)
    self.interval = interval
    self.__databasename = dbname
    self.__databasehelper = databasehelper.DataBaseHelper()
    self.__app_manager = app_manager

  def setNodesDict(self, nodes: dict):
    self.nodes = nodes

  def __connectnodes(self):
    db = self.__databasehelper.get_database(self.__databasename)
    while self.__isrunning:
      connectionscol = self.__databasehelper.get_collection(db, CONNECTER_COLLECTION_NAME)
      connections = list(self.__databasehelper.find(connectionscol, {}))

      for connection in connections:
        event = connection['event']
        eventnodecol = self.__databasehelper.get_collection(db, event['nodename'])
        eventnodevalues = self.__databasehelper.find(eventnodecol, {})
        # Sort with time by desc
        desceventnodevalues = sorted(eventnodevalues, key=lambda x:x['time'], reverse=True)

        firstvalue = str(desceventnodevalues[0]['value'])
        secondvalue = str(desceventnodevalues[1]['value'])
        eventoperator = str(event['operator'])
        eventvalue = str(event['value'])

        firstrule = firstvalue + eventoperator + eventvalue
        secondrule = secondvalue + eventoperator + eventvalue

        # Rule check
        if eval(firstrule) and not eval(secondrule):
          logging.info('ignite: ' + str(connection))
          actions = connection['actions']
          for action in actions:
            app_id = self.__app_manager.find_localapp_id_from_name(action['nodename'])
            self.__app_manager.write_app_value(int(app_id), action['value'])

      time.sleep(self.interval)

  def run(self):
    self.__isrunning = True
    self.__connectnodes()

  def kill(self):
    self.__isrunning = False
