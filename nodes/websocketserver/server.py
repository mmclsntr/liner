from node import Node
from node import Parent

import threading
from websocket_server import WebsocketServer

values = {"clients": [], "messages":[], "newest": {}}

class ParentMain(Parent):
  def new_client(self, client, server):
    values["clients"] = server.clients

  def client_left(self, client, server):
    values["clients"] = server.clients

  def message_received(self, client, server, message):
    values["messages"].append({client["id"]: message})
    values["newest"][client["id"]] = message
  
  def __init__(self, config: dict):
    super().__init__(config)
    __port = config['port']
    self.__server = WebsocketServer(port=__port, host='0.0.0.0')
    self.__server.set_fn_new_client(self.new_client)
    self.__server.set_fn_client_left(self.client_left)
    self.__server.set_fn_message_received(self.message_received)
    th = threading.Thread(target=self.__server.run_forever)
    th.setDaemon(True)
    th.start()

  def read(self, params):
    super().read(params)
    __tag = params["tag"]
    if __tag in values:
      return values[__tag]
    else:
      return None

  def write(self, value, params):
    super().write(value, params)
    __tag = params["tag"]
    __client = params["client"]
    if __tag == "send_to_client":
      if "client" in params:
        __client = params["client"]
        self.__server.send_message(__client, value)
    elif __tag == "send_to_all":
      self.__server.send_message_to_all(value)

  def __del__(self):
    super().__del__()
    del self.__server

