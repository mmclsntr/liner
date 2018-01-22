import server
import newest_client

import time

parent = server.ParentMain({"port": 8000})
n_clients = newest_client.NodeMain({}, parent)


while True:
  time.sleep(1)
  print(n_clients.read())
