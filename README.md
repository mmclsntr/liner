liner ~ linker, integrator, normalizer, enhancer and recorder for IoT at home ~
====

"liner" is integration and enhancement system for building interconnected IoT network at home. The system aims for end users as non programmer to be able to easily automate all of home IoTs and cloud services by Node-like linking. 

The name of **"liner"** is combination of those keywords, **"Linker"**, **"Integrator"**, **"Normalizer"**, **"Enhancer"**, and **"Recorder"** as the primary features. 


## Description

### Modules
|module name|description|
|:--|:--|
|**centralmanager**|Manage all modules in this project.|
|**nodemanager**|Manage Nodes described below|
|**devicemanager**|Manage devices (components)|
|**webmanager**|Manage web application which the user configures, controls and monitors things related this system via web browzer. It's built by Flask. |
|**datastoremanager**|Manage datastore|
|Data Store Thread|Record values of Node into datastore. This thread corresponds to Nodes one by one.|
|**rulebaselinkage**|Manage IF-THEN rules for interconnected network between Nodes|
|Rulebase Linkage Thread|Link Node to Node based on set IF-THEN rules by monitoring values in datastore independently. |

### Node

All applications of both devices and cloud servces are implemented as Node in this system. The node model has 2 edges, read and write. This common application framework makes interconnected network for every IoT app with each other. 

#### Node modules

Nodes are contributed as Node modules in `nodes/`. The information of node modules are in `node_modules` table in database. 

Node module absolutely includes *NodeAppMain* class inherited *Node* class as common main class. 

*ex.*

```python
class Node:
  def __init__(self):
      pass
  
  def read(self):
    pass

  def write(self, value):
    pass 
```

gpioonoff/\_\_init\_\_.py

```python
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

```

*Node Manager* imports Node modules as python module and creates an object of *NodeAppMain* class declared in the module. 

#### Implimented Node

| module name | description |
|:------------|:------------|
|||


## Requirement
- Raspberry Pi 3 model B
- Python 3.x
- MongoDB

## Usage

## Licence

## Author
