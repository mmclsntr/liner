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
  name: 'ECHONET lite Air Conditioner ON/OFF int-int',
  note: '',
  module_name: 'echonetaircononoff',
  readtype: 'int',
  writetype: 'int',
  required_configs: [
    {
      name: 'IP_Address',
      type: 'str'
    }
  ]
},
{
  name: 'ECHONET lite Air Conditioner Templeture int-int',
  note: '',
  module_name: 'echonetaircontemp',
  readtype: 'int',
  writetype: 'int',
  required_configs: [
    {
      name: 'IP_Address',
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
