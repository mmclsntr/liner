from node import Node
from time import sleep
import threading

import pika

class NodeMain(Node):

  def on_message(self, ch, method, properties, body):
    self.data_queue.append(body)

  def __init__(self, config: dict, parent=None):
    super().__init__(config)
    self.data_queue = []
    self.queue = config["queue"]
    self.host = config["broker_host"]
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
    self.channel = self.connection.channel()
    self.channel.queue_declare(queue=self.queue)
    self.channel.basic_consume(on_message, queue=self.queue, no_ack=True)

    th = threading.Thread(target=self.channel.start_consuming)
    th.setDaemon(True)
    th.start()
  
  def read(self):
    super().read()
    if len(self.data_queue) > 0:
      return self.data_queue.pop(0)
    else:
      return None

  def write(self, value):
    super().write(value)
    self.channel.basic_publish(exhange="", routing_key=self.queue, body=value)

  def __del__(self):
    super().__del__()
    self.connection.close()
