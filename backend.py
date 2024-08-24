import tkinter.messagebox
import requests,os
import json,asyncio
import urllib.request,datetime,base64,tkinter,window2,aiohttp,threading,time
class Backend:
    __my_puuid = None
    __my_index = None
    my_data = None
    game_data = None
    __all_matches = []
    champ_name = None
    __tasks = []
    __match_information = []
    match_results = []
    def __init__(self,region,game_name,game_tag,api,count) -> None:
        self.region = region
        self.game_name = game_name
        self.game_tag = game_tag
        self.api = api
        self.count = count
        
    async def returnList(self):
        # WORKING ####################### #############################
        # await self.getPUUID()
        # await self.getMatchIds(self.region,self.api,self.__my_puuid,self.count)
        # for each_match in self.__all_matches:
            
        #     await self.getMatchData(self.region,each_match,self.api)## sets my data in the current game
        #     self.format_my_data() # formats my current data into a list
        # return self.__match_information  ## all games in a list 
        ###############################################################################
                                    #testing
        await self.getPUUID()
        await self.getMatchIds(self.region,self.api,self.__my_puuid,self.count)
        return await self.create_tasks(self.region,self.__all_matches,self.api)
        

    async def create_tasks(self, region, all_matches, api):
        self.__tasks = []
        temp_list = []
        
        async with aiohttp.ClientSession() as session:
            for matchId in all_matches:
                url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={api}"
                task = asyncio.create_task(session.get(url, ssl=False))
                self.__tasks.append(task)

            # Gather the responses
            responses = await asyncio.gather(*self.__tasks)
            
            for response in responses:
                try:
                    # Parse the JSON response
                    game_data = await response.json()
                    
                    # Get the index of the participant
                    self.__my_index = game_data["metadata"]["participants"].index(self.__my_puuid)
                    
                    # Store participant and game data
                    self.my_data = game_data["info"]["participants"][self.__my_index]
                    self.game_data = game_data
                    
                    # Format and store the data
                    formatted = self.format_my_data()
                    print(formatted)
                    temp_list.append(formatted)
                    
                except Exception as e:
                    print(f"An error occurred: {e}")
                    continue
        
        return temp_list








    async def getPUUID(self):
        
        url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{self.game_name}/{self.game_tag}?api_key={self.api}"
        async with aiohttp.ClientSession() as session:
            request = await asyncio.create_task(session.get(url,ssl=False))
            
            response = await request.json()
            self.__my_puuid = response.get("puuid")
    












    async def getMatchIds(self,region,api,puuid,count):
        url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&api_key={api}"
        async with aiohttp.ClientSession() as session:
            request = await asyncio.create_task(session.get(url,ssl=False))

            self.__all_matches = await request.json()
   
    async def getMatchData(self,region,matchId,api):
            
        url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={api}"    
        async with aiohttp.ClientSession() as session:
            request = await asyncio.create_task(session.get(url,ssl=False))
            game_data= await request.json()
            for participant in game_data["metadata"]["participants"]:
                if self.__my_puuid == participant:
                    self.__my_index = game_data["metadata"]["participants"].index(participant)
            self.my_data = game_data["info"]["participants"][self.__my_index]
            self.game_data = game_data
    
    def format_my_data(self):
        print("----------------------->",self.my_data)
        game_duration = self.game_data["info"]["gameDuration"]
        date = self.game_data["info"]["gameEndTimestamp"]
        queueId = self.game_data["info"]["queueId"]
        champion_icon = self.my_data["championName"]
        kills = self.my_data["kills"]
        deaths = self.my_data["deaths"]
        #self.champ_name = self.my_data["championName"]
        assists = self.my_data["assists"]
        items = [self.my_data["item0"],self.my_data["item1"],self.my_data["item2"],
                 self.my_data["item3"],self.my_data["item4"],self.my_data["item5"],
                 self.my_data["item6"]]
        # profile_icon = self.my_data["profileIcon"]
        total_damage_to_champions = self.my_data["totalDamageDealtToChampions"]
        total_damage_taken = self.my_data["totalDamageTaken"]
        cs = self.my_data["totalMinionsKilled"] + self.my_data["neutralMinionsKilled"]
        win = self.my_data["win"]
        return [champion_icon,game_duration,kills,deaths,assists,cs,items,queueId,total_damage_to_champions,total_damage_taken,win,date]
        
        

    def getItems(slef,lst):
        for each_item in lst:
            path = f"items/{each_item}.png"
            if os.path.exists(path):
                
                continue
            else:
                url = f"https://ddragon.leagueoflegends.com/cdn/14.13.1/img/item/{each_item}.png"
                img_data = requests.get(url)
                with open(path,"wb") as handler:
                    handler.write(img_data.content)
    
    def getIcon(slef,champ_name):
        path = f"champion_icons/{champ_name}.png"
        if os.path.exists(path):
            
            return path
        else:
            url = f"https://ddragon.leagueoflegends.com/cdn/14.13.1/img/champion/{champ_name}.png"
            img_data = requests.get(url)
            with open(path,"wb") as handler:
                handler.write(img_data.content)

    async def getQueues(self):
        async with aiohttp.ClientSession() as session:
            request = await asyncio.create_task(session.get("https://static.developer.riotgames.com/docs/lol/queues.json",ssl=False))
            data = await request.json()

        
        
            os.makedirs("queueIds",exist_ok=True)
            file_path = os.path.join("queueIds","queues.json")
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

    def loadJsonQueues(self, queueId):
        with open("queueIds/queues.json") as f:
            data = json.load(f)
    
        game_map = "Unknown Map"
        description = "Unknown Description"

        for each in data:
            if each["queueId"] == queueId:
                game_map = each["map"]
                description = each["description"] if each["description"] else "No Description"
                break
        
        return game_map, description

    

    def timestamp_to_days_ago(self,timestamp_ms):
        # Convert the given timestamp from milliseconds to seconds
        timestamp_s = timestamp_ms / 1000
        
        # Convert the timestamp to a datetime object
        date_time = datetime.datetime.fromtimestamp(timestamp_s)
        
        # Get the current time
        now = datetime.datetime.now()
        
        # Calculate the difference between now and the given datetime
        time_difference = now - date_time
        
        # Calculate the difference in days
        days_ago = time_difference.days
        
        # Return the formatted string
        return days_ago

