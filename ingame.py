import customtkinter as ctk

from PIL import Image ,ImageTk
import backend,requests,urllib3,chardet
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os,json,test_algo
PATH = os.getcwd()
BACKGROUND = "#242424" #BACKGROUND COLOR 
app = None # Main CTK
x =220 # start of the UI
WIDTH = 0 #screen width
HEIGHT = 0 # screen height
font = ('Montserrat',17,'bold') # FONT USED 
widgets =[] # labels,buttons and etc are placed here to destroy
already_clicked = False
icon_references = []
all_data = None
checking_for_match = False
prof = backend.Profile()

import game_dir
def get_config_dir():
    path = f"{PATH}\\saved_config\\game_dir.json"
    
    if os.path.exists(path):
        with open(path) as p:
            config = json.load(p)
            return config["game_dir"]


game_dir.game_dir = get_config_dir()
game_dir.game_dir += "/lockfile"
profile_info = backend.Profile()
port,api = profile_info.getAPI(game_dir.game_dir)
test_algo.port = port
test_algo.api = api
data_recieved = False
dictionary = backend.getChampionsWithID()
game_info = []
Y_level = 250
Y_level_second = 250

def live_game_draw(appp):
    global app,WIDTH,HEIGHT,already_clicked,data_recieved,all_data,dictionary,game_info
    
    app = appp
    WIDTH = app.winfo_screenwidth()
    HEIGHT = app.winfo_screenheight()
     
    
    all_data,data_recieved,game_info = refresh()
    cv_width, cv_height = get_canvas_dimentions()
    canvas = ctk.CTkCanvas(app, width=cv_width, height=cv_height, bg=BACKGROUND, highlightthickness=0)
    canvas.grid(row=4,column=3,columnspan=12,rowspan=9,sticky="nw",padx=40,pady=30)
    if is_in_session(port,api):
        draw_champ_select(canvas)
    elif data_recieved == False :
        req_label = ctk.CTkLabel(app,text="You are neither in a game nor in a champ select",text_color="red",font=('Montserrat',40,'bold'),anchor="center")
        req_label.grid(row=3,column=6,columnspan=5,rowspan=2)
        image_size = (60,60)
        loaded_refresh_image = Image.open(f"{PATH}\\icons\\refresh.png")
        refresh_resized = loaded_refresh_image.resize(image_size)
        refresh_image = ImageTk.PhotoImage(refresh_resized)
        check_for_match_button = ctk.CTkButton(app,image=refresh_image,text="",command=lambda: live_game_draw(app),bg_color=BACKGROUND,fg_color=BACKGROUND,anchor="center",hover_color="yellow")
        check_for_match_button.grid(row=4,column=6,rowspan=3,columnspan=5)
        
        # for x in widgets:
        #     x.destroy()
        #app.after(1000, live_game_draw, app)
        widgets.append(req_label)
        widgets.append(check_for_match_button)
    
    else:   
        try:
            req_label.place_forget()
        except:AttributeError
    
        draw_map()
        draw_live_label()
        draw_gamemap()
        draw_ranked()
        draw_red_point()
        draw_both_teams(canvas)
        
    
    

    
def draw_map():
    global app,game_info
    
    map = game_info[0]
    if map == "CLASSIC":
        open_summoners_rift_image = Image.open(f"{PATH}\\icons\\summoners_rift.jpg")
        sr_resized_image = open_summoners_rift_image.resize((1146,200))
        ingame_image = ImageTk.PhotoImage(sr_resized_image)
        summoners_rift_image = ctk.CTkLabel(app,image=ingame_image,text="")
        summoners_rift_image.grid(row=0,column=3,rowspan=4,columnspan=12,sticky='e',padx=40)
        widgets.append(summoners_rift_image)
    elif map == "ARAM":
        open_summoners_rift_image = Image.open(f"{PATH}\\icons\\aram.jpg")
        sr_resized_image = open_summoners_rift_image.resize((1146,200))
        ingame_image = ImageTk.PhotoImage(sr_resized_image)
        summoners_rift_image = ctk.CTkLabel(app,image=ingame_image,text="")
        summoners_rift_image.grid(row=0,column=3,rowspan=4,columnspan=12,sticky='e',padx=40)
        widgets.append(summoners_rift_image)

