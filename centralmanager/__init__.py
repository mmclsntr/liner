import appmanager 
import rulebaseconnectormanager
import devicemanager
from webmanager import WebManager

import time


__webmanager = WebManager()

def run() -> None:
  appmanager.load_localapps()
  print('Locaded apps')
  time.sleep(3)
  print('rulebase')
  rulebaseconnectormanager.run()
  print('webmanager')
  __webmanager.run(True)

def destroy() -> None:
  appmanager.unload_localapps()
  rulebaseconnectormanager.kill()
