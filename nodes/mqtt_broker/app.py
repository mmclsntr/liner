from node import Node

class NodeMain(Node):
  def __init__(self, config, parent=None):
    super().__init__(config, parent)

  def read(self):
    super().read()
    return None

  def write(self, value):
    super().write(value)

  def __del__(self):
    super().__del__()
