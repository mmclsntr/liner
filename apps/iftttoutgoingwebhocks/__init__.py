import urllib
import json
from apps.node import Node

class NodeAppMain(Node):
  def __init__(self, config: dict):
    super(NodeAppMain, self).__init__()
    self.__uri = config['uri']
    self.__iftttoutgoing = IFTTTOutgoing(self.__uri)

  def read(self):
    super(NodeAppMain, self).read()
    _value = self.__iftttoutgoing.read()
    return _value

  def write(self, value):
    super(NodeAppMain, self).write(value)
    self.__iftttoutgoing.write(value)


class IFTTTOutgoing:
  def __init__(self, uri):
    self.__uri = uri
    self.__count = 0

  def read(self):
    return self.__count;

  def write(self, value):
    data = {
      "value1": str(value)
    }
    data = urllib.parse.urlencode(data).encode("utf-8")
    res =  urllib.request.urlopen(self.__uri, data=data)
    self.__count += 1
