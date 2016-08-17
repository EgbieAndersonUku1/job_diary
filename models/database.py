import pymongo

class DataBase(object):

    URI = 'mongodb://127.0.0.1:27017'

    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(DataBase.URI)
        DataBase.DATABASE = client['users']

    @staticmethod
    def insert(collection, data):
        DataBase.DATABASE[collection].insert(data)

    @staticmethod
    def search(collections, query):
        return DataBase.DATABASE[collections].find(query)

    @staticmethod
    def find_one(collections, query):
        return DataBase.DATABASE[collections].find_one(query)

    @staticmethod
    def delete_row(collections, query):
        DataBase.DATABASE[collections].find_one_and_delete(query)
        return DataBase.DATABASE[collections].count(query)



DataBase.initialize()
