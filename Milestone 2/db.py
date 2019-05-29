import json
from pymongo import MongoClient
from random import randint


def create_db(client,tf_idf):
        db=client.CS121Project3
        for term in tf_idf:
                db.ICSindex.insert(json.loads(json.dumps({'term':term,'URLs':tf_idf[term]})), check_keys=False)
