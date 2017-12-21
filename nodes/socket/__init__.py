import socket
from nodes.node import Node

class NodeAppMain(Node):
  def __init__(self, config: dict):
    super(NodeAppMain, self).__init__()
    self.__address = config['address']
    self.__port = config['port']
    self.__socketmanager = SocketManager(self.__address, self.__port)

  def read(self):
    super(NodeAppMain, self).read()
    _value = self.__socketmanager.read()
    return _value

  def write(self, value):
    super(NodeAppMain, self).write(value)
    self.__socketmanager.write(str(value))


class SocketManager:
  def __init__(self, address, port):
    self.__address = (address, port)

  def read(self):
    self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__client.connect(self.__address)
    self.__client.sendall('read'.encode('utf-8'))
    data = self.__client.recv(1000)
    self.__client.close()
    strval = data.decode('utf-8')
    if strval != '':
      return int(data.decode('utf-8'))
    else:
      return 0;

  def write(self, value):
    self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__client.connect(self.__address)
    self.__client.sendall('write'.encode('utf-8'))
    if value != '':
      self.__client.sendall(str(value).encode('utf-8'))
    else:
      self.__client.sendall(''.encode('utf-8'))
    self.__client.close()

