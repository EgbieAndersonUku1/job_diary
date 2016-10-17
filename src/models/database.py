###################################################################
# Author   : Egbie Uku
# Database
###################################################################

from flask.ext.pymongo import pymongo


class DataBase(object):
    """Database stores the entire records of the users"""

    URI = 'mongodb://127.0.0.1:27017'
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(DataBase.URI)
        DataBase.DATABASE = client['users']

    @staticmethod
    def insert_one(collection, data):
        """insert_one(str) -> return(none)

        collections: The name of the table(collections) to save to
        data : The data to insert into the database's collection

        Inserts data into a collection(table) for a given database.
        """
        DataBase.DATABASE[collection].insert_one(data)

    @staticmethod
    def search(collections, query, key, limit_num=5):
        """search(str, value) -> return(cursor)

        collections: A table name from the database
        query      : The data to query from the database
        key        : The key for the data to sort out
        limit_num  :  Returns a default limit of 5 documents
        return     : returns a cursor

        Takes a query and queries the database for information.
        """
        field, value = key
        if query == None:
            return DataBase.DATABASE[collections].find().sort(field, value).limit(limit_num) # query all documents
        return DataBase.DATABASE[collections].find(query).sort(field, value).limit(limit_num)

    @staticmethod
    def find_one(collections, query):
        """find_one(str, value) -> return(dict)

        collections: A table name from the database
        query : The information to query from the database
        returns: A single row if found

        Returns the data from the database.
        """
        return DataBase.DATABASE[collections].find_one(query)

    @staticmethod
    def delete_row(collections, query):
        """delete_row(str, value) -> return(dict)

        collections: A table name from the database
        query : The information to query from the database
        returns: A single row if found

        Deletes and entry from the row.
        """
        DataBase.DATABASE[collections].find_one_and_delete(query)
        return DataBase.DATABASE[collections].count(query)


    def get_count(self, collections, query):
        """returns the number of documents inside a collection"""
        if query == None:
            return DataBase.DATABASE[collections].find().count()
        return self.search(collections, query).count()

DataBase.initialize()