def draw_live_label():
    
    live_label = ctk.CTkLabel(app,text="Live Game Information",bg_color=BACKGROUND,font=font)
    live_label.grid(row=4,column=3,columnspan=2,sticky="nw",padx=65,pady=5)
    
    widgets.append(live_label)

def draw_red_point():



    open_red_point = Image.open(f"{PATH}\\icons\\redpoint.png")
    red_point_resized_image = open_red_point.resize((20,20))
    red_image = ImageTk.PhotoImage(red_point_resized_image)
    red_point_image = ctk.CTkLabel(app,image=red_image,text="",bg_color="#242424")
    widgets.append(red_point_image)
    def blink(image):
        image.grid(row=4,column=3,sticky="nw",padx=40)
        app.after(1000,hide,image)
    def hide(image):
        image.grid_forget()
        app.after(1000,blink,image)
            
    blink(red_point_image)


def draw_gamemap():
    global game_info
    if data_recieved == True:
        if game_info[0] == "CLASSIC":
            
            gamemap = ctk.CTkLabel(app,text="Summoner's Rift",bg_color=BACKGROUND,font=font)
        elif game_info[0] == "ARAM":
            gamemap = ctk.CTkLabel(app,text="ARAM",bg_color=BACKGROUND,font=font)
        else: 
            gamemap = ctk.CTkLabel(app,text="Unknown",bg_color=BACKGROUND,font=font)
        gamemap.grid(row=4,column=6,sticky="nw",pady=5)
        widgets.append(gamemap)
def draw_ranked():

    global game_info
    
    if game_info[1] == 4:

        queue_type = ctk.CTkLabel(app,text="Ranked SOLO/DUO",bg_color=BACKGROUND,font=font)
    elif game_info[1] == 7:
        queue_type = ctk.CTkLabel(app,text="Ranked Flex",bg_color=BACKGROUND,font=font)
    elif game_info[1] == 0:
        queue_type = ctk.CTkLabel(app,text="Custom",bg_color=BACKGROUND,font=font)
    else:
        queue_type = ctk.CTkLabel(app,text="Not Ranked",bg_color=BACKGROUND,font=font)
    queue_type.grid(row=4,column=8,columnspan=3,sticky="nw",pady=5)
    widgets.append(queue_type)
def get_canvas_dimentions():
    
    cv_width = round((83.89/100)*WIDTH) -6
    cv_height = round((58.59/100)*HEIGHT)- 6
    return cv_width, cv_height

def draw_both_teams(canvas):

    cv_width, cv_height = get_canvas_dimentions()
    
    blue_color = "#6C8EBF"
    red_color = "#db5e56"
    
    pxSize = int((6.59/100)* WIDTH)
    
    
    widgets.append(canvas)
    draw_blue_team_rectangles(canvas,cv_width,blue_color,pxSize)
    draw_red_team_rectangles(canvas,cv_width,red_color,pxSize)
    draw_blue_icons(canvas,all_data,pxSize,cv_width)
    draw_summoner_names(canvas,cv_width,cv_height,all_data,pxSize)
    draw_levels(canvas,cv_width,cv_height,all_data,pxSize)
    draw_ranks(canvas,cv_width,cv_height,all_data,pxSize)
    draw_winrate(canvas,cv_width,cv_height,all_data,pxSize)
    draw_rank_image(canvas,cv_width,cv_height,all_data,pxSize)
