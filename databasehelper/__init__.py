import pymongo
import configmanager
from bson.codec_options import CodecOptions

__addr = configmanager.get_key('DATABASE', 'DatabaseAddr')
__port = int(configmanager.get_key('DATABASE', 'DatabasePort'))

__client = pymongo.MongoClient(__addr, __port)

def get_database(name: str) -> pymongo.database:
  database = __client[name]
  return database

def isExistCollection(database, name: str) -> bool:
  collist = list_collection_names(database)
  for colname in collist:
    if colname == name:
      return True
  return False

def list_collection_names(database) -> list:
  return database.collection_names()

def create_collection(database, name: str) -> pymongo.collection:
  database.create_collection(name, capped=True, size=256 * 1024, max=100)
  return get_collection(database, name)
  
def get_collection(database, name: str) -> pymongo.collection:
  collection = database[name]
  return collection

def insert(collection, doc):
  return collection.insert_one(doc)

def find(collection, filter, params = None):
  if params == None:
    return collection.find(filter)
  else:
    return collection.find(filter, **params)

def update(collection, filter, update):
  return collection.update_one(filter, {'$set': update})

def delete(collection, filter):
  return collection.delete_one(filter)

def drop(collection):
  return collection.drop()
