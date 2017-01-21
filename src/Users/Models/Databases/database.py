###################################################################
# Author   : Egbie Uku
# Database : Database
###################################################################

import pymongo

class DataBase(object):
    """Database stores the entire records of the users"""

    URI = 'mongodb://127.0.0.1:27017'
    DATABASE = None

    @staticmethod
    def initialize():
        """The initialize method initialize the pymongo database"""
        client = pymongo.MongoClient(DataBase.URI)
        DataBase.DATABASE = client['users']
        job_details = client['users']['jobs_details']
        cache = client['users']['cache']

        # created index one line because mongo does query compound indexes properly
        job_details.create_index([('user_id', pymongo.DESCENDING)])
        job_details.create_index([('hours', pymongo.DESCENDING)])
        job_details.create_index([('loc', pymongo.DESCENDING)])
        job_details.create_index([('start_time', pymongo.DESCENDING)])
        job_details.create_index([('finish_time', pymongo.DESCENDING)])
        job_details.create_index([('daily_rate', pymongo.DESCENDING)])
        job_details.create_index([('day', pymongo.DESCENDING)])
        job_details.create_index([('job_title', pymongo.DESCENDING)])
        job_details.create_index([('hourly_rate', pymongo.DESCENDING)])
        job_details.create_index([('row_id', pymongo.DESCENDING)])
        job_details.create_index([('date', pymongo.DESCENDING)])
        job_details.create_index([('year', pymongo.DESCENDING)])
        job_details.create_index([('month', pymongo.DESCENDING)])
        job_details.create_index([('is_shift_confirmed', pymongo.DESCENDING)])

        # create an index for the cache
        cache.create_index([('current_jobs', pymongo.DESCENDING)])
        cache.create_index([('worked_jobs', pymongo.DESCENDING)])

    @staticmethod
    def insert_one(collection, data):
        """insert_one(str) -> return(none)
        Inserts data into a collection(table) for a given database.

        :parameters
            - collection: The table name for the data to be inserted into.
            - data: The data will be inserted into the collection.

        """
        DataBase.DATABASE[collection].insert_one(data)

    @staticmethod
    def search(collections, query, key, limit_num):
        """search(str, value, value, tuple) -> return(cursor)

        Takes a given query and queries the database for that information.

        parameters:
         - collections: A table name for the database.
         - query      : Queries the database based on the query.
         - key        : Sorts the data based on the key.
         - limit_num  : Limits the data returned. 0 values returns all values.
         - return     : Returns a cursor object.
        """
        field, value = key
        if query == None:
            return DataBase.DATABASE[collections].find().sort(field, value).limit(limit_num) # query all documents
        elif query == None and key == None:
            return DataBase.DATABASE[collections].find()
        return DataBase.DATABASE[collections].find(query).sort(field, value).limit(limit_num)

    @staticmethod
    def find_one(collections, query):
        """find_one(str, dict) -> return(dict)

        Return a json object from from the database.

        parameters:
           - collections: A table name from the database
           - query      : The information to query from the database
           - returns    : A single row if found
        """
        return DataBase.DATABASE[collections].find_one(query)

    @staticmethod
    def delete_row(collections, query):
        """delete_row(str, dict) -> return(None)

        Deletes and entry from the row.

        parameters:
           - collections: A table name from the database
           - query      : The information to query from the database
        """
        DataBase.DATABASE[collections].find_one_and_delete(query)

    @staticmethod
    def update(collections, key, value, query):
        """update_row(str, str, dict) -> return(None)

        Updates a single row in the table.

        parameters:
           - collections: A table name from the database
           - key        : The key finds the specific row to update
           - value      : Replaces the old value with the new value.
           - query      : The information used to update to the database

        """
        DataBase.DATABASE[collections].update_one({key: value}, {'$set':query})
