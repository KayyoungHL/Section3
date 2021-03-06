import pickle
from personal_info import HOST, USER, PASSWORD
from pymongo import MongoClient
import pandas as pd
from tqdm import tqdm


def make_db_csv():
    DATABASE_NAME   = 'lol'
    COLLECTION_NAME = 'match_detail'
    MONGO_URI       = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

    import certifi
    ca = certifi.where()

    client = MongoClient(MONGO_URI, tlsCAFile=ca)
    database = client[DATABASE_NAME]
    collection = database[COLLECTION_NAME]

    # col = [
    #     "GameID", "GameVersion",
    #     "bTopID", "bTopChamp", "bTopPerkPrime", "bTopPerkPrime0", "bTopPerkPrime1", "bTopPerkPrime2", "bTopPerkPrime3", "bTopPerkSub", "bTopPerkSub0", "bTopPerkSub1", "bTopPerkStat0", "bTopPerkStat1", "bTopPerkStat2",
    #     "bJugID", "bJugChamp", "bJugPerkPrime", "bJugPerkPrime0", "bJugPerkPrime1", "bJugPerkPrime2", "bJugPerkPrime3", "bJugPerkSub", "bJugPerkSub0", "bJugPerkSub1", "bJugPerkStat0", "bJugPerkStat1", "bJugPerkStat2",
    #     "bMidID", "bMidChamp", "bMidPerkPrime", "bMidPerkPrime0", "bMidPerkPrime1", "bMidPerkPrime2", "bMidPerkPrime3", "bMidPerkSub", "bMidPerkSub0", "bMidPerkSub1", "bMidPerkStat0", "bMidPerkStat1", "bMidPerkStat2",
    #     "bBotID", "bBotChamp", "bBotPerkPrime", "bBotPerkPrime0", "bBotPerkPrime1", "bBotPerkPrime2", "bBotPerkPrime3", "bBotPerkSub", "bBotPerkSub0", "bBotPerkSub1", "bBotPerkStat0", "bBotPerkStat1", "bBotPerkStat2",
    #     "bSupID", "bSupChamp", "bSupPerkPrime", "bSupPerkPrime0", "bSupPerkPrime1", "bSupPerkPrime2", "bSupPerkPrime3", "bSupPerkSub", "bSupPerkSub0", "bSupPerkSub1", "bSupPerkStat0", "bSupPerkStat1", "bSupPerkStat2",
    #     "rTopID", "rTopChamp", "rTopPerkPrime", "rTopPerkPrime0", "rTopPerkPrime1", "rTopPerkPrime2", "rTopPerkPrime3", "rTopPerkSub", "rTopPerkSub0", "rTopPerkSub1", "rTopPerkStat0", "rTopPerkStat1", "rTopPerkStat2",
    #     "rJugID", "rJugChamp", "rJugPerkPrime", "rJugPerkPrime0", "rJugPerkPrime1", "rJugPerkPrime2", "rJugPerkPrime3", "rJugPerkSub", "rJugPerkSub0", "rJugPerkSub1", "rJugPerkStat0", "rJugPerkStat1", "rJugPerkStat2",
    #     "rMidID", "rMidChamp", "rMidPerkPrime", "rMidPerkPrime0", "rMidPerkPrime1", "rMidPerkPrime2", "rMidPerkPrime3", "rMidPerkSub", "rMidPerkSub0", "rMidPerkSub1", "rMidPerkStat0", "rMidPerkStat1", "rMidPerkStat2",
    #     "rBotID", "rBotChamp", "rBotPerkPrime", "rBotPerkPrime0", "rBotPerkPrime1", "rBotPerkPrime2", "rBotPerkPrime3", "rBotPerkSub", "rBotPerkSub0", "rBotPerkSub1", "rBotPerkStat0", "rBotPerkStat1", "rBotPerkStat2",
    #     "rSupID", "rSupChamp", "rSupPerkPrime", "rSupPerkPrime0", "rSupPerkPrime1", "rSupPerkPrime2", "rSupPerkPrime3", "rSupPerkSub", "rSupPerkSub0", "rSupPerkSub1", "rSupPerkStat0", "rSupPerkStat1", "rSupPerkStat2",
    #     "bBan1", "bBan2", "bBan3", "bBan4", "bBan5", "rBan1", "rBan2", "rBan3", "rBan4", "rBan5",
    #     "bWin", "rWin"
    # ]

    m = "metadata"
    f = "info"
    ps = "participants"
    sp = "statPerks"
    pk = "perks"
    p = "perk"
    st = "styles"
    s = "style"
    sl = "selections"
    de = "defense"
    fl = "flex"
    of = "offense"
    t = "teams"
    b = "bans"
    pu = "puuid"
    ch = "championId"

    data = []
    for i in tqdm(collection.find()):
        # data.append({"GameID":i[f]["gameId"], "GameVersion":i[f]["gameVersion"],
        # "bTopID":i[f][ps][0][pu], "bTopChamp":i[f][ps][0][ch], "bTopSpell0":i[f][ps][0]["summoner1Id"], "bTopSpell1":i[f][ps][0]["summoner2Id"], "bTopPerkPrime":i[f][ps][0][pk][st][0][s], "bTopPerkPrime0":i[f][ps][0][pk][st][0][sl][0][p], "bTopPerkPrime1":i[f][ps][0][pk][st][0][sl][1][p], "bTopPerkPrime2":i[f][ps][0][pk][st][0][sl][2][p], "bTopPerkPrime3":i[f][ps][0][pk][st][0][sl][3][p], "bTopPerkSub":i[f][ps][0][pk][st][1][s], "bTopPerkSub0":i[f][ps][0][pk][st][1][sl][0][p], "bTopPerkSub1":i[f][ps][0][pk][st][1][sl][1][p], "bTopPerkStat0":i[f][ps][0][pk][sp][de], "bTopPerkStat1":i[f][ps][0][pk][sp][fl], "bTopPerkStat2":i[f][ps][0][pk][sp][of],
        # "bJugID":i[f][ps][1][pu], "bJugChamp":i[f][ps][1][ch], "bJugSpell0":i[f][ps][1]["summoner1Id"], "bJugSpell1":i[f][ps][1]["summoner2Id"], "bJugPerkPrime":i[f][ps][1][pk][st][0][s], "bJugPerkPrime0":i[f][ps][1][pk][st][0][sl][0][p], "bJugPerkPrime1":i[f][ps][1][pk][st][0][sl][1][p], "bJugPerkPrime2":i[f][ps][1][pk][st][0][sl][2][p], "bJugPerkPrime3":i[f][ps][1][pk][st][0][sl][3][p], "bJugPerkSub":i[f][ps][1][pk][st][1][s], "bJugPerkSub0":i[f][ps][1][pk][st][1][sl][0][p], "bJugPerkSub1":i[f][ps][1][pk][st][1][sl][1][p], "bJugPerkStat0":i[f][ps][1][pk][sp][de], "bJugPerkStat1":i[f][ps][1][pk][sp][fl], "bJugPerkStat2":i[f][ps][1][pk][sp][of],
        # "bMidID":i[f][ps][2][pu], "bMidChamp":i[f][ps][2][ch], "bMicSpell0":i[f][ps][2]["summoner1Id"], "bMicSpell1":i[f][ps][2]["summoner2Id"], "bMidPerkPrime":i[f][ps][2][pk][st][0][s], "bMidPerkPrime0":i[f][ps][2][pk][st][0][sl][0][p], "bMidPerkPrime1":i[f][ps][2][pk][st][0][sl][1][p], "bMidPerkPrime2":i[f][ps][2][pk][st][0][sl][2][p], "bMidPerkPrime3":i[f][ps][2][pk][st][0][sl][3][p], "bMidPerkSub":i[f][ps][2][pk][st][1][s], "bMidPerkSub0":i[f][ps][2][pk][st][1][sl][0][p], "bMidPerkSub1":i[f][ps][2][pk][st][1][sl][1][p], "bMidPerkStat0":i[f][ps][2][pk][sp][de], "bMidPerkStat1":i[f][ps][2][pk][sp][fl], "bMidPerkStat2":i[f][ps][2][pk][sp][of],
        # "bBotID":i[f][ps][3][pu], "bBotChamp":i[f][ps][3][ch], "bBotSpell0":i[f][ps][3]["summoner1Id"], "bBotSpell1":i[f][ps][3]["summoner2Id"], "bBotPerkPrime":i[f][ps][3][pk][st][0][s], "bBotPerkPrime0":i[f][ps][3][pk][st][0][sl][0][p], "bBotPerkPrime1":i[f][ps][3][pk][st][0][sl][1][p], "bBotPerkPrime2":i[f][ps][3][pk][st][0][sl][2][p], "bBotPerkPrime3":i[f][ps][3][pk][st][0][sl][3][p], "bBotPerkSub":i[f][ps][3][pk][st][1][s], "bBotPerkSub0":i[f][ps][3][pk][st][1][sl][0][p], "bBotPerkSub1":i[f][ps][3][pk][st][1][sl][1][p], "bBotPerkStat0":i[f][ps][3][pk][sp][de], "bBotPerkStat1":i[f][ps][3][pk][sp][fl], "bBotPerkStat2":i[f][ps][3][pk][sp][of],
        # "bSupID":i[f][ps][4][pu], "bSupChamp":i[f][ps][4][ch], "bSupSpell0":i[f][ps][4]["summoner1Id"], "bSupSpell1":i[f][ps][4]["summoner2Id"], "bSupPerkPrime":i[f][ps][4][pk][st][0][s], "bSupPerkPrime0":i[f][ps][4][pk][st][0][sl][0][p], "bSupPerkPrime1":i[f][ps][4][pk][st][0][sl][1][p], "bSupPerkPrime2":i[f][ps][4][pk][st][0][sl][2][p], "bSupPerkPrime3":i[f][ps][4][pk][st][0][sl][3][p], "bSupPerkSub":i[f][ps][4][pk][st][1][s], "bSupPerkSub0":i[f][ps][4][pk][st][1][sl][0][p], "bSupPerkSub1":i[f][ps][4][pk][st][1][sl][1][p], "bSupPerkStat0":i[f][ps][4][pk][sp][de], "bSupPerkStat1":i[f][ps][4][pk][sp][fl], "bSupPerkStat2":i[f][ps][4][pk][sp][of],
        # "rTopID":i[f][ps][5][pu], "rTopChamp":i[f][ps][5][ch], "rTopSpell0":i[f][ps][5]["summoner1Id"], "rTopSpell1":i[f][ps][5]["summoner2Id"], "rTopPerkPrime":i[f][ps][5][pk][st][0][s], "rTopPerkPrime0":i[f][ps][5][pk][st][0][sl][0][p], "rTopPerkPrime1":i[f][ps][5][pk][st][0][sl][1][p], "rTopPerkPrime2":i[f][ps][5][pk][st][0][sl][2][p], "rTopPerkPrime3":i[f][ps][5][pk][st][0][sl][3][p], "rTopPerkSub":i[f][ps][5][pk][st][1][s], "rTopPerkSub0":i[f][ps][5][pk][st][1][sl][0][p], "rTopPerkSub1":i[f][ps][5][pk][st][1][sl][1][p], "rTopPerkStat0":i[f][ps][5][pk][sp][de], "rTopPerkStat1":i[f][ps][5][pk][sp][fl], "rTopPerkStat2":i[f][ps][5][pk][sp][of],
        # "rJugID":i[f][ps][6][pu], "rJugChamp":i[f][ps][6][ch], "rJugSpell0":i[f][ps][6]["summoner1Id"], "rJugSpell1":i[f][ps][6]["summoner2Id"], "rJugPerkPrime":i[f][ps][6][pk][st][0][s], "rJugPerkPrime0":i[f][ps][6][pk][st][0][sl][0][p], "rJugPerkPrime1":i[f][ps][6][pk][st][0][sl][1][p], "rJugPerkPrime2":i[f][ps][6][pk][st][0][sl][2][p], "rJugPerkPrime3":i[f][ps][6][pk][st][0][sl][3][p], "rJugPerkSub":i[f][ps][6][pk][st][1][s], "rJugPerkSub0":i[f][ps][6][pk][st][1][sl][0][p], "rJugPerkSub1":i[f][ps][6][pk][st][1][sl][1][p], "rJugPerkStat0":i[f][ps][6][pk][sp][de], "rJugPerkStat1":i[f][ps][6][pk][sp][fl], "rJugPerkStat2":i[f][ps][6][pk][sp][of],
        # "rMidID":i[f][ps][7][pu], "rMidChamp":i[f][ps][7][ch], "rMidSpell0":i[f][ps][7]["summoner1Id"], "rMidSpell1":i[f][ps][7]["summoner2Id"], "rMidPerkPrime":i[f][ps][7][pk][st][0][s], "rMidPerkPrime0":i[f][ps][7][pk][st][0][sl][0][p], "rMidPerkPrime1":i[f][ps][7][pk][st][0][sl][1][p], "rMidPerkPrime2":i[f][ps][7][pk][st][0][sl][2][p], "rMidPerkPrime3":i[f][ps][7][pk][st][0][sl][3][p], "rMidPerkSub":i[f][ps][7][pk][st][1][s], "rMidPerkSub0":i[f][ps][7][pk][st][1][sl][0][p], "rMidPerkSub1":i[f][ps][7][pk][st][1][sl][1][p], "rMidPerkStat0":i[f][ps][7][pk][sp][de], "rMidPerkStat1":i[f][ps][7][pk][sp][fl], "rMidPerkStat2":i[f][ps][7][pk][sp][of],
        # "rBotID":i[f][ps][8][pu], "rBotChamp":i[f][ps][8][ch], "rBotSpell0":i[f][ps][8]["summoner1Id"], "rBotSpell1":i[f][ps][8]["summoner2Id"], "rBotPerkPrime":i[f][ps][8][pk][st][0][s], "rBotPerkPrime0":i[f][ps][8][pk][st][0][sl][0][p], "rBotPerkPrime1":i[f][ps][8][pk][st][0][sl][1][p], "rBotPerkPrime2":i[f][ps][8][pk][st][0][sl][2][p], "rBotPerkPrime3":i[f][ps][8][pk][st][0][sl][3][p], "rBotPerkSub":i[f][ps][8][pk][st][1][s], "rBotPerkSub0":i[f][ps][8][pk][st][1][sl][0][p], "rBotPerkSub1":i[f][ps][8][pk][st][1][sl][1][p], "rBotPerkStat0":i[f][ps][8][pk][sp][de], "rBotPerkStat1":i[f][ps][8][pk][sp][fl], "rBotPerkStat2":i[f][ps][8][pk][sp][of],
        # "rSupID":i[f][ps][9][pu], "rSupChamp":i[f][ps][9][ch], "rSupSpell0":i[f][ps][9]["summoner1Id"], "rSupSpell1":i[f][ps][9]["summoner2Id"], "rSupPerkPrime":i[f][ps][9][pk][st][0][s], "rSupPerkPrime0":i[f][ps][9][pk][st][0][sl][0][p], "rSupPerkPrime1":i[f][ps][9][pk][st][0][sl][1][p], "rSupPerkPrime2":i[f][ps][9][pk][st][0][sl][2][p], "rSupPerkPrime3":i[f][ps][9][pk][st][0][sl][3][p], "rSupPerkSub":i[f][ps][9][pk][st][1][s], "rSupPerkSub0":i[f][ps][9][pk][st][1][sl][0][p], "rSupPerkSub1":i[f][ps][9][pk][st][1][sl][1][p], "rSupPerkStat0":i[f][ps][9][pk][sp][de], "rSupPerkStat1":i[f][ps][9][pk][sp][fl], "rSupPerkStat2":i[f][ps][9][pk][sp][of],
        # "bBan1":i[f][t][0][b][0][ch], 
        # "bBan2":i[f][t][0][b][1][ch], 
        # "bBan3":i[f][t][0][b][2][ch], 
        # "bBan4":i[f][t][0][b][3][ch], 
        # "bBan5":i[f][t][0][b][4][ch], 
        # "rBan1":i[f][t][1][b][0][ch], 
        # "rBan2":i[f][t][1][b][1][ch], 
        # "rBan3":i[f][t][1][b][2][ch], 
        # "rBan4":i[f][t][1][b][3][ch], 
        # "rBan5":i[f][t][1][b][4][ch],
        # "bWin":1 if i[f][t][0]["win"] else 0,
        # "rWin":1 if i[f][t][1]["win"] else 0})
        data.append({"GameID":i[f]["gameId"], "GameVersion":i[f]["gameVersion"],
        "bTopChamp":i[f][ps][0][ch], "bTopSpell0":i[f][ps][0]["summoner1Id"], "bTopSpell1":i[f][ps][0]["summoner2Id"], "bTopPerkPrime":i[f][ps][0][pk][st][0][s], "bTopPerkPrime0":i[f][ps][0][pk][st][0][sl][0][p], "bTopPerkSub":i[f][ps][0][pk][st][1][s],
        "bJugChamp":i[f][ps][1][ch], "bJugSpell0":i[f][ps][1]["summoner1Id"], "bJugSpell1":i[f][ps][1]["summoner2Id"], "bJugPerkPrime":i[f][ps][1][pk][st][0][s], "bJugPerkPrime0":i[f][ps][1][pk][st][0][sl][0][p], "bJugPerkSub":i[f][ps][1][pk][st][1][s],
        "bMidChamp":i[f][ps][2][ch], "bMicSpell0":i[f][ps][2]["summoner1Id"], "bMicSpell1":i[f][ps][2]["summoner2Id"], "bMidPerkPrime":i[f][ps][2][pk][st][0][s], "bMidPerkPrime0":i[f][ps][2][pk][st][0][sl][0][p], "bMidPerkSub":i[f][ps][2][pk][st][1][s],
        "bBotChamp":i[f][ps][3][ch], "bBotSpell0":i[f][ps][3]["summoner1Id"], "bBotSpell1":i[f][ps][3]["summoner2Id"], "bBotPerkPrime":i[f][ps][3][pk][st][0][s], "bBotPerkPrime0":i[f][ps][3][pk][st][0][sl][0][p], "bBotPerkSub":i[f][ps][3][pk][st][1][s],
        "bSupChamp":i[f][ps][4][ch], "bSupSpell0":i[f][ps][4]["summoner1Id"], "bSupSpell1":i[f][ps][4]["summoner2Id"], "bSupPerkPrime":i[f][ps][4][pk][st][0][s], "bSupPerkPrime0":i[f][ps][4][pk][st][0][sl][0][p], "bSupPerkSub":i[f][ps][4][pk][st][1][s],
        "rTopChamp":i[f][ps][5][ch], "rTopSpell0":i[f][ps][5]["summoner1Id"], "rTopSpell1":i[f][ps][5]["summoner2Id"], "rTopPerkPrime":i[f][ps][5][pk][st][0][s], "rTopPerkPrime0":i[f][ps][5][pk][st][0][sl][0][p], "rTopPerkSub":i[f][ps][5][pk][st][1][s],
        "rJugChamp":i[f][ps][6][ch], "rJugSpell0":i[f][ps][6]["summoner1Id"], "rJugSpell1":i[f][ps][6]["summoner2Id"], "rJugPerkPrime":i[f][ps][6][pk][st][0][s], "rJugPerkPrime0":i[f][ps][6][pk][st][0][sl][0][p], "rJugPerkSub":i[f][ps][6][pk][st][1][s],
        "rMidChamp":i[f][ps][7][ch], "rMidSpell0":i[f][ps][7]["summoner1Id"], "rMidSpell1":i[f][ps][7]["summoner2Id"], "rMidPerkPrime":i[f][ps][7][pk][st][0][s], "rMidPerkPrime0":i[f][ps][7][pk][st][0][sl][0][p], "rMidPerkSub":i[f][ps][7][pk][st][1][s],
        "rBotChamp":i[f][ps][8][ch], "rBotSpell0":i[f][ps][8]["summoner1Id"], "rBotSpell1":i[f][ps][8]["summoner2Id"], "rBotPerkPrime":i[f][ps][8][pk][st][0][s], "rBotPerkPrime0":i[f][ps][8][pk][st][0][sl][0][p], "rBotPerkSub":i[f][ps][8][pk][st][1][s],
        "rSupChamp":i[f][ps][9][ch], "rSupSpell0":i[f][ps][9]["summoner1Id"], "rSupSpell1":i[f][ps][9]["summoner2Id"], "rSupPerkPrime":i[f][ps][9][pk][st][0][s], "rSupPerkPrime0":i[f][ps][9][pk][st][0][sl][0][p], "rSupPerkSub":i[f][ps][9][pk][st][1][s],
        "bWin":1 if i[f][t][0]["win"] else 0,
        "rWin":1 if i[f][t][1]["win"] else 0})
        



    df = pd.DataFrame(data, columns=data[0].keys()).sort_values("GameID").reset_index(drop=True).set_index("GameID")
    print(df.head())

    df.to_csv("data.csv")


