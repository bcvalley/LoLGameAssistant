import requests
import warnings,aiohttp,ijson,asyncio

api = ""
port = 0
def best_champion(lst):
    winrate = {}
    ## has to find the champion with most wins
    for each in lst:
        if each[0] not in winrate:
            if each[1] == True:
                winrate[each[0]] = (1,1)
            else:
                winrate[each[0]] = (0,1)
        else:
            if each[1] == True:
                winrate[each[0]] = (winrate[each[0]][0]+1,winrate[each[0]][1]+1)
            else:
                winrate[each[0]] = (winrate[each[0]][0],winrate[each[0]][1]+1)
    return winrate 
# Suppress only the InsecureRequestWarning
warnings.simplefilter('ignore', requests.packages.urllib3.exceptions.InsecureRequestWarning)
def id_to_champ(id):
    for key,value in champ_dictionary.items():
        if int(value) == id:
            return key



def getChampionsWithID():
    url_version = "https://ddragon.leagueoflegends.com/api/versions.json"
    version_request = requests.get(url=url_version)
    latest_version = version_request.json()[0]
    url_champions = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
    request = requests.get(url=url_champions)
    response = request.json()
    champion_dict = {champion["id"]: champion["key"] for champion in response["data"].values()}
    return champion_dict
async def getNameAndTag(puuid,port,api):
        
        url = f"https://127.0.0.1:{port}/lol-summoner/v2/summoners/puuid/{puuid}"
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth('riot',api)) as session:
            request = await session.get(url,ssl=False)

        
            response = await request.json()
            return f"{response['gameName']}#{response['tagLine']}"
    
async def get_200_games(puuid, port, api):
    champ_ids = []
    name_and_tag= await getNameAndTag(puuid, port, api)
    name_and_tag = name_and_tag.split("#")
    name = name_and_tag[0]
    tag = name_and_tag[1]
    url = f'https://127.0.0.1:{port}/lol-match-history/v1/products/lol/{puuid}/matches?begIndex=0&endIndex=100'
    async with aiohttp.ClientSession(auth=aiohttp.BasicAuth('riot',api)) as session:
        async with session.get(url,ssl=False) as request:
        
            
            async for prefix,event,value in ijson.parse_async(request.content):
                
                if prefix.endswith(".championId") and event == "number":
                    champion_id = value
                if prefix.endswith(".win") and event == "boolean":
                    win = value
                    if champion_id <= 1000:  # Filtering out invalid champion IDs
                        champ_ids.append((champion_id, win))

        pair = extract_max_pair(best_champion(champ_ids))
        champ = id_to_champ(pair[0])
        
        winrate = pair[1][0]/pair[1][1]
        return champ,round(winrate*100),pair[1][1],name,tag
   
    

    
def extract_max_pair(lst): 
    max_second_value = -float('inf')  # Start with the lowest possible value
    max_pair = None  # This will store the pair with the maximum second value

    # Iterate through each key-value pair in the dictionary
    for key, (first, second) in lst.items():
        # Check if the current second value is greater than the current maximum
        if second > max_second_value:
            # Update the maximum second value and the corresponding pair
            max_second_value = second
            max_pair = (key, (first, second))

    return max_pair 


champ_dictionary = getChampionsWithID()

async def start_func(puuids):
    data = []
    for puuid in puuids:
        lst = await get_200_games(puuid, port, api)
        champ = lst[0]
        wr = lst[1]
        games = lst[2]
        name,tag = lst[3],lst[4]
        data.append((champ,wr,games,name,tag))
    return data




# def getNameAndTag(puuid,port,api):
        
#         url = f"https://127.0.0.1:{port}/lol-summoner/v2/summoners/puuid/{puuid}"
#         request = requests.get(url,auth=('riot',api),verify=False)
#         response = request.json()
#         if request.status_code == 200:

#             return response["gameName"],response["tagLine"]
#         else:
#             return "error","error"
# game_name,tag = getNameAndTag(puuids[3], port, api)
# print(game_name,tag)
# game_name,tag = getNameAndTag(puuids[4], port, api)
# print(game_name,tag)