class Profile:
    
    def getAPI(slef,path):
        
        try:  
            file = open(path)
            text = file.readline()
            splitted_array = text.split(':')
            port = splitted_array[2]
            auth = splitted_array[3]
            
            return int(port),auth
        except FileNotFoundError:
            
            tkinter.messagebox.showinfo("lockfile not found", "League of Legends is not running.\nPlease start League of Legends first")
            exit()
            
            
class AutoPick:
  
    def getPickableChamps(self,port,auth):
        url_pickable = f"https://127.0.0.1:{port}/lol-champ-select/v1/pickable-champion-ids"

        pickable_champion_request = requests.get(url=url_pickable,auth=('riot',auth),verify=False)
        pickable_champions = pickable_champion_request.json()
        
        return pickable_champions
    def getActorCellId(self,port,auth):
        url_actor = f"https://127.0.0.1:{port}/lol-champ-select/v1/session"

        actor_request = requests.get(url=url_actor,auth=('riot',auth),verify=False)
        actor = actor_request.json()
        localPlayerCellId = actor["localPlayerCellId"]

        return int(localPlayerCellId)
    def pick_event(self,champion_id,localPlayerCellId,pickable_champions,port,auth):
        url_phase = f"https://127.0.0.1:{port}/lol-champ-select/v1/session"

        phase_request = requests.get(url=url_phase, auth=('riot', auth), verify=False)
        phase_request.raise_for_status()
        phase_data = phase_request.json()
        phase = phase_data["timer"]["phase"]
        if phase == "BAN_PICK":
            if champion_id not in pickable_champions:
                print(f"Champion ID {champion_id} is not pickable.")
                return

            url_actions = f"https://127.0.0.1:{port}/lol-champ-select/v1/session"
            try:
                actions_request = requests.get(url=url_actions, auth=('riot', auth), verify=False)
                actions_request.raise_for_status()
                actions_data = actions_request.json()
                actions = actions_data["actions"]
            except requests.RequestException as e:
                print(f"Error fetching actions: {e}")
                return

            action_id = None
            for lst in actions:
                for action in lst:
                    if action["actorCellId"] == localPlayerCellId and action["isInProgress"] and not action["completed"] and action["type"] == "pick":
                        action_id = action["id"]
                        break
                if action_id is not None:
                    break

            if action_id is None:
                print("No valid action found for picking.")
                return

            put_json = {
                "actorCellId": localPlayerCellId,
                "championId": champion_id,
                "completed": True,
                "id": action_id,
                "isAllyAction": True,
                "type": "pick"
            }
            url_put = f"https://127.0.0.1:{port}/lol-champ-select/v1/session/actions/{action_id}"
            try:
                put_request = requests.patch(url=url_put, json=put_json, auth=('riot', auth), verify=False)
                put_request.raise_for_status()
                print(f"Champion {champion_id} successfully picked.")
            except requests.RequestException as e:
                print(f"Error executing pick action: {e}")

