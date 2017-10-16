globalapps = [
{
  name: 'gpio',
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
  name: 'socket',
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
}
]

db.global_apps.drop();
db.createCollection('global_apps');
db.global_apps.insert(globalapps);
result = db.global_apps.find();
shellPrint(result);

global_id = db.global_apps.find({name: 'gpio'})[0]._id.valueOf();


devices = [
  {
    name: 'led1',
    note: ''
  },
  {
    name: 'led2',
    note: ''
  }
]


db.devices.drop();
db.createCollection('devices');
db.devices.insert(devices);
result = db.devices.find();
shellPrint(result);

led1_id = db.devices.find({name: 'led1'})[0]._id.valueOf();
led2_id = db.devices.find({name: 'led2'})[0]._id.valueOf();

localapps = [
{
  name: 'gpio23',
  module_name: 'gpiodigital',
  global_app_id: global_id,
  device_id: led1_id,
  readtype: 'int',
  writetype: 'int',
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
  name: 'gpio24',
  module_name: 'gpiodigital',
  global_app_id: global_id,
  device_id: led2_id,
  readtype: 'int',
  writetype: 'int',
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

gpio23_id = db.local_apps.find({name: 'gpio23'})[0]._id.valueOf();
gpio24_id = db.local_apps.find({name: 'gpio24'})[0]._id.valueOf();


rules = [
{
  name: 'gpio23 on with 24',
  event: {
    nodeid: gpio23_id, 
    operator: '==', 
    value: NumberInt(1),
    type: 'int'
  }, 
  action: {
    nodeid: gpio24_id, 
    value: NumberInt(1),
    type: 'int'
  }
},
{
  name: 'gpio23 off with 24',
  event: {
    nodeid: gpio23_id, 
    operator: '==', 
    value: NumberInt(0),
    type: 'int'
  }, 
  action: {
    nodeid: gpio24_id, 
    value: NumberInt(0),
    type: 'int'
  }
}
]


db.rules.drop();
db.createCollection('rules');
db.rules.insert(rules);
result = db.rules.find();
shellPrint(result);
