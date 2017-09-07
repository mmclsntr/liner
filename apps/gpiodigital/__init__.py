from apps.node import Node
import wiringpi

class NodeAppMain(Node):
  def __init__(self, config: dict):
    super(NodeAppMain, self).__init__()
    self.__pin = config['pin_num']
    self.__gpiomanager = GpioManager(self.__pin)

  def read(self):
    super(NodeAppMain, self).read()
    _value = self.__gpiomanager.read()
    return int(_value)

  def write(self, value):
    super(NodeAppMain, self).write(value)
    self.__gpiomanager.write(int(value))



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

