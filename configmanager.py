import os
import configparser

INI_FILE = os.path.dirname(os.path.abspath(__file__)) + '/config.ini'

__config = configparser.SafeConfigParser()
__config.read(INI_FILE, encoding='utf8')

def get_section(section: str) -> str:
  return __config.options(section)

def get_key(section: str, key: str) -> str:
  return __config.get(section, key)

def set_value(section, key, value) -> None:
  __config.set(section, key, value)
  return

if __name__ == '__main__':
  print(get_section('DATABASE'))
