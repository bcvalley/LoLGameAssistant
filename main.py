import customtkinter as ctk

from PIL import Image ,ImageTk, ImageDraw
import ingame,backend,match_history
import auto_pick,requests,os
import auto_ban,auto_spells,auto_accept,saveload
import game_dir
WIDTH = 0
HEIGHT = 0
game_dir.game_dir = saveload.get_config_dir()
game_dir.game_dir += "/lockfile"
statuses = [None,None,None,None,None]
profile_info = backend.Profile()
port,api = profile_info.getAPI(game_dir.game_dir)
widgets = None
path = os.getcwd()

#print(backend.InGame.getPUUID("easywins","EUNE","RGAPI-6e925dd7-2bdc-4a78-ba23-35b3a895a417"))
def load_widgets():
    global widgets
    widgets = (
        auto_accept.get_widgets() +
        ingame.get_widgets() +
        auto_pick.get_widgets() +
        auto_ban.get_widgets() +
        auto_spells.get_widgets() +
        match_history.get_widgets() +
        saveload.get_widgets()
    )
    # was 2 in the original code
                    ##|
    if len(widgets) > 0:
        
        
        
        
        print(len(widgets))
        for x in widgets:
            print(f"Last widget: {x}")
            if isinstance(x, (ctk.CTkRadioButton, ctk.CTkComboBox)):
                x.grid_remove()
            else:
                x.destroy()
        
        
        widgets.clear()
        print(f"Widgets list after clearing: {widgets}")

# Example usage of the function
load_widgets()

