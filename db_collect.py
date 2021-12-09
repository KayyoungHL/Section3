import requests
import json
import time

import pandas as pd
from tqdm import tqdm

from api_info import API_KEY


def response_checker(data, url, request):
    if request.status_code == 200: # response가 정상이면 바로 맨 밑으로 이동하여 정상적으로 코드 실행
        return request
    elif request.status_code == 429:
        print('api cost full : infinite loop start')
        print('loop location : ',data)
        start_time = time.time()
        times = 0
        while True: # 429error가 끝날 때까지 무한 루프
            if request.status_code == 429:
                print(f'try 10 second wait time: {times}\nresponse_code: {request.status_code}', end="\r")
                time.sleep(10)
                times += 10
                request = requests.get(url)

            elif request.status_code == 200: #다시 response 200이면 loop escape
                print('total wait time : ', time.time() - start_time)
                print('recovery api cost')
                return request
    else:
        print(end="\r")
        print(f"\nReponse_code: error {request.status_code} from '{data}'")
        return None


def collect_id():
    leagues = ["challenger", "grandmaster"]
    summoner_id = [] ## 저장할 사전
    for league in leagues:
        url = f"https://kr.api.riotgames.com/lol/league/v4/{league}leagues/by-queue/RANKED_SOLO_5x5?api_key={API_KEY}"
        req = requests.get(url)
        entries = req.json()['entries']

        for i in entries:
            summoner_id.append(i['summonerName'])

    puuids = {}
    for username in tqdm(summoner_id):
        url2 = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username}/KR1?api_key={API_KEY}"
        try:
            req2 = requests.get(url2)
            time.sleep(0.85)
            req2 = response_checker(username, url2, req2)
            if not req2 == None: ## 기타 에러코드 발생시
                puuid = req2.json()['puuid']
                puuids[username] = puuid
        except: # 예외발생. 주로 타임아웃!
            print(username+"에서 예외 발생", req2.status_code)
            continue

    filename = "puuids.json"
    with open(filename, "w") as f:
        json.dump(puuids, f)


def collect_match_id(league):
    filename = f"{league}_puuid.json"
    with open(filename, "r") as f :
        user_list = json.load(f)
    
    match_list = set()
    for puuid in tqdm(user_list.values()):
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?api_key={API_KEY}"
        try:
            req = requests.get(url)
            time.sleep(1)
            req = response_checker(puuid, url, req)

            if not req == None:
                match = set(req.json())
                match_list.update(match)
        except:
            print(puuid+"에서 예외 발생", req.status_code)
            continue

    filename = "match_list.json"
    try:
        with open(filename, "r") as f:
            prior_match_list = set(json.load(f))
        match_list.update(prior_match_list)
    except:
        None

    match_list = sorted(list(match_list),reverse=True)
    with open(filename, "w") as f:
        json.dump(match_list, f)


def collect_match_detail():
    filename = "match_list.json"
    with open(filename, "r") as f:
        match_list = json.load(f)

    not_solo = set()
    match_detail = []
    count = 0
    for match in tqdm(match_list):
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{match}?api_key={API_KEY}"
        try:
            req = requests.get(url)
            time.sleep(0.82)
            req = response_checker(match, url, req)
            if not req == None:
                data = req.json()
                if data["info"]["queueId"] == 420:
                    match_detail.append(data)
                else:
                    count += 1
                    not_solo.add(match)
                    print("\r솔로랭크 겜 아니네!", count, data["info"]["queueId"])
        except:
            print(match+"에서 예외 발생", req.status_code)
            continue

    new_match_list = sorted(list(set(match_list)-not_solo), reverse=True)
    with open(filename, "w") as f:
        json.dump(new_match_list, f)                

    with open("match_detail.json", "a") as f:
        json.dump(match_detail, f)


if __name__ == "__main__":
    collect_id()
    # collect_match_id()
    # collect_match_detail()