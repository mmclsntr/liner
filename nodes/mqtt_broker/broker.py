from node import Parent
from hbmqtt.broker import Broker

import asyncio
import threading
import time

config_broker = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': '0.0.0.0:1883'
        }
    }
}

class ParentMain(Parent):
  @asyncio.coroutine
  def broker_coro(self):
      yield from self.broker.start()
  
  def __init__(self, config):
    super().__init__(config)
    self.broker = Broker(config_broker)

    asyncio.get_event_loop().run_until_complete(self.broker_coro())
    #asyncio.get_event_loop().run_forever()
    th = threading.Thread(target=asyncio.get_event_loop().run_forever)
    th.setDaemon(True)
    th.start()

  def read(self, params=None):
    super().read(params)

  def write(self, value, params=None):
    super().write(value, params)

  def __del__(self):
    super().__del__()
    self.broker.shutdown()


if __name__ == "__main__":
  main = ParentMain({})

  time.sleep(10)
  del main
