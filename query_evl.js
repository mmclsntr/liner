node_modules = [
{
  name: 'HTTP GET Client',
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
}
]

db.node_modules.drop();
db.createCollection('node_modules');
db.node_modules.insert(node_modules);
result = db.node_modules.find();
shellPrint(result);


parent_node_modules = [
{
  name: 'HTTP Server',
  readtype: 'str',
  writetype: 'str',
  module_name: 'httpserver.httpserver',
  note: '',
  required_configs: [
  ]
},
{
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
  name: 'MQTT Broker',
  module_name: 'mqtt_broker.broker',
  note: '',
  required_configs: [
  ]
},
{
  name: 'Echonet lite controller',
  readtype: 'int',
  writetype: 'int',
  module_name: 'echonetcontrol.echonetlitecontroller',
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
