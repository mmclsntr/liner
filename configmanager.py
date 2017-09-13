import configparser

INI_FILE = 'config.ini'

__config = configparser.SafeConfigParser()
__config.read(INI_FILE, encoding='utf8')

def get_section(section):
  return __config.options(section)

def get_key(section, key):
  return __config.get(section, key)

def set_value(section, key, value):
  __config.set(section, key, value)
  return

if __name__ == '__main__':
  print(get_section('DATABASE'))
