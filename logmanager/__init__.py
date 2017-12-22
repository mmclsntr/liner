import time
import sys

def log(tag, msg):
  sys.stdout.write(str(time.time()) + "\t" + str(tag) + "\t" + str(msg) + "\n")
  sys.stdout.flush()
  
def error(tag, msg):
  sys.stderr.write(str(time.time()) + "\t" + str(tag) + "\t" + str(msg) + "\n")
  sys.stderr.flush()
