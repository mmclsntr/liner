globalapps = [
{
  id: 0,
  name: 'gpio',
  note: '',
  required_configs: [
    {
      name: 'pin_num',
      type: 'int'
    }
  ]
},
{
  id: 1,
  name: 'socket',
  note: '',
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
  id: 0,
  name: 'gpio23',
  module_name: 'gpiomanager',
  global_app_id: 0,
  device_id: 0,
  note: '',
  configs: [
    {
      name: 'pin_num',
      type: 'int',
      value: 23
    }
  ]
},
{
  id: 1,
  name: 'gpio24',
  module_name: 'gpiomanager',
  global_app_id: 0,
  device_id: 1,
  note: '',
  configs: [
    {
      name: 'pin_num',
      type: 'int',
      value: 24
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
    id: 0,
    name: 'led1',
    local_apps: [0],
    note: ''
  },
  {
    id: 1,
    name: 'led2',
    local_apps: [1],
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
  event: {
    nodename: 'gpio23', 
    operator: '==', 
    value: 1
  }, 
  actions: [
    {
      nodename: 'gpio24', 
      value: 1
    }
  ]
},
{
  event: {
    nodename: 'gpio23', 
    operator: '==', 
    value: 0
  }, 
  actions: [
    {
      nodename: 'gpio24', 
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