def draw_blue_team():
    
    blue_color = "#6C8EBF"
    def draw_rectangles():
        y_level = 250
        
        rect_height = 90
        
        
        for i in range(1,6):
            end_width = x + (WIDTH - x) / 2  - x
        
        
            canvas = ctk.CTkCanvas(app, width=end_width, height=rect_height,)
            
            canvas.create_rectangle(x, y_level, end_width, y_level + rect_height)
            canvas.configure(bg=blue_color,highlightbackground="black")
            canvas.grid(row=5,column=3,columnspan=6,rowspan=6,sticky="nw",padx=40)
            widgets.append(canvas)
            
            y_level+=90
        
        for item in all_data[0:5]:
                
                
                draw_icons(item[2])
        
        
    def draw_summoner_names():
        x_start = x+90
        y_start = 260
        for item in all_data[0:5]:
                    
                    label = ctk.CTkLabel(app,text=f"{item[8]}",bg_color=blue_color,font=('Montserrat',20,'bold'),text_color="black")
                    label.place(x=x_start+3,y=y_start)
                    widgets.append(label)
                    y_start+= 90

    def draw_summoner_level():
        x_start = x+90
        y_start = 310
        for item in all_data[0:5]:
            
                    label = ctk.CTkLabel(app,text=f"LVL {item[7]}",bg_color=blue_color,font=('Montserrat',20,'bold'),text_color="black")
                    label.place(x=x_start+3,y=y_start)
                    y_start+= 90
                    widgets.append(label)

    def draw_rank():
        center = WIDTH/2 
       # center -= 40
        y=280
        for item in all_data[0:5]:
                    
                    rank = ctk.CTkLabel(app,text=f"{item[4]} {item[5]}",bg_color=blue_color,font=('Montserrat',17,'bold'),text_color="black")
                    rank.place(x=center-30,y=y)
                    widgets.append(rank)
                    draw_devision(item[4],x=center-130,y=y-28,color="#6C8EBF")
                    y+=90

    def draw_winrate():
        center = WIDTH/2 
        # center -= 40
        y=310
        for item in all_data[0:5]:
                    winrate = ctk.CTkLabel(app,text=f"Winrate:{item[6]}%",bg_color=blue_color,font=('Montserrat',17,'bold'),text_color="black")
                    winrate.place(x=center-30,y=y)
                    widgets.append(winrate)
                    
                    y+=90
    def draw_icons(id):
        global Y_level
        icon_name = id_to_name(id)
        image_size = (90,90)
        loaded_champion_image = Image.open(f"{PATH}\\champion_icons\\{icon_name}.png")
        pick_champ_resized = loaded_champion_image.resize(image_size)
        pick_champ_image = ImageTk.PhotoImage(pick_champ_resized)
        pick_champ = ctk.CTkLabel(app,image=pick_champ_image,text="")
        pick_champ.place(x=220,y=Y_level)
        Y_level+=90
        widgets.append(pick_champ)
    draw_rectangles()
    draw_summoner_names()
    draw_summoner_level()
    draw_rank()
    draw_winrate()
def draw_red_team():


    
    def draw_rectangles():
        y_level = 250
        
        rect_height = 90
        
        
        for i in range(1,6):
            end_width = x + (WIDTH - x) / 2  - x
        
        
            canvas = ctk.CTkCanvas(app, width=end_width, height=rect_height)
            
            canvas.create_rectangle(x, y_level, end_width, y_level + rect_height)
            canvas.configure(bg=red_color,highlightbackground="black")
            canvas.grid(row=5,column=8,columnspan=6,rowspan=6,sticky="nw",padx=40)
            widgets.append(canvas)
            
            y_level+=90
        for item in all_data[5:]:
                draw_icons(item[2])
    def draw_summoner_level():
        end_width = x + (WIDTH - x) / 2 
        x_start = end_width+90
        y_start = 310
        for item in all_data[5:]:
            label = ctk.CTkLabel(app,text=f"LVL {item[7]}",bg_color=red_color,text_color="black",font=('Montserrat',20,'bold'))
            label.place(x=x_start+3,y=y_start)
            widgets.append(label)
            y_start+= 90
        
    def draw_summoner_names():
        end_width = x + (WIDTH - x) / 2 
        x_start = end_width+90
        y_start = 260
        for item in all_data[5:]:
                    
                    label = ctk.CTkLabel(app,text=f"{item[8]}",bg_color=red_color,text_color="black",font=('Montserrat',20,'bold'))
                    label.place(x=x_start+3,y=y_start)
                    widgets.append(label)
                    y_start+= 90

    def draw_rank():
        center = WIDTH-100
       # center -= 40
        y=280
        for item in all_data[5:]:
                    rank = ctk.CTkLabel(app,text=f"{item[4]} {item[5]}",bg_color=red_color,font=('Montserrat',17,'bold'),text_color="black")
                    rank.place(x=center-30,y=y)
                    widgets.append(rank)
                    draw_devision(item[4],x=center-130,y=y-28,color="#db5e56")
                    y+=90

    def draw_winrate():
        center = WIDTH-100 
        # center -= 40
        y=310
        for item in all_data[5:]:
                    winrate = ctk.CTkLabel(app,text=f"Winrate:{item[6]}%",bg_color=red_color,font=('Montserrat',17,'bold'),text_color="black")
                    winrate.place(x=center-30,y=y)
                    widgets.append(winrate)
                    y+=90
    def draw_icons(id):
        global Y_level_second
        end_width = x + (WIDTH - x) / 2 
        x_start = end_width+90
        icon_name = id_to_name(id)
        image_size = (90,90)
        loaded_champion_image = Image.open(f"{PATH}\\champion_icons\\{icon_name}.png")
        pick_champ_resized = loaded_champion_image.resize(image_size)
        pick_champ_image = ImageTk.PhotoImage(pick_champ_resized)
        pick_champ = ctk.CTkLabel(app,image=pick_champ_image,text="")
        pick_champ.place(x=x_start-90,y=Y_level_second)
        widgets.append(pick_champ)
        Y_level_second+=90    
    draw_rectangles()
    draw_summoner_names()
    draw_summoner_level()
    draw_rank()
    draw_winrate()
