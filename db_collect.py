import requests
import json
import time

import pandas as pd
from tqdm import tqdm

from personal_info import API_KEY


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
    print("User ID collecting...")
    leagues = ["challenger", "grandmaster"]
    summoner_id = [] ## 저장할 사전
    for league in leagues:
        url = f"https://kr.api.riotgames.com/lol/league/v4/{league}leagues/by-queue/RANKED_SOLO_5x5?api_key={API_KEY}"
        req = requests.get(url)
        entries = req.json()['entries']

        for i in entries:
            summoner_id.append(i['summonerId'])

    puuids = {}
    for user_id in tqdm(summoner_id):
        url2 = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/{user_id}?api_key={API_KEY}"
        
        try:
            req2 = requests.get(url2)
            time.sleep(0.9)
            req2 = response_checker(user_id, url2, req2)
            if not req2 == None: ## 기타 에러코드 발생 안할 시
                puuids[req2.json()['name']] = req2.json()['puuid']
        except: # 예외발생. 주로 타임아웃!
            print()
            print(user_id+"에서 예외 발생", req2.status_code)
            continue

    filename = "puuids.json"
    with open(filename, "w") as f:
        json.dump(puuids, f)


def collect_match_id():
    print("Match ID collecting...")
    filename = f"puuids.json"
    with open(filename, "r") as f :
        user_list = json.load(f)
    
    match_list = set()
    for puuid in tqdm(user_list.values()):
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&type=ranked&start=0&count=20&api_key={API_KEY}"
        try:
            req = requests.get(url)
            time.sleep(1)
            req = response_checker(puuid, url, req)

            if not req == None:
                match = set(req.json())
                match_list.update(match)
        except:
            print()
            print(puuid+"에서 예외 발생", req.status_code)
            continue

    filename = "match_list.json"
    try:
        with open("done_"+filename, "r") as f:
            done_match_list = set(json.load(f))
        match_list = match_list - done_match_list
    except:
        None

    match_list = sorted(list(match_list))
    with open(filename, "w") as f:
        json.dump(match_list, f)


def collect_match_detail():
    print("Match detail collecting...")
    filename = "match_list.json"
    with open(filename, "r") as f:
        match_list = set(json.load(f))
    
    done_match = set()
    match_detail = []

    for match in tqdm(match_list):
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{match}?api_key={API_KEY}"
        try:
            req = requests.get(url)
            time.sleep(0.83)
            req = response_checker(match, url, req)
            if not req == None:
                match_detail.append(req.json())
                done_match.add(match)
        except:
            print()
            print(match+"에서 예외 발생", req.status_code)
            continue
    
    from db_update import db_upload
    db_upload(match_detail)

    with open("done_"+filename, "r") as f:
        done_match_list = set(json.load(f))
    done_match_list.update(done_match)
    new_match_list = sorted(list(done_match_list))

    with open("done_"+filename, "w") as f:
        json.dump(new_match_list, f)


if __name__ == "__main__":
    collect_id()
    collect_match_id()
    collect_match_detail()