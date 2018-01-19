from node import Node
from node import Parent

class NodeMain(Node):
  def __init__(self, config: dict, parent=None):
    super().__init__(config, parent)
    self.__addr = config['IP Address']
    self.__parent = parent

  def read(self):
    super().read()
    if self.__parent != None:
      params = {
        "ip_addr": self.__addr,
        "DEOJ": "013001",
        "EPC": "80"
      }
      if self.__parent.read(params) == "31":
        return True
      else:
        return False
    else:
      return None
    
  def write(self, value):
    super().write(value)
    if self.__parent != None:
      edt = "31"
      if bool(value) == True:
        edt = "30"
      
      params = {
        "ip_addr": self.__addr,
        "DEOJ": "013001",
        "EPC": "80"
      }
      self.__parent.write(edt, params)
