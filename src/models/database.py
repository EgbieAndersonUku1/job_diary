###################################################################
# Author   : Egbie Uku
# Database : Database
###################################################################

from flask.ext.pymongo import pymongo

class DataBase(object):
    """Database stores the entire records of the users"""

    URI = 'mongodb://127.0.0.1:27017'
    DATABASE = None

    @staticmethod
    def initialize():
        """The initialize method initialize the pymongo database"""
        client = pymongo.MongoClient(DataBase.URI)
        DataBase.DATABASE = client['users']

    @staticmethod
    def insert_one(collection, data):
        """insert_one(str) -> return(none)

        @params:
        collections: The name of the table(collections) to save to.
        data       : The data to insert into the database's collection

        Inserts data into a collection(table) for a given database.
        """
        DataBase.DATABASE[collection].insert_one(data)

    @staticmethod
    def search(collections, query, key, limit_num):
        """search(str, value, value, tuple) -> return(cursor)

        @params:
        collections: A table name for the database.
        query      : Queries the database based on the query.
        key        : Sorts the data based on the key.
        limit_num  : Limits the data returned.
        return     : Returns a cursor object.

        Takes a given query and queries the database for that information.
        """
        field, value = key
        if query == None:
            return DataBase.DATABASE[collections].find().sort(field, value).limit(limit_num) # query all documents       
        return DataBase.DATABASE[collections].find(query).sort(field, value).limit(limit_num)        

    @staticmethod
    def find_one(collections, query):
        """find_one(str, value) -> return(dict)

        @params:
        collections: A table name from the database
        query      : The information to query from the database
        returns    : A single row if found

        Return a single obj from from the database.
        """
        return DataBase.DATABASE[collections].find_one(query)

    @staticmethod
    def delete_row(collections, query):
        """delete_row(str, value) -> return(None)

        @params:
        collections: A table name from the database
        query      : The information to query from the database
      
        Deletes and entry from the row.
        """
        DataBase.DATABASE[collections].find_one_and_delete(query)

    @staticmethod
    def update_row(collections, row_id, query):
        """update_row(str, value) -> return(None)

        @params:
        collections: A table name from the database
        query      : The information to query from the database
        
        Updates a single row in the table.
        """
        DataBase.DATABASE[collections].update_one({'row_id': row_id}, {'$set':query})
        