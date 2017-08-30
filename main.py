from centralmanager import CentralManager
import sys
import signal

centralmanager = CentralManager()
print('start')

def handler(signal, frame):
  centralmanager.destroy()
  print('end')
  sys.exit(0)

signal.signal(signal.SIGINT, handler)

while True:
  pass
