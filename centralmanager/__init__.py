import nodemanager 
import rulebaselinkage
import devicemanager
import webmanager

import time


def run() -> None:
  nodemanager.load_nodes()
  print('Loaded nodes')
  time.sleep(3)
  print('rulebase')
  rulebaselinkage.run()
  print('webmanager')
  webmanager.run_server()

def destroy() -> None:
  nodemanager.unload_nodes()
  rulebaselinkage.kill()
