from rulebaseconnectorthread import RuleBaseConnectorThread
from appmanager import AppManager

class NodeConnectorManager:
  __instance = None

  def __new__(cls, *args, **keys):
    if cls.__instance is None:
      cls.__instance = object.__new__(cls)
    return cls.__instance

  def __init__(self, app_manager: AppManager, dbname: str):
    self.__app_manager = app_manager
    self.__nodeconnectorthread = RuleBaseConnectorThread(app_manager, 0.5, dbname)
    self.__nodeconnectorthread.start()

  def kill(self):
    self.__nodeconnectorthread.kill()
