from node import Node
from node import Parent

class NodeMain(Node):
  def __init__(self, config: dict, parent=None):
    super().__init__(config)
    self.__parent = parent

  def read(self):
    super().read()
    __newests = self.__parent.read({"tag": "newest"})
    return __newests

  def write(self, value):
    super().write(value)
    self.__parent.write(value, {"tag": "send_to_all"})

  def __del__(self):
    super().__del__()

