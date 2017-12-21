import urllib
import json
from nodes.node import Node

class NodeAppMain(Node):
  def __init__(self, config: dict):
    super(NodeAppMain, self).__init__()
    self.__uri = config['uri']
    self.__deviceid = config['deviceid']
    self.__mabeeeserver = MabeeeServer(self.__uri, self.__deviceid)

  def read(self):
    super(NodeAppMain, self).read()
    _value = self.__mabeeeserver.read()
    return _value

  def write(self, value):
    super(NodeAppMain, self).write(value)
    self.__mabeeeserver.write(value)


class MabeeeServer:
  def __init__(self, uri, deviceid):
    self.__uri = uri
    self.__deviceid = deviceid
    url = uri + "/scan/start/"
    res =  urllib.request.urlopen(url)
    url = uri + "/devices/" + str(deviceid) + "/connect/"
    res =  urllib.request.urlopen(url)
    url = uri + "/scan/stop/"
    res =  urllib.request.urlopen(url)

  def read(self):
    url = self.__uri + "/devices/" + str(self.__deviceid) + "/"
    res =  urllib.request.urlopen(url)
    content = json.loads(res.read().decode('utf-8'))
    return content["pwm_duty"]

  def write(self, value):
    url = self.__uri + "/devices/" + str(self.__deviceid) + "/set/?pwm_duty=" + str(value)
    res =  urllib.request.urlopen(url)
