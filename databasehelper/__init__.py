import pymongo
import configmanager

__addr = configmanager.get_key('DATABASE', 'DatabaseAddr')
__port = int(configmanager.get_key('DATABASE', 'DatabasePort'))

__client = pymongo.MongoClient(__addr, __port)

def get_database(name: str) -> pymongo.database:
  database = __client[name]
  return database

def get_collection(database, name: str) -> pymongo.collection:
  collection = database[name]
  #database.command({"convertToCapped": name, "size": 1024 * 1024})
  return collection

def insert(collection, doc):
  return collection.insert_one(doc)

def find(collection, filter):
  return collection.find(filter)

def update(collection, filter, update):
  return collection.update_one(filter, {'$set': update})

def delete(collection, filter):
  return collection.delete_one(filter)

def drop(collection):
  return collection.drop()
