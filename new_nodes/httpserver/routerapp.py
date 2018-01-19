from node import Node

class NodeMain(Node):
  def __init__(self, config: dict, parent=None):
    super().__init__(config, parent)
    self.__route = config['route']
    self.__parent = parent

  def read(self):
    super().read()
    if self.__parent != None:
      params = {
        "route": self.__route
      }
      return self.__parent.read(params)
    else:
      return None
    
  def write(self, value):
    super().write(value)
    if self.__parent != None:
      params = {
        "route": self.__route
      }
      self.__parent.write(value, params)
