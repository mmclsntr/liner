import app
import time

client1 = app.NodeMain({"topic": "topic/test", "broker_host": "192.168.1.5"})
client2 = app.NodeMain({"topic": "topic1/test", "broker_host": "192.168.1.5"})
client3 = app.NodeMain({"topic": "topic2/test", "broker_host": "192.168.1.5"})

while True:
  time.sleep(1)
  print("1: ", client1.read())
  print("2: ", client2.read())
  print("3: ", client3.read())
