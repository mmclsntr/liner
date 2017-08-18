import wiringpi
import enum
import socket

class GpioManager:
  name = 'gpio_device'

  def __init__(self, pin_num: int):
    self.pin_num = pin_num
    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(pin_num, 1)

  def read(self) -> int:
    _value = wiringpi.digitalRead(self.pin_num)
    return _value

  def write(self, value: int):
    wiringpi.digitalWrite(self.pin_num, value)

class SocketManager:
  name = 'socket_device'

  def __init__(self, host: str, port: int):
    self.__host = host
    self.__port = port
    self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def __connect():
    self.__sock.connect((self.__host, self.__port))


  def read(self):
    self.__connect()
    chunks = []
    bytes_recd = 0
    while bytes_recd < MSGLEN:
      chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
      if chunk == b'':
        raise RuntimeError("socket connection broken")
      chunks.append(chunk)
      bytes_recd = bytes_recd + len(chunk)
    return b''.join(chunks)

  def write(self, value):
    self.__connect()
    totalsent = 0
    while totalsent < MSGLEN:
      sent = self.sock.send(msg[totalsent:])
      if sent == 0:
        raise RuntimeError("socket connection broken")
      totalsent = totalsent + sent

class DeviceMode(enum.Enum):
  GPIO = 0
  SOCKET = 1

class DeviceManager:
  def __init__(self, mode: DeviceMode, config: dict):
    if mode == DeviceMode.GPIO:
      self.__device = GpioManager(config['pin_num'])
    elif mode == DeviceMode.SOCKET:
      self.__device = SocketManager(config['host'], config['port'])

  def read(self):
    _value = self.__device.read()
    return _value

  def write(self, value):
    self.__device.write(value)
