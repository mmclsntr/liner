import urllib
import json
from node import Node

class NodeMain(Node):
  def __init__(self, config: dict, parent=None):
    super().__init__(config, parent)
    self.__readuri = config['read_uri']
    self.__writeuri = config['write_uri']
    self.__httpget = HTTPGet(self.__readuri, self.__writeuri)

  def read(self):
    super().read()
    _value = self.__httpget.read()
    return _value

  def write(self, value):
    super().write(value)
    self.__httpget.write(value)


class HTTPGet:
  def __init__(self, readuri, writeuri):
    self.__readuri = readuri
    self.__writeuri = writeuri

  def read(self):
    res =  urllib.request.urlopen(self.__readuri)
    content = res.read().decode('utf-8')
    json_dict = json.loads(content)
    return json_dict['value']

  def write(self, value):
    url = self.__writeuri + "?value=" + str(value)
    res =  urllib.request.urlopen(url)
