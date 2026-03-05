from pymongo import MongoClient
from config import mongo_connection_uri


def create_database(name: str):
    client: MongoClient = MongoClient(mongo_connection_uri)
    db = client[name]
    collection = db["temp"]
    post = {}
    collection.insert_one(post)
    client.close()


def delete_database(name: str):
    client: MongoClient = MongoClient(mongo_connection_uri)
    client.drop_database(name)
    client.close()


def update_database_name(old_name: str, new_name: str):
    client: MongoClient = MongoClient(mongo_connection_uri)
    if old_name == new_name:
        return
    for i in client[old_name].list_collection_names():
        old_col = client[old_name][i]
        new_col = client[new_name][i]
        docs = old_col.find()
        new_col.insert_many(docs)
    client.drop_database(old_name)


def get_database_collections(name: str):
    pass