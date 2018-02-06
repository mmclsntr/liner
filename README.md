liner ~ linker, integrator, normalizer, enhancer and recorder for  home automation ~
====

"liner" is integration and enhancement platform system for building interconnected IoT network at home. The system aims for end users as non programmer to be able to easily automate all of home IoTs and cloud services by Node-like linking. 

The name of **"liner"** is combination of those keywords, **"Linker"**, **"Integrator"**, **"Normalizer"**, **"Enhancer"**, and **"Recorder"** as the primary features. 

## Usage
1. Run MongoDB server
1. Preset node module information into MongoDB  
  `mongo dev query.js`
1. Run main program of Liner  
  `python main.py`

## Requirement
- Raspberry Pi 3 model B
- Python 3.x
- MongoDB (upper 2.4)


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

Node module absolutely includes *NodeMain* class inherited *Node* class as common main class. The class has been defined in `nodes/node.py`.


#### Implimented Node

| module name | description |
|:------------|:------------|
|||

### Parent Node
To cover various types of applications, Liner has introduced ”Parent Node”. It also shapes simple node with Read edge and Write edge same as Node, but the role is distinct. 

It relays communication between multiple Nodes and the corresponding IoT device as a single connection

Parent Node has been implemented as an abstract base class, named `Parent class`. The class has been defined in `nodes/node.py`.


## License
See [LICENSE](LICENSE).  
© Shintaro Yamasaki. All Rights Reserved.
