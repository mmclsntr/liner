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
}
]

db.global_apps.drop();
db.createCollection('global_apps');
db.global_apps.insert(globalapps);
result = db.global_apps.find();
shellPrint(result);

gpio_id = db.global_apps.find({name: 'gpio int-int'})[0]._id.valueOf();
socket_id = db.global_apps.find({name: 'socket int-int'})[0]._id.valueOf();
mabeee_id = db.global_apps.find({name: 'mabeee server int-int'})[0]._id.valueOf();
phue_id = db.global_apps.find({name: 'phue onoff int-int'})[0]._id.valueOf();


localapps = [
{
  name: 'gpio23',
  module_name: 'gpiodigital',
  global_app_id: gpio_id,
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
  global_app_id: gpio_id,
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
},
{
  name: 'buzzer grove',
  module_name: 'socket',
  global_app_id: socket_id,
  readtype: 'int',
  writetype: 'int',
  note: 'buzzer 1s',
  configs: [
    {
      name: 'address',
      type: 'str',
      value: '192.168.1.8'
    },
    {
      name: 'port',
      type: 'int',
      value: '4002'
    }
  ]
},
{
  name: 'button grove',
  module_name: 'socket',
  global_app_id: socket_id,
  readtype: 'int',
  writetype: 'int',
  note: 'button',
  configs: [
    {
      name: 'address',
      type: 'str',
      value: '192.168.1.8'
    },
    {
      name: 'port',
      type: 'int',
      value: '4008'
    }
  ]
},
{
  name: 'touch grove',
  module_name: 'socket',
  global_app_id: socket_id,
  readtype: 'int',
  writetype: 'int',
  note: 'touch',
  configs: [
    {
      name: 'address',
      type: 'str',
      value: '192.168.1.8'
    },
    {
      name: 'port',
      type: 'int',
      value: '4007'
    }
  ]
},
{
  name: 'light sensor grove',
  module_name: 'socket',
  global_app_id: socket_id,
  readtype: 'int',
  writetype: 'int',
  note: 'light [K]',
  configs: [
    {
      name: 'address',
      type: 'str',
      value: '192.168.1.8'
    },
    {
      name: 'port',
      type: 'int',
      value: '4011'
    }
  ]
},
{
  name: 'potential meter grove',
  module_name: 'socket',
  global_app_id: socket_id,
  readtype: 'int',
  writetype: 'int',
  note: '0-300',
  configs: [
    {
      name: 'address',
      type: 'str',
      value: '192.168.1.8'
    },
    {
      name: 'port',
      type: 'int',
      value: '4012'
    }
  ]
},
{
  name: 'mabeee server',
  module_name: 'mabeeeserver',
  global_app_id: socket_id,
  readtype: 'int',
  writetype: 'int',
  note: '',
  configs: [
    {
      name: 'uri',
      type: 'str',
      value: 'http://192.168.1.3:8080/mabeee'
    },
    {
      name: 'deviceid',
      type: 'int',
      value: '1'
    }
  ]
},
{
  name: 'phue onoff',
  module_name: 'phueonoffmanager',
  global_app_id: socket_id,
  readtype: 'int',
  writetype: 'int',
  note: '0-100',
  configs: [
    {
      name: 'address',
      type: 'str',
      value: '192.168.1.2'
    },
    {
      name: 'light_name',
      type: 'str',
      value: 'light'
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
touch_id = db.local_apps.find({name: 'touch grove'})[0]._id.valueOf();
button_id = db.local_apps.find({name: 'button grove'})[0]._id.valueOf();
buzzer_id = db.local_apps.find({name: 'buzzer grove'})[0]._id.valueOf();
light_id = db.local_apps.find({name: 'light sensor grove'})[0]._id.valueOf();
potentialmeter_id = db.local_apps.find({name: 'potential meter grove'})[0]._id.valueOf();
mabeee_id = db.local_apps.find({name: 'mabeee server'})[0]._id.valueOf();
phue_id = db.local_apps.find({name: 'phue onoff'})[0]._id.valueOf();


devices = [
  {
    name: 'self',
    note: '',
    apps: [gpio23_id, gpio24_id]
  },
  {
    name: 'grove Pi',
    note: 'ip: 192.168.1.8',
    apps: [touch_id, button_id, buzzer_id, light_id, potentialmeter_id]
  },
  {
    name: 'macbook',
    note: 'ip: 192.168.1.3',
    apps: [mabeee_id]
  },
  {
    name: 'phue',
    note: 'ip: 192.168.1.2',
    apps: [phue_id]
  }
]

db.devices.drop();
db.createCollection('devices');
db.devices.insert(devices);
result = db.devices.find();
shellPrint(result);



rules = [
{
  name: 'gpio23 on with 24',
  on: false,
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
  on: false,
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
