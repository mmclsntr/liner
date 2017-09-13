globalapps = [
{
  id: NumberInt(0),
  name: 'gpio',
  note: '',
  module_name: 'gpiodigital',
  required_configs: [
    {
      name: 'pin_num',
      type: 'int'
    }
  ]
},
{
  id: NumberInt(1),
  name: 'socket',
  note: '',
  module_name: 'socket',
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
}
]

db.global_apps.drop();
db.createCollection('global_apps');
db.global_apps.insert(globalapps);
result = db.global_apps.find();
shellPrint(result);


localapps = [
{
  id: NumberInt(0),
  name: 'gpio23',
  module_name: 'gpiodigital',
  global_app_id: NumberInt(0),
  device_id: NumberInt(0),
  note: '',
  configs: [
    {
      name: 'pin_num',
      type: 'int',
      value: NumberInt(23)
    }
  ]
},
{
  id: NumberInt(1),
  name: 'gpio24',
  module_name: 'gpiodigital',
  global_app_id: NumberInt(0),
  device_id: NumberInt(1),
  note: '',
  configs: [
    {
      name: 'pin_num',
      type: 'int',
      value: NumberInt(24)
    }
  ]
}
]

db.local_apps.drop();
db.createCollection('local_apps');
db.local_apps.insert(localapps);
result = db.local_apps.find();
shellPrint(result);


devices = [
  {
    id: NumberInt(0),
    name: 'led1',
    note: ''
  },
  {
    id: NumberInt(1),
    name: 'led2',
    note: ''
  }
]


db.devices.drop();
db.createCollection('devices');
db.devices.insert(devices);
result = db.devices.find();
shellPrint(result);

rules = [
{
  id: NumberInt(0),
  name: 'gpio23 on with 24',
  event: {
    nodeid: NumberInt(0), 
    operator: '==', 
    value: 1
  }, 
  actions: [
    {
      nodeid: NumberInt(1), 
      value: 1
    }
  ]
},
{
  id: 1,
  name: 'gpio23 off with 24',
  event: {
    nodeid: 0, 
    operator: '==', 
    value: 0
  }, 
  actions: [
    {
      nodeid: 0, 
      value: 0
    }
  ]
}
]


db.rules.drop();
db.createCollection('rules');
db.rules.insert(rules);
result = db.rules.find();
shellPrint(result);
