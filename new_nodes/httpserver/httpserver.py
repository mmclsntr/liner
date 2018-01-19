from node import Node
from node import Parent
import time
import http.server
import json
import threading

values = {}

class ParentMain(Parent):
  def __init__(self, config: dict):
    super().__init__(config)
    server_class = http.server.HTTPServer
    self.httpd = server_class(("", 8080),Handle)
    th = threading.Thread(target=self.httpd.serve_forever)
    th.setDaemon(True)
    th.start()

  def read(self, params):
    super().read(params)
    __route = params["route"]
    if __route in values:
      return values[__route]
    else:
      return None

  def write(self, value, params):
    super().write(value, params)
    __route = params["route"]
    values[__route] = value

  def __del__(self):
    super().__del__()
    self.httpd.server_close()

class Handle(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    __path = self.path
    print(__path)
    if __path in values:
      self.send_response(200)
      self.send_header("Content-type","application/json")
      self.end_headers()
      msg = values[__path]
      self.wfile.write(msg.encode('utf-8'))
    else:
      self.send_response(400)
      self.send_header("Content-type","application/json")
      self.end_headers()
      msg = '{"value": null}'
      self.wfile.write(msg.encode('utf-8'))

    return
  
  def do_POST(self):
    __path = self.path
    print(__path)
    content_len = int(self.headers.get('content-length'))
    request_body = self.rfile.read(content_len).decode('UTF-8')
    print('request body:', request_body)
    values[__path] = request_body
    self.send_response(200)
    self.send_header("Content-type","application/json")
    self.end_headers()
    self.wfile.write(b"")

    return
