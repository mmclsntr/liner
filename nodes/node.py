import threading

class Node:
  def __init__(self, config: dict, parent=None):
    pass

  def read(self):
    pass

  def write(self, value):
    pass 

  def __del__(self):
    pass

class Parent:
  def __init__(self, config: dict):
    pass

  def keep_running(self, target):
    pass

  def read(self, params=None):
    pass

  def write(self, value, params=None):
    pass

  def __del__(self):
    pass