def getChampionsWithID():
    url_version = "https://ddragon.leagueoflegends.com/api/versions.json"
    version_request = requests.get(url=url_version)
    latest_version = version_request.json()[0]
    print(latest_version)
    url_champions = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
    request = requests.get(url=url_champions)
    response = request.json()
    
    champion_dict = {champion["id"]: champion["key"] for champion in response["data"].values()}
    return champion_dict
def getIcon(champ_name):
        path = f"champion_icons/{champ_name}.png"
        if not os.path.exists(path):
            
            url = f"https://ddragon.leagueoflegends.com/cdn/14.13.1/img/champion/{champ_name}.png"
            img_data = requests.get(url)
            with open(path,"wb") as handler:
                handler.write(img_data.content)


class AutoBan:

    def getActorCellId(self,port,auth):
        
            url_actor = f"https://127.0.0.1:{port}/lol-champ-select/v1/session"

            actor_request = requests.get(url=url_actor,auth=('riot',auth),verify=False)
            actor = actor_request.json()
            localPlayerCellId = actor["localPlayerCellId"]

            return int(localPlayerCellId)     
        
            

    def getBannableChamps(self,port,auth):
        url_bannable = f"https://127.0.0.1:{port}/lol-champ-select/v1/bannable-champion-ids"

        bannable_champion_request = requests.get(url=url_bannable,auth=('riot',auth),verify=False)
        bannable_champions = bannable_champion_request.json()
        
        return bannable_champions

    def ban_event(self,champion_id,localPlayerCellId,pickable_champions,port,auth):
        url_phase = f"https://127.0.0.1:{port}/lol-champ-select/v1/session"

        phase_request = requests.get(url=url_phase, auth=('riot', auth), verify=False)
        phase_request.raise_for_status()
        print("ban req sent!")
        phase_data = phase_request.json()
        phase = phase_data["timer"]["phase"]
        if phase == "BAN_PICK":
            if champion_id not in pickable_champions:
                print(f"Champion ID {champion_id} is not pickable.")
                return

            url_actions = f"https://127.0.0.1:{port}/lol-champ-select/v1/session"
            try:
                actions_request = requests.get(url=url_actions, auth=('riot', auth), verify=False)
                actions_request.raise_for_status()
                actions_data = actions_request.json()
                actions = actions_data["actions"]
            except requests.RequestException as e:
                print(f"Error fetching actions: {e}")
                return

            action_id = None
            for lst in actions:
                for action in lst:
                    if action["actorCellId"] == localPlayerCellId and action["isInProgress"] and not action["completed"] and action["type"] == "ban":
                        action_id = action["id"]
                        break
                if action_id is not None:
                    break

            if action_id is None:
                print("No valid action found for picking.")
                return

            put_json = {
                "actorCellId": localPlayerCellId,
                "championId": champion_id,
                "completed": True,
                "id": action_id,
                "isAllyAction": True,
                "type": "ban"
            }
            url_put = f"https://127.0.0.1:{port}/lol-champ-select/v1/session/actions/{action_id}"
            try:
                put_request = requests.patch(url=url_put, json=put_json, auth=('riot', auth), verify=False)
                put_request.raise_for_status()
                print(f"Champion {champion_id} successfully picked.")
            except requests.RequestException as e:
                print(f"Error executing pick action: {e}")

class AutoAccept:
    def accept_event(port,auth):
        url = f"https://127.0.0.1:{port}/lol-matchmaking/v1/ready-check/accept"

        request = requests.post(url=url,auth=('riot',auth),verify=False)

