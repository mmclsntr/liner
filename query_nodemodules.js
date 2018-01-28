node_modules = [
{
  name: 'gpio int-int',
  note: '',
  module_name: 'gpiodigital',
  readtype: 'int',
  writetype: 'int',
  required_configs: [
    {
      name: 'pin_num',
      type: 'int'
    }
  ]
},
{
  name: 'gpio int-int [readonly]',
  note: '',
  module_name: 'gpiodigital',
  readtype: 'int',
  required_configs: [
    {
      name: 'pin_num',
      type: 'int'
    }
  ]
},
{
  name: 'gpio int-int [writeonly]',
  note: '',
  module_name: 'gpiodigital',
  writetype: 'int',
  required_configs: [
    {
      name: 'pin_num',
      type: 'int'
    }
  ]
},
{
  name: 'socket int-int',
  note: '',
  module_name: 'socket',
  readtype: 'int',
  writetype: 'int',
  required_configs: [
    {
      name: 'address',
      type: 'str'
    },
    {
      name: 'port',
      type: 'int'
    }
  ]
},
{
  name: 'http get str-str',
  note: '',
  module_name: 'httpget',
  readtype: 'str',
  writetype: 'str',
  required_configs: [
    {
      name: 'read_uri',
      type: 'str'
    },
    {
      name: 'write_uri',
      type: 'str'
    }
  ]
},
{
  name: 'mabeee server int-int',
  note: '',
  module_name: 'mabeeeserver',
  readtype: 'int',
  writetype: 'int',
  required_configs: [
    {
      name: 'uri',
      type: 'str'
    },
    {
      name: 'deviceid',
      type: 'int'
    }
  ]
},
{
  name: 'phue onoff int-int',
  note: 'Please press hue bridge button before adding this app.',
  module_name: 'phueonoffmanager',
  readtype: 'int',
  writetype: 'int',
  required_configs: [
    {
      name: 'address',
      type: 'str'
    },
    {
      name: 'light_name',
      type: 'str'
    }
  ]
},
{
  name: 'phue brightness int-int',
  note: 'Please press hue bridge button before adding this app.',
  module_name: 'phuebrightnessmanager',
  readtype: 'int',
  writetype: 'int',
  required_configs: [
    {
      name: 'address',
      type: 'str'
    },
    {
      name: 'light_name',
      type: 'str'
    }
  ]
},
{
  name: 'ifttt outgoing webhocks',
  note: 'https://ifttt.com/maker_webhooks',
  module_name: 'iftttoutgoingwebhocks',
  readtype: 'str',
  writetype: 'str',
  required_configs: [
    {
      name: 'uri',
      type: 'str'
    }
  ]
},
{
  name: 'Echonet lite power',
  note: '',
  module_name: 'echonetcontrol.airconditioner_power',
  parent_module_name: 'echonetcontrol.echonetlitecontroller',
  readtype: 'bool',
  writetype: 'bool',
  required_configs: [
    {
      name: 'IP Address',
      type: 'str'
    }
  ]
},
{
  name: 'Echonet lite temprature',
  note: '',
  module_name: 'echonetcontrol.airconditioner_temperature',
  parent_module_name: 'echonetcontrol.echonetlitecontroller',
  readtype: 'int',
  writetype: 'int',
  required_configs: [
    {
      name: 'IP Address',
      type: 'str'
    }
  ]
},
{
  name: 'HTTP Server router',
  note: '',
  module_name: 'httpserver.routerapp',
  parent_module_name: 'httpserver.httpserver',
  readtype: 'str',
  writetype: 'str',
  required_configs: [
    {
      name: 'route',
      type: 'str'
    }
  ]
},
{
  name: 'MQTT client',
  note: '',
  module_name: 'mqtt_client.app',
  parent_module_name: '',
  readtype: 'str',
  writetype: 'str',
  required_configs: [
    {
      name: 'topic',
      type: 'str'
    },
    {
      name: 'broker_host',
      type: 'str'
    }
  ]
},
{
  name: 'MQTT broker',
  note: '',
  module_name: 'mqtt_broker.app',
  parent_module_name: 'mqtt_broker.broker',
  writetype: 'str',
  required_configs: [
  ]
},
{
  name: 'Websocket get newest values',
  note: '',
  module_name: 'websocketserver.newest_client',
  parent_module_name: 'websocketserver.server',
  readtype: 'str',
  writetype: 'str',
  required_configs: [
  ]
},
{
  name: 'Websocket Client',
  note: '',
  module_name: 'websocketclient.app',
  readtype: 'str',
  writetype: 'str',
  required_configs: [
    {
      name: "URL",
      type: "str"
    }
  ]
}
]

db.node_modules.drop();
db.createCollection('node_modules');
db.node_modules.insert(node_modules);
result = db.node_modules.find();
shellPrint(result);


parent_node_modules = [
{
  _id: ObjectId('111111111111111111111111'),
  name: 'Echonet lite controller',
  readtype: 'int',
  writetype: 'int',
  module_name: 'echonetcontrol.echonetlitecontroller',
  note: '',
  required_configs: [
  ]
},
{
  _id: ObjectId('222222222222222222222222'),
  name: 'HTTP Server',
  readtype: 'str',
  writetype: 'str',
  module_name: 'httpserver.httpserver',
  note: '',
  required_configs: [
  ]
},
{
  _id: ObjectId('333333333333333333333333'),
  name: 'Websocket Server',
  readtype: 'str',
  writetype: 'str',
  module_name: 'websocketserver.server',
  note: '',
  required_configs: [
    {
      name: 'port',
      type: 'int'
    }
  ]
},
{
  _id: ObjectId('444444444444444444444444'),
  name: 'MQTT Broker',
  module_name: 'mqtt_broker.broker',
  note: '',
  required_configs: [
  ]
}
]

db.parent_node_modules.drop();
db.createCollection('parent_node_modules');
db.parent_node_modules.insert(parent_node_modules);
result = db.parent_node_modules.find();
shellPrint(result);

parent_nodes = [
{
  name: 'Echonet lite controller',
  readtype: 'str',
  writetype: 'str',
  module_name: 'echonetcontrol.echonetlitecontroller',
  note: '',
  parent_node_module_id: '111111111111111111111111',
  configs: [
  ]
},
{
  name: 'HTTP Server',
  readtype: 'int',
  writetype: 'int',
  module_name: 'httpserver.httpserver',
  note: '',
  parent_node_module_id: '222222222222222222222222',
  configs: [
  ]
},
{
  name: 'Websocket Server',
  readtype: 'str',
  writetype: 'str',
  module_name: 'websocketserver.server',
  note: '',
  parent_node_module_id: '333333333333333333333333',
  configs: [
    {
      name: 'port',
      type: 'int',
      value: 8000
    }
  ]
},
{
  name: 'MQTT Broker',
  module_name: 'mqtt_broker.broker',
  note: '',
  parent_node_module_id: '444444444444444444444444',
  configs: [
  ]
}
]

db.parent_nodes.drop();
db.createCollection('parent_nodes');
db.parent_nodes.insert(parent_nodes);
result = db.parent_nodes.find();
shellPrint(result);
