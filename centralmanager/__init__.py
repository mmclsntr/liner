import nodemanager 
import rulebaselinkage
import devicemanager
import webmanager
import logmanager

import time

TAG = 'CentralManager'

def run() -> None:
  logmanager.log(TAG, 'Loading nodes')
  nodemanager.load_nodes()
  time.sleep(2)
  logmanager.log(TAG, 'Running RulebaseLinkage')
  rulebaselinkage.run()
  logmanager.log(TAG, 'Running WebManager')
  webmanager.run_server()

def destroy() -> None:
  logmanager.log(TAG, 'Destroy')
  nodemanager.unload_nodes()
  rulebaselinkage.kill()
