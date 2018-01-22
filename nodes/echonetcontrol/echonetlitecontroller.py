import socket
import codecs
import time

from node import Node
from node import Parent

E_HEADER = "10810000"
E_SEOJ = "05FF01"
E_OPC = "01"
E_PDC1 = "01"

class ParentMain(Parent):
  def __init__(self, config: dict):
    super().__init__(config)
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.settimeout(5)
    self.__port = 3610
    self.sock.bind(("0.0.0.0", self.__port))

  def read(self, params=None):
    super().read(params)
    esv = "62"
    epc = "80"
    edt = "00"

    ip_addr = params["ip_addr"]
    deoj = params["DEOJ"]
    epc = params["EPC"]

    #print(ip_addr)

    message = E_HEADER + E_SEOJ + deoj + esv + E_OPC + epc + E_PDC1 + edt
    msg = codecs.decode(message, "hex")

    self.sock.sendto(msg, (ip_addr, self.__port))
    
    try:
      data = self.sock.recvfrom(4048)
    except socket.timeout:
      return None

    datahex = codecs.encode(data[0], 'hex')
    datastr = codecs.decode(datahex, 'utf-8')

    r_addr = data[1][0]
    r_seoj = datastr[8:14]
    r_epc = datastr[24:26]
    value = datastr[28:30]
    
    #print(r_addr)
    #print(r_seoj)
    #print(r_epc)

    if ip_addr != r_addr:
      return None
    if int(deoj, 16) != int(r_seoj, 16):
      return None
    if int(epc, 16) != int(r_epc, 16):
      return None

    return value


  def write(self, value, params=None):
    super().write(value, params)
    esv = "60"
    epc = "80"
    edt = "00"

    ip_addr = params["ip_addr"]
    deoj = params["DEOJ"]
    epc = params["EPC"]
    edt = value

    message = E_HEADER + E_SEOJ + deoj + esv + E_OPC + epc + E_PDC1 + edt
    msg = codecs.decode(message, "hex")

    self.sock.sendto(msg, (ip_addr, self.__port))

  def __del__(self):
    super().__del__()
    self.sock.close()


