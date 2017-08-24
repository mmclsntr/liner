import threading
import databasehelper
import devicemanager
import time

CONNECTER_COLLECTION_NAME = 'connections'

class NodeConnectorThread(threading.Thread):
  def __init__(self, interval, dbname):
    super(NodeConnectorThread, self).__init__()
    self.interval = interval
    self.__databasename = dbname
    self.__databasehelper = databasehelper.DataBaseHelper()

  def setNodesDict(self, nodes: dict):
    self.nodes = nodes

  def __connectnodes(self):
    db = self.__databasehelper.get_database(self.__databasename)
    while self.__isrunning:
      connectionscol = self.__databasehelper.get_collection(db, CONNECTER_COLLECTION_NAME)
      connections = list(self.__databasehelper.find(connectionscol, {}))
      #connections = [
      #  {'event': {'nodename': 'gpio24', 'operator': '==', 'value': 1}, 'actions': [{'nodename': 'gpio23', 'value': 1}]},
      #  {'event': {'nodename': 'gpio24', 'operator': '==', 'value': 0}, 'actions': [{'nodename': 'gpio23', 'value': 0}]}
      #]

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
          actions = connection['actions']
          for action in actions:
            node = self.nodes[action['nodename']]
            node.write(int(action['value']))

      time.sleep(self.interval)

  def run(self):
    self.__isrunning = True
    self.__connectnodes()

  def kill(self):
    self.__isrunning = False
