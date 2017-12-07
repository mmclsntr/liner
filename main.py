import centralmanager
import sys
import signal

centralmanager.run()

def handler(signal, frame):
  centralmanager.destroy()
  sys.exit(0)

signal.signal(signal.SIGINT, handler)

