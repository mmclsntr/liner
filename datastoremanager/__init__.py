from datastorethread import DataStoreThread
import configmanager

data_stores = {}
INTERVAL = float(configmanager.get_key('INTERVALS', 'DatastoreInterval'))

def run_datastorer(node_id, node):
  datastorethread = DataStoreThread(node, node_id, INTERVAL)
  datastorethread.start()
  data_stores[node_id] = datastorethread

def kill_datastorer(node_id):
  data_stores[node_id].kill()
  data_stores[node_id] = None
  del data_stores[node_id]

def killall():
  for datastore in data_stores.values():
    datastore.kill()
