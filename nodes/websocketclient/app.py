import websocket
import threading

from node import Node

class NodeMain(Node):
  def on_message(self, ws, message):
    self.values.append(message)

  def on_error(self, ws, error):
    pass

  def on_close(self, ws):
    pass
  
  def on_open(self, ws):
    pass
 
  def __init__(self, config: dict, parent=None):
    super().__init__(config, parent)
    self.__url = config["URL"]
    self.values = []
    websocket.enableTrace(True)
    self.ws = websocket.WebSocketApp(self.__url,
                              on_message = self.on_message,
                              on_error = self.on_error,
                              on_close = self.on_close)
    self.ws.on_open = self.on_open
    th = threading.Thread(target=self.ws.run_forever)
    th.setDaemon(True)
    th.start()

  def read(self):
    super().read()
    if len(self.values) > 1:
      return self.values.pop(0)
    elif len(self.values) == 1:
      return self.values[0]
    else:
      return None

  def write(self, value):
    super().write(value)
    self.ws.send(value)

  def __del__(self):
    super().__del__()
    self.ws.close()

if __name__ == "__main__":
  test = NodeMain({"URL": "ws://localhost:3000" })