def rf_model(data):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.pipeline import make_pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    from category_encoders import OrdinalEncoder

    model = make_pipeline(
        OrdinalEncoder(),
        SimpleImputer(),
        RandomForestClassifier(n_estimators=500, min_samples_leaf=10, n_jobs=-1, criterion ='entropy', random_state=1)
    )
    train, test = train_test_split(data, random_state=42, shuffle=False)
    X_train = train.drop(["bWin","rWin"], axis = 1)
    y_train = train.bWin
    X_test  = test.drop(["bWin","rWin"], axis = 1)
    y_test  = test.bWin

    model.fit(X_train,y_train)


    print(accuracy_score(y_train, model.predict(X_train)))
    print(accuracy_score(y_test, model.predict(X_test)))

    return model


def deep_model(data):
    from sklearn.model_selection import train_test_split
    from category_encoders import OneHotEncoder
    import tensorflow as tf
    from tensorflow import keras 
    
    print("One Hot Encoding...")
    # ohe = OneHotEncoder(use_cat_names=False, cols=["GameVersion",
    #     "bTopID", "bTopChamp", "bTopPerkPrime", "bTopPerkPrime0", "bTopPerkPrime1", "bTopPerkPrime2", "bTopPerkPrime3", "bTopPerkSub", "bTopPerkSub0", "bTopPerkSub1", "bTopPerkStat0", "bTopPerkStat1", "bTopPerkStat2",
    #     "bJugID", "bJugChamp", "bJugPerkPrime", "bJugPerkPrime0", "bJugPerkPrime1", "bJugPerkPrime2", "bJugPerkPrime3", "bJugPerkSub", "bJugPerkSub0", "bJugPerkSub1", "bJugPerkStat0", "bJugPerkStat1", "bJugPerkStat2",
    #     "bMidID", "bMidChamp", "bMidPerkPrime", "bMidPerkPrime0", "bMidPerkPrime1", "bMidPerkPrime2", "bMidPerkPrime3", "bMidPerkSub", "bMidPerkSub0", "bMidPerkSub1", "bMidPerkStat0", "bMidPerkStat1", "bMidPerkStat2",
    #     "bBotID", "bBotChamp", "bBotPerkPrime", "bBotPerkPrime0", "bBotPerkPrime1", "bBotPerkPrime2", "bBotPerkPrime3", "bBotPerkSub", "bBotPerkSub0", "bBotPerkSub1", "bBotPerkStat0", "bBotPerkStat1", "bBotPerkStat2",
    #     "bSupID", "bSupChamp", "bSupPerkPrime", "bSupPerkPrime0", "bSupPerkPrime1", "bSupPerkPrime2", "bSupPerkPrime3", "bSupPerkSub", "bSupPerkSub0", "bSupPerkSub1", "bSupPerkStat0", "bSupPerkStat1", "bSupPerkStat2",
    #     "rTopID", "rTopChamp", "rTopPerkPrime", "rTopPerkPrime0", "rTopPerkPrime1", "rTopPerkPrime2", "rTopPerkPrime3", "rTopPerkSur", "rTopPerkSur0", "rTopPerkSur1", "rTopPerkStat0", "rTopPerkStat1", "rTopPerkStat2",
    #     "rJugID", "rJugChamp", "rJugPerkPrime", "rJugPerkPrime0", "rJugPerkPrime1", "rJugPerkPrime2", "rJugPerkPrime3", "rJugPerkSur", "rJugPerkSur0", "rJugPerkSur1", "rJugPerkStat0", "rJugPerkStat1", "rJugPerkStat2",
    #     "rMidID", "rMidChamp", "rMidPerkPrime", "rMidPerkPrime0", "rMidPerkPrime1", "rMidPerkPrime2", "rMidPerkPrime3", "rMidPerkSur", "rMidPerkSur0", "rMidPerkSur1", "rMidPerkStat0", "rMidPerkStat1", "rMidPerkStat2",
    #     "rBotID", "rBotChamp", "rBotPerkPrime", "rBotPerkPrime0", "rBotPerkPrime1", "rBotPerkPrime2", "rBotPerkPrime3", "rBotPerkSub", "rBotPerkSub0", "rBotPerkSub1", "rBotPerkStat0", "rBotPerkStat1", "rBotPerkStat2",
    #     "rSupID", "rSupChamp", "rSupPerkPrime", "rSupPerkPrime0", "rSupPerkPrime1", "rSupPerkPrime2", "rSupPerkPrime3", "rSupPerkSur", "rSupPerkSur0", "rSupPerkSur1", "rSupPerkStat0", "rSupPerkStat1", "rSupPerkStat2",
    #     "bBan1", "bBan2", "bBan3", "bBan4", "bBan5", "rBan1", "rBan2", "rBan3", "rBan4", "rBan5"])
    
    # ohe.fit_transform(data).to_csv("df_ohe.csv")
    
    ohe = OneHotEncoder(use_cat_names=False, cols=["GameVersion",
        "bTopChamp", "bTopPerkPrime", "bTopPerkPrime0", "bTopPerkSub", "bTopSpell0", "bTopSpell1",
        "bJugChamp", "bJugPerkPrime", "bJugPerkPrime0", "bJugPerkSub", "bJugSpell0", "bJugSpell1",
        "bMidChamp", "bMidPerkPrime", "bMidPerkPrime0", "bMidPerkSub", "bMicSpell0", "bMicSpell1",
        "bBotChamp", "bBotPerkPrime", "bBotPerkPrime0", "bBotPerkSub", "bBotSpell0", "bBotSpell1",
        "bSupChamp", "bSupPerkPrime", "bSupPerkPrime0", "bSupPerkSub", "bSupSpell0", "bSupSpell1",
        "rTopChamp", "rTopPerkPrime", "rTopPerkPrime0", "rTopPerkSub", "rTopSpell0", "rTopSpell1",
        "rJugChamp", "rJugPerkPrime", "rJugPerkPrime0", "rJugPerkSub", "rJugSpell0", "rJugSpell1",
        "rMidChamp", "rMidPerkPrime", "rMidPerkPrime0", "rMidPerkSub", "rMidSpell0", "rMidSpell1",
        "rBotChamp", "rBotPerkPrime", "rBotPerkPrime0", "rBotPerkSub", "rBotSpell0", "rBotSpell1",
        "rSupChamp", "rSupPerkPrime", "rSupPerkPrime0", "rSupPerkSub", "rSupSpell0", "rSupSpell1"
        ])

    data = ohe.fit_transform(data)
    data.to_csv("df_ohe1.csv")

    
    print("deep learning modeling...")
    model = keras.Sequential([
        keras.layers.Dense(2048, activation='relu', input_shape=(1844,)), 
        keras.layers.Dense(2048, activation='relu'), 
        keras.layers.Dense(2048, activation='relu'), 
        keras.layers.Dense(2048, activation='relu'), 
        keras.layers.Dense(2048, activation='relu'), 
        keras.layers.Dense(2048, activation='relu'), 
        keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', 
        loss='binary_crossentropy', 
        metrics=['accuracy'])

    train, test = train_test_split(data, random_state=42, shuffle=False)
    X_train = train.drop(["bWin","rWin"], axis = 1)
    y_train = train.bWin
    X_test  = test.drop(["bWin","rWin"], axis = 1)
    y_test  = test.bWin


    model.fit(X_train, y_train, epochs=15)

    print(predict(model, X_test, y_test))

    return model


def predict(model, X_test, y_test):
    import numpy as np
    model.predict(X_test)
    y_pred = np.array([[1] if i >= 0.5 else [0] for i in model.predict(X_test)])

    count = 0
    n = len(y_test)
    for i in range(n):
        if y_test[i] == y_pred[i]:
            count += 1

    return count/n


if __name__ == "__main__":

    print("Making db as CSV file...")
    make_db_csv()
    print("data loading...")
    data = pd.read_csv("data.csv", index_col="GameID")
    model = rf_model(data)
    # data = pd.read_csv("df_ohe1.csv", index_col="GameID")
    # model = deep_model(data)
    with open("rf_model.pkl", "bw") as f:
        pickle.dump(model, f)
        