def draw_blue_team_rectangles(canvas,cv_width,color,pxSize):
    x=0
    y=0
    #blue team
    
    for i in range(1,6):
        
        canvas.create_rectangle(x, y, cv_width/2, y + pxSize,fill=color)
        
        y+=pxSize
def draw_red_team_rectangles(canvas,cv_width,color,pxSize):
    
    
    y=0
    #red team
    for i in range(1,6):
        
        canvas.create_rectangle(cv_width/2, y, cv_width, y + pxSize,fill=color)
        
        y+=pxSize

def draw_blue_icons(canvas, all_data, pxSize,cv_width):
    y = 0
   
    for player in all_data:
        icon_name = id_to_name(player[2])
        
        image_size = (pxSize,pxSize)
        image_path = f"{PATH}/champion_icons/{icon_name}.png"  # Ensure correct path separator
        loaded_champion_image = Image.open(image_path)
        pick_champ_resized = loaded_champion_image.resize(image_size)
        pick_champ_image = ImageTk.PhotoImage(pick_champ_resized)
        
        icon_references.append(pick_champ_image)
        if player[1] == 100:
             
            canvas.create_image(pxSize/2, y+(pxSize/2), image=pick_champ_image)  # Adjust y coordinate and anchor
        else:
            canvas.create_image((pxSize/2)+cv_width/2, y, image=pick_champ_image, anchor="s")  # Adjust y coordinate and anchor
        y += pxSize
def draw_summoner_names(canvas,cv_width,cv_height,all_data,pxSize):
    blue_y = (4.5/100)*cv_height
    blue_x = (13.16/100)*cv_width # coords of blue name
    red_x =  cv_width/2 + blue_x
    red_y = (4.5/100)*cv_height # coords of red name
    for player in all_data:
        if player[1] == 100:
            canvas.create_text(blue_x,blue_y, text=f"{player[8]}")
            blue_y+=pxSize
        else:
            canvas.create_text(red_x,red_y, text=f"{player[8]}")
            red_y+=pxSize
def draw_levels(canvas,cv_width,cv_height,all_data,pxSize):
    blue_y = (9.5/100)*cv_height          
    blue_x = (13.16/100)*cv_width
    red_y = (9.5/100)*cv_height
    red_x =  cv_width/2 + blue_x
    for player in all_data:
        if player[1] == 100:
            canvas.create_text(blue_x,blue_y, text=f"LVL:{player[7]}")
            blue_y+=pxSize
        else:
            canvas.create_text(red_x,red_y, text=f"LVL:{player[7]}")
            red_y+=pxSize
def draw_ranks(canvas,cv_width,cv_height,all_data,pxSize):
    blue_y = (9.5/100)*cv_height
    blue_x = (45/100)*cv_width
    red_y = (9.5/100)*cv_height
    red_x = (90/100)*cv_width
    for player in all_data:
        if player[4] != None and player[5] != None:
            print(player[4],player[5])
            if player[1] == 100:
            
                canvas.create_text(blue_x,blue_y, text=f"{player[4]} {player[5]}")
                blue_y+=pxSize 
            else:
                canvas.create_text(red_x,red_y, text=f"{player[4]} {player[5]}")
                red_y+=pxSize
