from phue import Bridge
from apps.node import Node

class NodeAppMain(Node):
  def __init__(self, config: dict):
    super(NodeAppMain, self).__init__()
    self.__address = config['address']
    self.__lightname = config['light_name']
    self.__phueonoffmanager = PhueOnOffManager(self.__address, self.__lightname)

  def read(self):
    super(NodeAppMain, self).read()
    _value = self.__phueonoffmanager.read()
    return _value

  def write(self, value):
    super(NodeAppMain, self).write(value)
    self.__phueonoffmanager.write(int(value))

class PhueOnOffManager:
  def __init__(self, addr, lightname):
    self.b = Bridge(addr)
    self.b.connect()
    self.lightname = lightname

  def read(self):
    value = self.b.get_light(self.lightname, 'bri')
    return int(value)

  def write(self, value):
    if value > 254:
      value = 254
    elif value < 0:
      value = 0
      
    self.b.set_light(self.lightname, 'bri', value)
