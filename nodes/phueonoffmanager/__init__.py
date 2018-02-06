from phue import Bridge
from node import Node

class NodeMain(Node):
  def __init__(self, config: dict, parent=None):
    super().__init__(config, parent)
    self.__address = config['address']
    self.__lightname = config['light_name']
    self.__phueonoffmanager = PhueOnOffManager(self.__address, self.__lightname)

  def read(self):
    super().read()
    _value = self.__phueonoffmanager.read()
    return _value

  def write(self, value):
    super().write(value)
    if value == "True" or value == "true" or  value == "1":
      self.__phueonoffmanager.write(True)
    else:
      self.__phueonoffmanager.write(False)

class PhueOnOffManager:
  def __init__(self, addr, lightname):
    self.b = Bridge(addr)
    self.b.connect()
    self.lightname = lightname

  def read(self):
    value = self.b.get_light(self.lightname, 'on')
    return str(value)

  def write(self, value):
    self.b.set_light(self.lightname, 'on', value)
