from node import Node
from node import Parent

import time

from httpserver import ParentMain
from routerapp import NodeMain


parent = ParentMain({})

node1 = NodeMain({"route": "/app1"}, parent=parent)
node2 = NodeMain({"route": "/app2"}, parent=parent)

count = 0
while True:
  time.sleep(1)
  print(node1.read())
  print(node2.read())
  time.sleep(1)
  count += 1
  node1.write("{\"value\":" + str(count * 1) + "}")
  node2.write("{\"value\":" + str(count * 2) + "}")
