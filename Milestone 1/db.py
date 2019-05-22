import json
from pymongo import MongoClient
from random import randint


def create_db(tf_idf):
    client = MongoClient(port=27017)
    db=client.CS121Project3

    for term in tf_idf:
        db.JSONTEST.insert(json.loads(json.dumps({'term':term,'URLs':tf_idf[term]})), check_keys=False)
