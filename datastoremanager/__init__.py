from datastorethread import DataStoreThread

class DataStoreManager:
  __instance = None

  def __new__(cls, *args, **keys):
    if cls.__instance is None:
      cls.__instance = object.__new__(cls)
    return cls.__instance
  
  def __init__(self, dbname: str):
    self.data_stores = {}
    self.__dbname = dbname

  def run_datastorer(self, node_id, name, node):
    datastorethread = DataStoreThread(node, name, 1.0, self.__dbname)
    datastorethread.start()
    self.data_stores[node_id] = datastorethread
  
  def kill_datastorer(self, node_id):
    self.data_stores[node_id].kill()
    self.data_stores[node_id] = None

  def killall(self):
    for datastore in self.data_stores.values():
      datastore.kill()

