from appmanager import AppManager
from datastoremanager import DataStoreManager
from nodeconnectormanager import NodeConnectorManager

import signal
import sys

appmanager = AppManager('dev')

apps = appmanager.get_localapps()

for app in apps.values():
  print(app)

datastoremanager = DataStoreManager(appmanager, 'dev')

nodeconnectormanager = NodeConnectorManager(appmanager, 'dev')

def handler(signal, frame):
  datastoremanager.killall()
  nodeconnectormanager.kill()
  sys.exit(0)

signal.signal(signal.SIGINT, handler)

while True:
  pass
