import wiringpi
import enum

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

class DeviceMode(enum.Enum):
  GPIO = 0
  TCPIP = 1

class DeviceManager:
  def __init__(self, mode: DeviceMode, config: dict):
    if mode == DeviceMode.GPIO:
      self.__device = GpioManager(config['pin_num'])
    #elif mode == DeviceMode.TCPIP:
      ## TODO

  def read(self):
    _value = self.__device.read()
    return _value

  def write(self, value):
    self.__device.write(value)