def draw_winrate(canvas,cv_width,cv_height,all_data,pxSize):
    blue_y = (12.5/100)*cv_height
    blue_x = (45/100)*cv_width
    red_y = (12.5/100)*cv_height
    red_x = (90/100)*cv_width           
    for player in all_data:
        if  player[6] != None:
            if player[1] == 100:
                canvas.create_text(blue_x,blue_y, text=f"Winrate:{player[6]}%")
                blue_y+=pxSize
            else:
                canvas.create_text(red_x,red_y, text=f"Winrate:{player[6]}%")
                red_y+=pxSize

def draw_rank_image(canvas,cv_width,cv_height,all_data,pxSize):
    blue_y = (9/100)*cv_height
    blue_x = (41.5/100)*cv_width
    red_y = (9/100)*cv_height
    red_x = (83/100)*cv_width 
    for player in all_data:
        if player[4] != None and player[5] != None:
            if player[1] == 100:
                image_size = (pxSize,pxSize)
                loaded_item_image = Image.open(f"{PATH}\\ranks\\{player[4]}.png")
                item_resized = loaded_item_image.resize(image_size)
                item_image = ImageTk.PhotoImage(item_resized)
                icon_references.append(item_image)
                canvas.create_image(blue_x,blue_y, image=item_image)
                blue_y+=pxSize
            else:
                image_size = (pxSize,pxSize)
                loaded_item_image = Image.open(f"{PATH}\\ranks\\{player[4]}.png")
                item_resized = loaded_item_image.resize(image_size)
                item_image = ImageTk.PhotoImage(item_resized)
                icon_references.append(item_image)
                canvas.create_image(red_x,red_y, image=item_image)
                red_y+=pxSize
            
             





##############################################
#             IN CHAMPION SELECT             #
##############################################
def is_in_session(port,api):
    url = f"https://127.0.0.1:{port}/lol-champ-select/v1/session"
    request = requests.get(url,auth=('riot',api),verify=False)
    if request.status_code == 200:
        return True
    else:
        return False
def get_visible_puuids(port,api):
    url = f"https://127.0.0.1:{port}/lol-champ-select/v1/session"
    #request = requests.get(url,auth=('riot',api),verify=False)
    #data = request.json()
    with open("session.json","r") as f:
        data = json.load(f)
    print(data)
    teamId =0
    
    puuids = []
    for part in data["myTeam"]:
        if part["nameVisibilityType"] == "UNHIDDEN" or part["nameVisibilityType"] == "VISIBLE":
            puuids.append(part["puuid"])
            teamId = part["team"]
    return puuids,teamId



# def get_names_from_puuids(puuids):
#     names = []
#     for puuid in puuids:
#         name,tag = getNameAndTag(puuid,port,api)
#         names.append((name,tag))
#     return names
    
    

# def get_Real_Puuid(name,tag):
#     url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key=RGAPI-6e925dd7-2bdc-4a78-ba23-35b3a895a417"
#     request = requests.get(url=url)
#     response = request.json()
#     return response["puuid"]
# def store_real_puuids(names_and_tags):
#     real_puuids = []
#     for name_and_tag in names_and_tags:
#         real_puuids.append(get_Real_Puuid(name_and_tag[0],name_and_tag[1]))
#     return real_puuids
# puuids = get_visible_puuids(port,api) # fetched puuids from champ select
# names_and_tags = get_names_from_puuids(puuids) #stored in a list of tuples
# real_puuids = store_real_puuids(names_and_tags) # stores real puuids in a list



