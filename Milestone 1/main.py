import os
from index import Index
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient(port=27017)
    if not 'CS121Project3' in client.list_database_names():
        Index().loop_urls(client)



    
    
    