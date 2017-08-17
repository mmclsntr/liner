import devicemanager as dm
import time

import signal
import sys

import datacollectorthread as dct
import nodeconnectorthread as nct

devices = [
  {'name': 'gpio23', 'mode': 'GPIO', 'config': {'pin_num': 23}},
  {'name': 'gpio24', 'mode': 'GPIO', 'config': {'pin_num': 24}}
]

datacollectors = []
devicesdict = {}

for device in devices:
  config = device['config']
  name = device['name']
  if device['mode'] == 'GPIO':
    mode = dm.DeviceMode.GPIO

  devicemanager_ = dm.DeviceManager(mode, config)
  devicemanager_.name = name
  devicemanager_.write(0)
  devicesdict[name] = devicemanager_
  datacollector = dct.DataCollectorThread(devicemanager_, 0.5, 'dev')
  datacollectors.append(datacollector)
  datacollector.start()


nodeconnectorthread = nct.NodeConnectorThread(0.1, 'dev')
nodeconnectorthread.setNodesDict(devicesdict)
nodeconnectorthread.start()

def handler(signal, frame):
  for datacollector in datacollectors:
    datacollector.kill()
  nodeconnectorthread.kill()
  sys.exit(0)

signal.signal(signal.SIGINT, handler)

while True:
  pass
