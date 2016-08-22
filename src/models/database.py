###################################################################
# Author   : Egbie Uku
# Database
###################################################################

import pymongo

class DataBase(object):
    """Database stores the entire records of the users"""

    URI = 'mongodb://127.0.0.1:27017'
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(DataBase.URI)
        DataBase.DATABASE = client['users']

    @staticmethod
    def insert(collection, data):
        """insert(str) -> return(none)

        collections: The name of the table(collections) to save to
        data : The data to insert into the database's collection

        Inserts data into a collection(table) for a given database.
        """
        DataBase.DATABASE[collection].insert(data)

    @staticmethod
    def search(collections, query):
        """search(str, value) -> return(cursor)

        collections: A table name from the database
        query : The data to query from the database
        return: returns a cursor

        Takes a query and queries the database for information.
        """
        return DataBase.DATABASE[collections].find(query)

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



#DataBase.initialize()
