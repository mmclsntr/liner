from node import Node
from time import sleep
import threading

import paho.mqtt.client as mqtt

PORT = 1883
KEEP_ALIVE = 60

PUBLISH_NUMBER = 5
SLEEP_TIME = 5

class NodeMain(Node):

  def on_connect(self, client, userdata, flags, response_code):
    client.subscribe(self.topic)

  def on_message(self, client, userdata, message):
    self.data_queue.append(message.payload.decode('utf-8'))

  def __init__(self, config: dict, parent=None):
    super().__init__(config)
    self.data_queue = []
    self.topic = config["topic"]
    self.host = config["broker_host"]
    self.client = mqtt.Client(protocol=mqtt.MQTTv311)
    self.client.topic = self.topic
    self.client.on_connect = self.on_connect
    self.client.on_message = self.on_message
    self.client.connect(self.host, port=PORT, keepalive=KEEP_ALIVE)

    th = threading.Thread(target=self.client.loop_forever)
    th.setDaemon(True)
    th.start()
  
  def read(self):
    super().read()
    if len(self.data_queue) > 1:
      return self.data_queue.pop(0)
    elif len(self.data_queue) == 1:
      return self.data_queue[0]
    else:
      return None

  def write(self, value):
    super().write(value)
    self.client.publish(self.topic, value)

  def __del__(self):
    super().__del__()
    self.client.disconnect()
