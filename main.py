from centralmanager import CentralManager
import sys
import signal

centralmanager = CentralManager()

def handler(signal, frame):
  centralmanager.destroy()
  sys.exit(0)

signal.signal(signal.SIGINT, handler)

while True:
  pass