class AutoSpells:
    def spells_event(spell1,spell2,port,auth):
        id_spell= {
                "Flash": 4,
                "Heal": 7,
                "Ghost": 6,
                "Teleport": 12,
                "Barrier": 21,
                "Cleanse": 1,
                "Ignite": 14,
                "Exhaust": 3,
                "Smite": 11,
                "Clarity": 30,
                "Snowball": 32
            }
        
        spell_id1 = id_spell[spell1]
        spell_id2 = id_spell[spell2]
        url = f"https://127.0.0.1:{port}/lol-champ-select/v1/session/my-selection"
        patch_json = {
        
        "selectedSkinId": 0,
        "spell1Id": spell_id1,
        "spell2Id": spell_id2,
        "wardSkinId": 0
        }
        request = requests.patch(url=url,json=patch_json,auth=('riot',auth),verify=False)



    def download_spells():
        url_summoner = "https://ddragon.leagueoflegends.com/cdn/14.13.1/data/en_US/summoner.json"
        request = requests.get(url=url_summoner)
        jsn = request.json()
        all_spells = []
        jsn = jsn["data"]
        for data in jsn:
            all_spells.append(jsn[data]["id"])
        for each_spell in all_spells:
            url = f"https://ddragon.leagueoflegends.com/cdn/14.13.1/img/spell/{each_spell}.png"
            img_data = requests.get(url)
            with open(f"spell_icons/{each_spell}.png","wb") as handler:
                handler.write(img_data.content)
    def get_gamemode(port,auth):

        url = f"https://127.0.0.1:{port}/lol-lobby/v2/lobby"
        request = requests.get(url= url,auth=('riot',auth),verify=False) 
        response = request.json()
        gamemode = response["gameConfig"]["gameMode"]
        return gamemode
    

