from pymongo import MongoClient
import json
from personal_info import HOST, USER, PASSWORD


def db_upload(data):

    DATABASE_NAME   = 'lol'
    COLLECTION_NAME = 'match_detail'
    MONGO_URI       = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

    import certifi
    ca = certifi.where()

    client = MongoClient(MONGO_URI, tlsCAFile=ca)
    database = client[DATABASE_NAME]
    collection = database[COLLECTION_NAME]
    print("Mongo DB uploading...")
    collection.insert_many(documents=data)
    print("Finish")

if __name__ == "__main__": pass
    # with open("match_detail.json", "r") as f:
    #     match_detail = json.load(f)
    # db_upload(match_detail)