from datastorethread import DataStoreThread
  
data_stores = {}

def run_datastorer(node_id, name, node):
  datastorethread = DataStoreThread(node, node_id, 1.0)
  datastorethread.start()
  data_stores[node_id] = datastorethread

def kill_datastorer(node_id):
  data_stores[node_id].kill()
  data_stores[node_id] = None
  del data_stores[node_id]

def killall():
  for datastore in data_stores.values():
    datastore.kill()
