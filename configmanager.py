# Copyright 2018 Shintaro Yamasaki <hitorans@icloud.com>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
  with open(INI_FILE, "w") as f:
    __config.write(f)
  return

if __name__ == '__main__':
  print(get_section('DATABASE'))
