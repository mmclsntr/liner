import appmanager 
import rulebaseconnectormanager
import devicemanager
import webmanager

import time


def run() -> None:
  appmanager.load_localapps()
  print('Locaded apps')
  time.sleep(3)
  print('rulebase')
  rulebaseconnectormanager.run()
  print('webmanager')
  webmanager.run_server(False)

def destroy() -> None:
  webmanager.kill_server()
  appmanager.unload_localapps()
  rulebaseconnectormanager.kill()
