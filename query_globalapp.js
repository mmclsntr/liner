globalapps = [
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
  name: 'test app int-int',
  note: '',
  module_name: 'testapp',
  readtype: 'int',
  writetype: 'int',
  required_configs: [
    {
      name: 'iofile',
      type: 'str'
    },
    {
      name: 'logfile',
      type: 'str'
    }
  ]
}
]

db.global_apps.drop();
db.createCollection('global_apps');
db.global_apps.insert(globalapps);
result = db.global_apps.find();
shellPrint(result);
