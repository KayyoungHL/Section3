import re
import requests
import json
import time

import pandas as pd
from tqdm import tqdm

from api_info import API_KEY


# def response_checker(data, url, request):
#     if request.status_code == 200: # response가 정상이면 바로 맨 밑으로 이동하여 정상적으로 코드 실행
#         return request
#     elif request.status_code == 429:
#         print('api cost full : infinite loop start')
#         print('loop location : ',data)
#         start_time = time.time()
#         times = 0
#         while True: # 429error가 끝날 때까지 무한 루프
#             if request.status_code == 429:
#                 print(f'try 10 second wait time: {times}\tresponse_code: {request.status_code}', end="\r")
#                 time.sleep(10)
#                 times += 10
#                 request = requests.get(url)

#             elif request.status_code == 200: #다시 response 200이면 loop escape
#                 print('total wait time : ', time.time() - start_time)
#                 print('recovery api cost')
#                 return request
#     else:
#         print(request.status_code)
#         return None

# username = "Chieftain00"
# url2 = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username}/KR1?api_key={API_KEY}"
# req2 = requests.get(url2)
# time.sleep(1)
# req2 = response_checker(username, url2, req2)

# puuids = {}
# if not req2 == None: ## 기타 에러코드 발생시
#     puuid = req2.json()['puuid']
#     puuids[username] = puuid

# print(puuids)
# puuid = puuids[username]
# url3 = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?api_key={API_KEY}"
# req3 = requests.get(url3)
# time.sleep(1)
# req3 = response_checker(puuid, url3, req3)

# match_list = set()
# if not req3 == None:
#     match_list.update(set(req3.json()))

# print(match_list)

# for match in tqdm(match_list):
#     url4 = f"https://asia.api.riotgames.com/lol/match/v5/matches/{match}?api_key={API_KEY}"
#     req4 = requests.get(url4)
#     time.sleep(1)
#     req4 = response_checker(match, url4, req4)
#     match_detail = []
#     if not req4 == None:
#         data = req4.json()
#         if data["info"]["queueId"] == 420:
#             match_detail.append(data)
#         else:
#             print("솔로랭크 겜 아니네!")    

# with open("test.json", "w") as f:
#     json.dump(match_detail, f)

filename = "match_list.json"
with open(filename, "r") as f:
    match_list = set(json.load(f))

with open("done_"+filename, "r") as f:
    done_match_list = set(json.load(f))

with open("match_detail.json", "r") as f:
    print("데이터",len(json.load(f)))


# with open("done_match_list.json", "w") as f:
#     json.dump(sorted(new_done_match_list), f)
print(len(match_list),len(done_match_list))
print(len(match_list|done_match_list))