def menu(app,s_height):
    global username,level,tagline,iconId,tier,rank,lp,winrate,port,api,path
    button_height = 80
    menu_width =220
    BACKGROUND = "dimgray"
    image_w_size = 70
    image_h_size = 70
    starting_position = 200
    frame1 = ctk.CTkFrame(app,width=menu_width,height=2000,fg_color=BACKGROUND)
    frame1.place(x=0,y=0)
    for gird in range(20):
        app.grid_columnconfigure(gird, weight=0,minsize=50)
        app.grid_rowconfigure(gird, weight=0,minsize=50)
   
    load_battle_image = Image.open(os.path.join(path,"icons\\battle.png"))
    battle_resized_image = load_battle_image.resize((image_w_size,image_h_size))
    battle_image = ImageTk.PhotoImage(battle_resized_image)
    def battle_button_clicked():
        load_widgets()
        match_history.draw_match_history(app,"easywins","EUNE")
    battle_button = ctk.CTkButton(app,image=battle_image,text="",
                                       fg_color=BACKGROUND,
                                       bg_color=BACKGROUND,
                                       height=button_height,
                                       width=menu_width,
                                       hover_color="white",
                                       command=battle_button_clicked,
                                       corner_radius=0
                                       )
    battle_button.grid(row=4,column=0,columnspan=4,sticky="w")

    load_ingame_image = Image.open(os.path.join(path,"icons\\ingame.png"))
    ingame_resized_image = load_ingame_image.resize((image_w_size,image_h_size))
    ingame_image = ImageTk.PhotoImage(ingame_resized_image)
    def ing_button_clicked():
        load_widgets()
        ingame.live_game_draw(app)
    ingame_button = ctk.CTkButton(app,image=ingame_image,text="",
                                       fg_color=BACKGROUND,
                                       bg_color=BACKGROUND,
                                       height=button_height,
                                       width=menu_width,
                                       hover_color="white",
                                        command=ing_button_clicked,
                                       corner_radius=0
                                       )
    
    
    ingame_button.grid(row=5,column=0,columnspan=4,sticky="w")

    loaded_lockin_image = Image.open(os.path.join(path,"icons\\autolock.png"))
    lockin_resized_image = loaded_lockin_image.resize((image_w_size,image_h_size))
    lockin_image = ImageTk.PhotoImage(lockin_resized_image)
    def lock_button_clicked():
         
        load_widgets()
        auto_pick.draw_auto_pick(app)
        
        
    lockin_button = ctk.CTkButton(app,image=lockin_image,text="",
                                       fg_color=BACKGROUND,
                                       bg_color=BACKGROUND,
                                       height=button_height,
                                       width=menu_width,
                                       hover_color="white",
                                       command=lock_button_clicked,
                                       corner_radius=0
                                       )
    lockin_button.grid(row=6,column=0,columnspan=4,sticky="w")
    
    loaded_ban_image = Image.open(os.path.join(path,"icons\\ban.png"))
    ban_resized_image = loaded_ban_image.resize((image_w_size,image_h_size))
    ban_image = ImageTk.PhotoImage(ban_resized_image)
    def ban_button_clicked():
        load_widgets()
        auto_ban.draw_auto_ban(app)
    ban_button = ctk.CTkButton(app,image=ban_image,text="",
                                       fg_color=BACKGROUND,
                                       bg_color=BACKGROUND,
                                       height=button_height,
                                       width=menu_width,
                                       hover_color="white",
                                       command=ban_button_clicked,
                                       corner_radius=0
                                       )
    ban_button.grid(row=7,column=0,columnspan=4,sticky="w")


    loaded_spell_image = Image.open(os.path.join(path,"icons\\spell.png"))
    spell_resized_image = loaded_spell_image.resize((image_w_size,image_h_size))
    spell_image = ImageTk.PhotoImage(spell_resized_image)
    def spell_button_clicked():
        load_widgets()
        auto_spells.draw_spells(app)
    spell_button = ctk.CTkButton(app,image=spell_image,text="",
                                       fg_color=BACKGROUND,
                                       bg_color=BACKGROUND,
                                       height=button_height,
                                       width=menu_width,
                                       hover_color="white",
                                       command=spell_button_clicked,
                                       corner_radius=0
                                       )
    spell_button.grid(row=8,column=0,columnspan=4,sticky="w")

    loaded_accept_image = Image.open(os.path.join(path,"icons\\accept.png"))
    accpet_resized_image = loaded_accept_image.resize((image_w_size,image_h_size))
    accpet_image = ImageTk.PhotoImage(accpet_resized_image)
    def accept_button_clicked():
        global statuses
        load_widgets()
        auto_accept.draw_accpet(app)
        
    accept_button = ctk.CTkButton(app,image=accpet_image,text="",
                                       fg_color=BACKGROUND,
                                       bg_color=BACKGROUND,
                                       height=button_height,
                                       width=menu_width,
                                       hover_color="white",
                                       command=accept_button_clicked,
                                       corner_radius=0
                                       )
    accept_button.grid(row=9,column=0,columnspan=4,sticky="w")
    #profile icon downloadProfileIcon(iconId)
    img = Image.open(downloadProfileIcon(iconId)).convert("RGBA")
    img=img.resize((80,80))
    background = Image.new("RGBA", img.size, (0,0,0,0))
    mask = Image.new("RGBA", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0,80,80), fill='white', outline=None)
    new_img = Image.composite(img, background, mask)
    new_img.save("cropped.png")
    tk_image = ImageTk.PhotoImage(new_img)
    def profile_clicked():
        global statuses
        load_widgets()
        saveload.draw_save(app,statuses)
    profile_button = ctk.CTkButton(app,image=tk_image,text="",bg_color=BACKGROUND,width=80,height=80,fg_color=BACKGROUND,hover_color="white",command=profile_clicked)
    profile_button.grid(row=0,column=0,rowspan=2,columnspan=2,padx=10)
    #Player Name {username}#{tagline}
    username_label = ctk.CTkLabel(app,text=f" {username}#{tagline}",bg_color=BACKGROUND,font=('Montserrat',20,'bold'))
    username_label.grid(row=2,column=0,columnspan=3,padx=10,sticky="s")
    #search box 
    def click(*args): 
        search_box.delete(0, 'end') 
    search_box = ctk.CTkEntry(app,width=menu_width-40,height=30)
    search_box.insert(0, 'example#EUNE') 
    search_box.bind("<Button-1>", click) 
    search_box.grid(row=3,column=0,columnspan=3,sticky="n")
    #search button
    loaded_lense_image = Image.open(os.path.join(path,"icons\\lense.png"))
    lense_resized_image = loaded_lense_image.resize((20,20))
    lense_image = ImageTk.PhotoImage(lense_resized_image)
    def search_player():
        temp = search_box.get().split("#")
        load_widgets()
        match_history.draw_match_history(app,temp[0],temp[1])

    lense_button = ctk.CTkButton(app,image=lense_image,text="",
                                       fg_color=BACKGROUND,   
                                       bg_color=BACKGROUND,
                                       height=30,
                                       width=30,
                                       hover_color="white",
                                       command=search_player,
                                       corner_radius=0
                                       )
    lense_button.grid(row=3,column=3,sticky="nw")
    #player level {level}
    
    player_level = ctk.CTkLabel(app,text=f"{level}",font=('Montserrat',20,'bold'),fg_color="purple")
    player_level.grid(row=1,column=0,columnspan=2,sticky="s")
    player_level.tkraise()
    #Rank Label {tier} {rank}    
    rank_label = ctk.CTkLabel(app,text=f" {tier} {rank}",font=('Montserrat',15,'bold'),text_color="black",bg_color="yellow")
    rank_label.grid(row=0,column=2)
    #LP label LP : {lp}      
    lp_label = ctk.CTkLabel(app,text=f" LP : {lp} ",font=('Montserrat',15,'bold'),text_color="black",bg_color="yellow")
    lp_label.grid(row=1,column=2,sticky="n")
    #Winrate label  WR:{winrate}%    
    winrate_label = ctk.CTkLabel(app,text=f"WR:{winrate}%",font=('Montserrat',15,'bold'))
    
    if winrate >50:
        winrate_label.configure(fg_color="green",bg_color="green")
    else:
        winrate_label.configure(fg_color="red",bg_color= "red")
    winrate_label.grid(row=1,column=2,sticky="s")

