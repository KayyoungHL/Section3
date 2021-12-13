from flask import Flask, render_template, request


def create_app():
    app = Flask(__name__)
    @app.route("/dashboard")
    def dashboard():
        return render_template("index.html"), 200
        
    @app.route("/")
    def users():
        from personal_info import API_KEY
        import requests
        import pandas as pd
        import numpy as np

        message = None
        code = 200
        username = request.args.get("username", None)
        if username == None :
            return render_template("result.html", chk = False), 200
        
        url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={API_KEY}"
        req = requests.get(url)
        if req.status_code == 200:
            user_id = req.json()["id"]

            url2 = f"https://kr.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{user_id}?api_key={API_KEY}"
            req2 = requests.get(url2)
            if req2.status_code == 200:
                data = req2.json()
                recently_version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
                if not data["gameQueueConfigId"] == 420:
                    message = "It's Not a Rank Game"
                    code = 405
                else:
                    p = "participants"
                    c = "championId"
                    s1 = "spell1Id"
                    s2 = "spell2Id"
                    pk = "perks"
                    pp = "perkStyle"
                    ps = "perkSubStyle"
                    pid = "perkIds"
                    index = data["gameId"]
                    bt = 0
                    bj = 1
                    bm = 2
                    bb = 3
                    bs = 4
                    rt = 5
                    rj = 6
                    rm = 7
                    rb = 8
                    rs = 9
                    input_data = {"GameVersion":recently_version,
                        "bTopChamp":data[p][bt][c], "bTopSpell0":data[p][bt][s1], "bTopSpell1":data[p][bt][s2], "bTopPerkPrime":data[p][bt][pk][pp], "bTopPerkPrime0":data[p][bt][pk][pid][0], "bTopPerkSub":data[p][bt][pk][ps],
                        "bJugChamp":data[p][bj][c], "bJugSpell0":data[p][bj][s1], "bJugSpell1":data[p][bj][s2], "bJugPerkPrime":data[p][bj][pk][pp], "bJugPerkPrime0":data[p][bj][pk][pid][0], "bJugPerkSub":data[p][bj][pk][ps],
                        "bMidChamp":data[p][bm][c], "bMicSpell0":data[p][bm][s1], "bMicSpell1":data[p][bm][s2], "bMidPerkPrime":data[p][bm][pk][pp], "bMidPerkPrime0":data[p][bm][pk][pid][0], "bMidPerkSub":data[p][bm][pk][ps],
                        "bBotChamp":data[p][bb][c], "bBotSpell0":data[p][bb][s1], "bBotSpell1":data[p][bb][s2], "bBotPerkPrime":data[p][bb][pk][pp], "bBotPerkPrime0":data[p][bb][pk][pid][0], "bBotPerkSub":data[p][bb][pk][ps],
                        "bSupChamp":data[p][bs][c], "bSupSpell0":data[p][bs][s1], "bSupSpell1":data[p][bs][s2], "bSupPerkPrime":data[p][bs][pk][pp], "bSupPerkPrime0":data[p][bs][pk][pid][0], "bSupPerkSub":data[p][bs][pk][ps],
                        "rTopChamp":data[p][rt][c], "rTopSpell0":data[p][rt][s1], "rTopSpell1":data[p][rt][s2], "rTopPerkPrime":data[p][rt][pk][pp], "rTopPerkPrime0":data[p][rt][pk][pid][0], "rTopPerkSub":data[p][rt][pk][ps],
                        "rJugChamp":data[p][rj][c], "rJugSpell0":data[p][rj][s1], "rJugSpell1":data[p][rj][s2], "rJugPerkPrime":data[p][rj][pk][pp], "rJugPerkPrime0":data[p][rj][pk][pid][0], "rJugPerkSub":data[p][rj][pk][ps],
                        "rMidChamp":data[p][rm][c], "rMidSpell0":data[p][rm][s1], "rMidSpell1":data[p][rm][s2], "rMidPerkPrime":data[p][rm][pk][pp], "rMidPerkPrime0":data[p][rm][pk][pid][0], "rMidPerkSub":data[p][rm][pk][ps],
                        "rBotChamp":data[p][rb][c], "rBotSpell0":data[p][rb][s1], "rBotSpell1":data[p][rb][s2], "rBotPerkPrime":data[p][rb][pk][pp], "rBotPerkPrime0":data[p][rb][pk][pid][0], "rBotPerkSub":data[p][rb][pk][ps],
                        "rSupChamp":data[p][rs][c], "rSupSpell0":data[p][rs][s1], "rSupSpell1":data[p][rs][s2], "rSupPerkPrime":data[p][rs][pk][pp], "rSupPerkPrime0":data[p][rs][pk][pid][0], "rSupPerkSub":data[p][rs][pk][ps]
                    }
                    df = pd.DataFrame(input_data, columns=input_data.keys(), index=[index])
                    import pickle
                    with open("rf_model.pkl","rb") as f:
                        model = pickle.load(f)
                    
                    result = model.predict_proba(df)

                    champ = requests.get("http://ddragon.leagueoflegends.com/cdn/11.24.1/data/en_US/champion.json").json()["data"]
                    champ_dict = {}
                    for i in champ.keys():
                        champ_dict[int(champ[i]["key"])] = i
                    spell = requests.get("http://ddragon.leagueoflegends.com/cdn/11.24.1/data/en_US/summoner.json").json()["data"]
                    spell_dict = {}
                    for i in spell.keys():
                        spell_dict[int(spell[i]["key"])] = i
                    
                    rune = requests.get("https://ddragon.leagueoflegends.com/cdn/10.6.1/data/en_US/runesReforged.json").json()
                    rune_dict = {}
                    for i in rune:
                        rune_dict[int(i["id"])] = i["icon"]
                    
                    return render_template("result.html", chk=True, message=message, data=data[p], result = np.around(result[0]*100,3), gv = recently_version, champ=champ_dict, spell=spell_dict, rune=rune_dict), 200
            else: 
                message = "This user is not playing now..."
                code = 405
        else:
            message = "User Not Found"
            code = 404

        return render_template("result.html", message=message), code
        

    return app
    

if __name__ == "__main__":  
    app = create_app()
    app.run(debug=True)