class InGame:
    def getPUUID(game_name,game_tag,api):
        

        url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{game_tag}?api_key={api}"
        request = requests.get(url=url)
        response = request.json()
        my_puuid = response.get("puuid")
        return my_puuid
        
    async def getCurrentMatchData(puuiddd,auth):
        
        url = f"https://eun1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuiddd}?api_key=RGAPI-6e925dd7-2bdc-4a78-ba23-35b3a895a417"
        async with aiohttp.ClientSession() as session:
            # request = await session.get(url, ssl=False)
            # response = await request.json()
        
            game_info = []
            all_data = []
            data_recieved = False
            if True:#status code =200
                data_recieved = True
                
                # response = request.json() # OG
                
                with open("ingame.json","r",encoding="utf-8") as f:
                    response = json.load(f)
                
                game_info.append(response["gameMode"])
                game_info.append(response["gameQueueConfigId"])
                tasks = []
                for participant in response["participants"]:
                    summoner_id = participant["summonerId"]
                    puuid = participant["puuid"]
                    tasks.append(InGame.getPlayerRank(summoner_id, auth,session))
                    tasks.append(InGame.getSummonerLevel(puuid, auth,session))

                results = await asyncio.gather(*tasks)
                
                for i, participant in enumerate(response["participants"]):
                    puid = participant["puuid"]
                    teamid = participant["teamId"]
                    championId = participant["championId"]
                    profileIconId = participant["profileIconId"]

                    tier, rank, winrate = results[i * 2]  # Indexing into the gathered results
                    level = results[i * 2 + 1]
                    riotID = participant["riotId"]

                    all_data.append([puid, teamid, championId, profileIconId, tier, rank, winrate, level, riotID])
                        # for participant in response["participants"]:
                        #     print(f"Praticipant: {participant}")
                        #     puid = participant["puuid"]
                        #     teamid = participant["teamId"]
                        #     championId = participant["championId"]
                        #     profileIconId = participant["profileIconId"]

                        #     tier,rank,winrate = InGame.getPlayerRank(participant["summonerId"],auth)
                            
                        #     level = InGame.getSummonerLevel(participant["puuid"],auth)
                        #     riotID = participant["riotId"]
                            
                        #     all_data.append([puid,teamid,championId,profileIconId,tier,rank,winrate,level,riotID])
                return all_data, True, game_info            
                #     return all_data,data_recieved,game_info
                # else:
                    
                #     return (all_data,False,None)
            
        ##async with aiohttp.ClientSession() as session:
            # request = await session.get(url, ssl=False)
            # response = await request.json()
        
            # game_info = []
            # all_data = []
            # data_recieved = False
            # if request.status == 200:
            #     data_recieved = True
                
            #     # response = request.json() # OG
                
            #     with open("ingame.json","r",encoding="utf-8") as f:
            #         response = json.load(f)
                
            #     game_info.append(response["gameMode"])
            #     game_info.append(response["gameQueueConfigId"])
                
            #     for participant in response["participants"]:
                    
            #         puid = participant["puuid"]
            #         teamid = participant["teamId"]
            #         championId = participant["championId"]
            #         profileIconId = participant["profileIconId"]

            #         tier,rank,winrate = InGame.getPlayerRank(participant["summonerId"],auth)
                    
            #         level = InGame.getSummonerLevel(participant["puuid"],auth)
            #         riotID = participant["riotId"]
            #         print(riotID)
            #         all_data.append([puid,teamid,championId,profileIconId,tier,rank,winrate,level,riotID])
                    
            #     return all_data,data_recieved,game_info
            # else:
                
            #     return (all_data,False,None)
    async def getSummonerLevel(puuiddd, auth, session):
        url = f"https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuiddd}?api_key={auth}"
        
        async with session.get(url) as get_level:
            get_level = await get_level.json()
            
        level = get_level.get("summonerLevel", None)
        return level
    # def getSummonerLevel(puuiddd,auth):
        
    #     url = f"https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuiddd}?api_key={auth}"
    #     get_level = requests.get(url)
    #     get_level = get_level.json()
    #     level = get_level["summonerLevel"]
    #     return level
    async def getPlayerRank(summoner_id, auth, session):
        url = f"https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={auth}"
        
        async with session.get(url) as rank_req:
            rank_data = await rank_req.json()

        if not isinstance(rank_data, list) or len(rank_data) == 0:
            return None, None, None

        tiers = {
            "IRON": 0,
            "BRONZE": 1,
            "SILVER": 2,
            "GOLD": 3,
            "PLATINUM": 4,
            "EMERALD": 5,
            "DIAMOND": 6,
            "MASTER": 7,
            "GRANDMASTER": 8,
            "CHALLENGER": 9
        }

        ranks = {
            "IV": 0,
            "III": 1,
            "II": 2,
            "I": 3
        }

        winrates = []
        divisions = []
        two_ranks = []

        for entry in rank_data:
            try:
                if entry["tier"] in tiers:
                    divisions.append(entry["tier"])
                if entry["rank"] in ranks:
                    two_ranks.append(entry["rank"])

                wins = entry.get("wins", 0)
                losses = entry.get("losses", 0)

                if wins + losses > 0:
                    winrate = int(wins / (wins + losses) * 100)
                    winrates.append(winrate)
                else:
                    winrates.append(0)

            except KeyError:
                continue

        if not divisions or not two_ranks or not winrates:
            return None, None, None

        max_index = winrates.index(max(winrates))
        tier_value = tiers.get(divisions[max_index], 0)
        rank_value = ranks.get(two_ranks[max_index], 0)

        return divisions[max_index], two_ranks[max_index], winrates[max_index]   
    # def getPlayerRank(summoner_id, auth):
    #     url = f"https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={auth}"
    #     rank_req = requests.get(url)
    #     rank_data = rank_req.json()
        
    #     if not isinstance(rank_data, list) or len(rank_data) == 0:
    #         return None, None, None
        
    #     tiers = {
    #         "IRON": 0,
    #         "BRONZE": 1,
    #         "SILVER": 2,
    #         "GOLD": 3,
    #         "PLATINUM": 4,
    #         "EMERALD": 5,
    #         "DIAMOND": 6,
    #         "MASTER": 7,
    #         "GRANDMASTER": 8,
    #         "CHALLENGER": 9
    #     }
        
    #     ranks = {
    #         "IV": 0,
    #         "III": 1,
    #         "II": 2,
    #         "I": 3
    #     }
        
    #     winrates = []
    #     divisions = []
    #     two_ranks = []

    #     for entry in rank_data:
    #         try:
    #             if entry["tier"] in tiers:
    #                 divisions.append(entry["tier"])
    #             if entry["rank"] in ranks:
    #                 two_ranks.append(entry["rank"])
                
    #             wins = entry.get("wins", 0)
    #             losses = entry.get("losses", 0)
                
    #             if wins + losses > 0:
    #                 winrate = int(wins / (wins + losses) * 100)
    #                 winrates.append(winrate)
    #             else:
    #                 winrates.append(0)
                    
    #         except KeyError:
    #             continue
        
    #     if not divisions or not two_ranks or not winrates:
    #         return None, None, None
        
    #     max_index = winrates.index(max(winrates))
    #     tier_value = tiers.get(divisions[max_index], 0)
    #     rank_value = ranks.get(two_ranks[max_index], 0)
        
    #     return divisions[max_index], two_ranks[max_index], winrates[max_index]
                
    













