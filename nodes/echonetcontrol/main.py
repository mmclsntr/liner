from echonetlitecontroller import ParentMain
import airconditioner_power
import airconditioner_temperature

import time

parent = ParentMain({})

airconpower = airconditioner_power.NodeMain({"IP Address": "192.168.1.34"}, parent=parent)
aircontemperature = airconditioner_temperature.NodeMain({"IP Address": "192.168.1.34"}, parent=parent)


while True:
  time.sleep(1)
  print(airconpower.read())
  print(aircontemperature.read())
  time.sleep(1)
  airconpower.write(True)
  aircontemperature.write(40)
  time.sleep(1)
  print(airconpower.read())
  print(aircontemperature.read())
  time.sleep(1)
  airconpower.write(False)
  aircontemperature.write(18)
