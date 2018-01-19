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
        "EPC": "B3"
      }
      value = self.__parent.read(params)
      if value != None:
        return int(value, 16)
      else:
        return None
    else:
      return None
    
  def write(self, value):
    super().write(value)
    if value > 50:
      edt = "%02x" % 50
    elif value < 0:
      edt = "%02x" % 0
    else:
      edt = "%02x" % value
    
      params = {
        "ip_addr": self.__addr,
        "DEOJ": "013001",
        "EPC": "B3"
      }
      self.__parent.write(edt, params)
