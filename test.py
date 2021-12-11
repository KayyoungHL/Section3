import re
import requests
import json
import time

import pandas as pd
from tqdm import tqdm

from personal_info import API_KEY
from pymongo import MongoClient

# HOST = 'cluster0.mevzi.mongodb.net'
# USER = 'KHL'
# PASSWORD = 'dlrudgml'
# DATABASE_NAME = 'lol'
# COLLECTION_NAME = 'match_detail'
# MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

# import certifi
# ca = certifi.where()

# client = MongoClient(MONGO_URI, tlsCAFile=ca)
# database = client[DATABASE_NAME]
# collection = database[COLLECTION_NAME]

# match_list = []
# for i in tqdm(collection.find()):
#     match_list.append(i["metadata"]["matchId"])

# with open("done_match_list.json", "w") as f:
#     json.dump(match_list, f)

with open("done_match_list.json", "r") as f:
    print(len(json.load(f)))