def draw_champ_select(canvas):
    blue_color = "#6C8EBF"
    red_color = "#db5e56"
    global icon_references
    cv_width, cv_height = get_canvas_dimentions()
    puuids, teamId = get_visible_puuids(port,api)
    
    most_played_champions = test_algo.start_func(puuids)# champ,wr,games
    pxSize = int((6.59/100)* WIDTH)
    draw_blue_team_rectangles(canvas,cv_width,blue_color,pxSize)
    draw_red_team_rectangles(canvas,cv_width,red_color,pxSize)
    
    blue_x = pxSize/2
    blue_y = pxSize/2
    red_x = (pxSize/2)+cv_width
    red_y = pxSize/2
    # FAV CHAMP ICONS
    image_size = (pxSize,pxSize)
    
    for item in most_played_champions:
        if teamId == 1:
            image_ = Image.open(f"{PATH}\\champion_icons\\{item[0]}.png").resize(image_size)
            image = ImageTk.PhotoImage(image_)
            icon_references.append(image)
            canvas.create_image(blue_x,blue_y, image=image)
            blue_y+=pxSize
        else:
            image_ = Image.open(f"{PATH}\\champion_icons\\{item[0]}.png").resize(image_size)
            image = ImageTk.PhotoImage(image_)
            icon_references.append(image)
            canvas.create_image(red_x,red_y, image=image)
            red_y+=pxSize
        
        
    
        
            
    def draw_winrate_and_games():
        wr_blue_y = (9.5/100)*cv_height
        wr_blue_x = (45/100)*cv_width
        wr_red_y = (9.5/100)*cv_height
        wr_red_x = (90/100)*cv_width
        games_blue_y = (12.5/100)*cv_height
        games_blue_x = (45/100)*cv_width
        games_red_y = (12.5/100)*cv_height
        games_red_x = (90/100)*cv_width
        for item in most_played_champions:
            if teamId == 1:
                canvas.create_text(wr_blue_x,wr_blue_y, text=f"Winrate: {item[1]}%")
                canvas.create_text(games_blue_x,games_blue_y, text=f"Games: {item[2]}")
                wr_blue_y+=pxSize
                games_blue_y+=pxSize
            else:
                canvas.create_text(wr_red_x,wr_red_y, text=f"Winrate: {item[1]}%")
                canvas.create_text(games_red_x,games_red_y, text=f"Games: {item[2]}")
                wr_red_y+=pxSize
                games_red_y+=pxSize
    def draw_summoner_names():
        blue_y = (4.5/100)*cv_height
        blue_x = (13.16/100)*cv_width # coords of blue name
        red_x =  cv_width/2 + blue_x
        red_y = (4.5/100)*cv_height # coords of red name
        for item in most_played_champions:     
            if teamId == 1:
                canvas.create_text(blue_x,blue_y, text=f"{item[3]}#{item[4]}",anchor="w")
                blue_y+=pxSize
            else:
                canvas.create_text(red_x,red_y, text=f"{item[3]}#{item[4]}")
                red_y+=pxSize
    
    draw_winrate_and_games()
    draw_summoner_names()














def get_widgets():
    global already_clicked
    already_clicked=False
    return widgets

def refresh():
    global port,api
    game_name , game_tag = getProfileData(port,api)
    
    my_puuid  = backend.InGame.getPUUID(game_name,game_tag,"RGAPI-6e925dd7-2bdc-4a78-ba23-35b3a895a417")
    
    all_data,data_recieved,game_info = backend.InGame.getCurrentMatchData(my_puuid,"RGAPI-6e925dd7-2bdc-4a78-ba23-35b3a895a417")
    
    return all_data,data_recieved,game_info
    
def getProfileData(port,api):
    if port != 0 and api!=0:
        url = f"https://127.0.0.1:{port}/lol-summoner/v1/current-summoner"
        request = requests.get(url,auth=('riot',api),verify=False)
        response = request.json()
        username = response["gameName"]
        tagline = response["tagLine"]
        return username,tagline
def id_to_name(id):
    global dictionary
    for key,value in dictionary.items():
        if int(value) == id:
            return key
def draw_devision(devision,x,y,color):
    global app
    if devision != None:
         
        image_size = (85,85)
        loaded_item_image = Image.open(f"{PATH}\\ranks\\{devision}.png")
        item_resized = loaded_item_image.resize(image_size)
        item_image = ImageTk.PhotoImage(item_resized)
        rank_emblem = ctk.CTkLabel(app,image=item_image,text="",bg_color=color,fg_color=color)
        rank_emblem.place(x=x,y=y)
    
    


