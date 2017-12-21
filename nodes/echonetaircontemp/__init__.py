import socket
import codecs
import time

from nodes.node import Node

E_HEADER = "10810000"
E_SEOJ = "05FF01"
E_DEOJ = "013001"  # Air conditioner
E_OPC = "01"
E_PDC1 = "01"

class NodeAppMain(Node):
  def __init__(self, config: dict):
    super(NodeAppMain, self).__init__()
    self.__addr = config['IP_Address']
    self.__aircontemp = ECHONETLiteAirConditionerTemp(self.__addr)

  def read(self):
    super(NodeAppMain, self).read()
    _value = self.__aircontemp.read()
    return int(_value)

  def write(self, value):
    super(NodeAppMain, self).write(value)
    self.__aircontemp.write(int(value))

class ECHONETLiteAirConditionerTemp:
  def __init__(self, addr):
    self.__ip_addr = addr
    self.__port = 3610

  def read(self):
    esv = "62"
    epc = "B3"
    edt = "00"
    
    message = E_HEADER + E_SEOJ + E_DEOJ + esv + E_OPC + epc + E_PDC1 + edt
    msg = codecs.decode(message, "hex")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", self.__port))

    sock.sendto(msg, (self.__ip_addr, self.__port))

    data = sock.recvfrom(4048)
    datahex = codecs.encode(data[0], 'hex')
    datastr = codecs.decode(datahex, 'utf-8')
    sock.close()

    value = datastr[28:30]

    return int(value, 16)

  def write(self, value):
    esv = "60"
    epc = "B3"

    if value > 50:
      edt = "%02x" % 50
    elif value < 0:
      edt = "%02x" % 0
    else:
      edt = "%02x" % value

    message = E_HEADER + E_SEOJ + E_DEOJ + esv + E_OPC + epc + E_PDC1 + edt
    msg = codecs.decode(message, "hex")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg, (self.__ip_addr, self.__port))