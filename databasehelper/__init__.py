import pymongo

class DataBaseHelper:
  __addr = 'localhost'
  __port = 27017
  def __init__(self):
    self.__client = pymongo.MongoClient(self.__addr, self.__port)

  def get_database(self, name: str) -> pymongo.database:
    self.database = self.__client[name]
    return self.database

  def get_collection(self, database, name: str) -> pymongo.collection:
    self.collection = database[name]
    database.command({"convertToCapped": name, "size": 1024 * 1024})
    return self.collection

  def insert(self, collection, doc):
    return collection.insert_one(doc)

  def find(self, collection, filter):
    return self.collection.find(filter)

  def update(self, collection, filter, update):
    return self.collection.update_one(filter, update)

  def delete(self, collection, filter):
    return self.collection.delete_one(filter)

  def drop(self, collection):
    return collection.drop()
