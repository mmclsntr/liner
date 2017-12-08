from apps.node import Node
import time
import os

IOFILE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/io'
LOGFILE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/logs'

class NodeAppMain(Node):
  def __init__(self, config: dict):
    super(NodeAppMain, self).__init__()
    self.__iofile = config['iofile']
    self.__logfile = config['logfile']
    self.__testapp = TestApp(self.__iofile, self.__logfile)

  def read(self):
    super(NodeAppMain, self).read()
    _value = self.__testapp.read()
    return int(_value)

  def write(self, value):
    super(NodeAppMain, self).write(value)
    self.__testapp.write(str(value))



class TestApp:

  def __init__(self, iofile, logfile):
    self.iofile = IOFILE_DIR + '/' + iofile
    self.logfile = LOGFILE_DIR + '/' + logfile
    with open(self.iofile, 'w') as f:
      f.write('0')
    
  def read(self) -> int:
    _value = ''
    with open(self.iofile, 'r') as f:
      _value = f.read()
    with open(self.logfile, 'a') as f:
      line = str(time.time()) + ',' + _value + ',' + 'read' + "\n"
      f.write(line)
    return _value

  def write(self, value: str):
    with open(self.logfile, 'a') as f:
      line = str(time.time()) + ',' + value + ',' + 'write' + "\n"
      f.write(line)
    with open(self.iofile, 'w') as f:
      f.write(value)