def getProfileData(port,api):
    if port != 0 and api!=0:
        url = f"https://127.0.0.1:{port}/lol-summoner/v1/current-summoner"
        request = requests.get(url,auth=('riot',api),verify=False)
        response = request.json()
        username = response["gameName"]
        tagline = response["tagLine"]
        iconId = response["profileIconId"]
        level = response["summonerLevel"]
        return username,tagline,iconId,level

def playerRankAndWinrate(username,tagline,api):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username}/{tagline}?api_key={api}"
    request = requests.get(url=url)
    response = request.json()
    puuid = response["puuid"]
    url2 = f"https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api}"
    request = requests.get(url=url2)
    response = request.json()
    summoner_id = response["id"]
    url3 = f"https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api}"
    request = requests.get(url=url3)
    response = request.json()
   
    tier = response[1]["tier"]
    rank = response[1]["rank"]
    lp = response[1]["leaguePoints"]
    winrate =  int(response[1]["wins"] / (response[1]["wins"] + response[1]["losses"]) * 100)
    return tier,rank,lp,winrate

username,tagline,iconId,level = getProfileData(port,api)   
tier,rank,lp,winrate = playerRankAndWinrate(username,tagline,"RGAPI-6e925dd7-2bdc-4a78-ba23-35b3a895a417")

def downloadProfileIcon(id:int):
    new_path = f"{path}\\profile_icons\\{id}.png"
    if os.path.exists(new_path):
        
        return new_path
    else:
        url = f"https://ddragon.leagueoflegends.com/cdn/14.13.1/img/profileicon/{id}.png"
        img_data = requests.get(url)
        with open(new_path,"wb") as handler:
            handler.write(img_data.content)
    getProfileIconPath(id)
def getProfileIconPath(id):
    return f"profile_icons/{id}.png"

def mainUI():
    global WIDTH,HEIGHT
    ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    app = ctk.CTk()  # create CTk window like you do with the Tk window
    
    WIDTH = app.winfo_screenwidth()
    
    
    HEIGHT = app.winfo_screenheight()
       
    app.geometry(f"{WIDTH}x{HEIGHT}-7-0")
    app.attributes("-alpha",1)
    menu(app,HEIGHT)
    
    app.mainloop()
def get_width():
    return WIDTH
def get_height():
    return HEIGHT
mainUI()