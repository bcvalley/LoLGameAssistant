import customtkinter as ctk
import numpy as np
from PIL import Image ,ImageTk, ImageDraw
import backend,requests,threading,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
BACKGROUND = "#242424" #BACKGROUND COLOR 
app = None # Main CTK
x =220 # start of the UI
WIDTH = 0 #screen width
HEIGHT = 0 # screen height
font = ('Montserrat',17,'bold') # FONT USED 
widgets =[] # labels,buttons and etc are placed here to destroy
already_clicked = False
all_data = None
prof = backend.Profile()
port,api = prof.getAPI("C:/Riot Games/League of Legends/lockfile")
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
    center = WIDTH/2 
    req_label = ctk.CTkLabel(app,text="You are not in match yet",text_color="red",font=('Montserrat',40,'bold'),anchor="center")
    all_data,data_recieved,game_info = refresh()
    print(f"start {all_data}")
    print(f"end------------------------------------")
    # all_data = [['1EvmemmZahbgXJJHtColbp6NQyvNdsKqUdSQGsfXT9J9KOzWI0_K3Pe5pXJzWLGilPLybUrOE38wkw', 100, 9, 3784, 'PLATINUM', 'II', 52, 831, 'Lord Shifu#UwU'],
    #     ['TDPhJGKwKamfHbC_JyMj09O9BrY6_DdxNxQ2DCGRPAVKrIDsy2ckJnRXUbGghv7xUl_brHMc_V7vUg', 100, 22, 5055, None, None, None, 423, 'be afraiid#EUNE'],
    #     ['SGlGGo4sOb6s_ut7AP_e6Dbuhvw3mFL-2ZX2FCBCF34URdNkjCb4bcp6oAgMpymtw7aDVkN-GGOnuQ', 100, 21, 6570, None, None, None, 106, 'remonderean#EUNE'],
    #     ['sBQFdHid_7SBuoGRDtnihjiNW_Pn3WtATsJalwqgmKQd17qLYHC_Z-JDzXVIrMYbpJgChK0BuTjEew', 100, 555, 4404, 'SILVER', 'II', 80, 250, 'LantiBoy#EUNE'],
    #     ['66tG3Ce5hqdDXSrgtc5vDzEw4tses4_MP968c2FW9Fb2BJ5uHVoWRAOZwf-gJIrjQTTFYVWySO2Oqg', 100, 131, 1645, 'GOLD', 'IV', 45, 433, 'easywins#EUNE'],
    #     ['NK59SkJ7gJVuR11w-YpMoJWOgbPs71GTmOWGdZfJukY1dVh3-Q0hiG2oNxI_Pn4cyGe_6dnVunPfUg', 200, 202, 582, None, None, None, 232, 'Black Pencil#EUNE'], 
    #     ['8p_bLOcn00e6nR5kwTizqi8OJ3XeEA4d9MjYMullamoBT0IXOy4xHaBw7IxtjBt4GkQM3o-SNhbUEQ', 200, 888, 5765, None, None, None, 278, 'Dezhavyu#EUNE'],
    #     ['9AGt-EfrNi3HzlNi9i_Ogn2JfX21T5iL6Wy86f7-nzf9x7tTM_k0ZMVmMPYsVgd4uV4a-RzHwkCG_A', 200, 14, 6632, 'PLATINUM', 'IV', 57, 563, 'H GeushTouMenous#txc'],
    #     ['S1w2-djr4iCn7l7K_lMQ0HeUAG-gC_h68pe61e4P5_AXPBjekryDmsf2fH1rPQ3U3b5l6ayrs1BVVQ', 200, 24, 4568, 'SILVER', 'II', 52, 336, 'dyfcio3#EUNE'],
    #     ['49pmi83W8SILkcFyVnXPpljglQpf-sQ__JasyAqGvw9NTuSmeM1crCz4Hu9USLOf93m3SiPmSK1Bog', 200, 711, 5859, 'SILVER', 'II', 50, 489, 'waynx#EUNE']]
    
    if data_recieved == False:
        print("data not recieved")
        req_label.place(x=center-100,y=HEIGHT/2-100)
        app.after(1000, live_game_draw, app)
    else:   
        try:
            req_label.place_forget()
        except:AttributeError
    
    draw_map()
    draw_live_label()
    draw_gamemap()
    draw_ranked()
    draw_red_point()
    draw_blue_team()
    draw_red_team()
    
    # already_clicked=False ## IMPORTANT

    
def draw_map():
    global app
    map="SR"
    if map == "SR":
        open_summoners_rift_image = Image.open("C:/Users/ivetoooooooooooo/OneDrive - Министерство на образованието и науката/Desktop/FF15/icons/summoners_rift.jpg")
        sr_resized_image = open_summoners_rift_image.resize((1146,200))
        ingame_image = ImageTk.PhotoImage(sr_resized_image)
        summoners_rift_image = ctk.CTkLabel(app,image=ingame_image,text="")
        summoners_rift_image.place(x=220,y=0)
        widgets.append(summoners_rift_image)
    elif map == "ARAM":
        open_summoners_rift_image = Image.open("C:/Users/ivetoooooooooooo/OneDrive - Министерство на образованието и науката/Desktop/FF15/icons/aram.jpg")
        sr_resized_image = open_summoners_rift_image.resize((1146,200))
        ingame_image = ImageTk.PhotoImage(sr_resized_image)
        summoners_rift_image = ctk.CTkLabel(app,image=ingame_image,text="")
        summoners_rift_image.place(x=220,y=0)
        widgets.append(summoners_rift_image)

def draw_live_label():
    
    live_label = ctk.CTkLabel(app,text="Live Game Information",bg_color=BACKGROUND,font=font)
    live_label.place(x=x+20,y=210)
    widgets.append(live_label)

def draw_red_point():



    open_red_point = Image.open("C:/Users/ivetoooooooooooo/OneDrive - Министерство на образованието и науката/Desktop/FF15/icons/redpoint.png")
    red_point_resized_image = open_red_point.resize((20,20))
    red_image = ImageTk.PhotoImage(red_point_resized_image)
    red_point_image = ctk.CTkLabel(app,image=red_image,text="",bg_color="#242424")
    widgets.append(red_point_image)
    def blink(image):
        image.place(x=x,y=210)
        app.after(1000,hide,image)
    def hide(image):
        image.place_forget()
        app.after(1000,blink,image)
            
    blink(red_point_image)

def draw_gamemap():
    global game_info
    if game_info[0] == "CLASSIC":
        
        gamemap = ctk.CTkLabel(app,text="Summoner's Rift",bg_color=BACKGROUND,font=font)
    elif game_info[0] == "ARAM":
        gamemap = ctk.CTkLabel(app,text="ARAM",bg_color=BACKGROUND,font=font)
    else: 
        gamemap = ctk.CTkLabel(app,text="Unknown",bg_color=BACKGROUND,font=font)
    gamemap.pack(padx=x+30,pady=210)
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
        queue_type = ctk.CTkLabel(app,text="Unknown",bg_color=BACKGROUND,font=font)
    queue_type.place(x=x + 800,y=210)
    widgets.append(queue_type)

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
            canvas.place(x=x,y=y_level)
            widgets.append(canvas)
            
            y_level+=90
        for item in all_data[0:5]:
                
                print(f"Blue team {item[0]}")
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
        loaded_champion_image = Image.open(f"C:/Users/ivetoooooooooooo/OneDrive - Министерство на образованието и науката/Desktop/FF15/champion_icons/{icon_name}.png")
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


    red_color = "#db5e56"
    def draw_rectangles():
        y_level = 250
        
        rect_height = 90
        
        
        for i in range(1,6):
            end_width = x + (WIDTH - x) / 2  - x
        
        
            canvas = ctk.CTkCanvas(app, width=end_width, height=rect_height)
            
            canvas.create_rectangle(x, y_level, end_width, y_level + rect_height)
            canvas.configure(bg=red_color,highlightbackground="black")
            canvas.place(x=x+end_width,y=y_level)
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
        loaded_champion_image = Image.open(f"C:/Users/ivetoooooooooooo/OneDrive - Министерство на образованието и науката/Desktop/FF15/champion_icons/{icon_name}.png")
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
        loaded_item_image = Image.open(f"C:/Users/ivetoooooooooooo/OneDrive - Министерство на образованието и науката/Desktop/FF15/ranks/{devision}.png")
        item_resized = loaded_item_image.resize(image_size)
        item_image = ImageTk.PhotoImage(item_resized)
        rank_emblem = ctk.CTkLabel(app,image=item_image,text="",bg_color=color,fg_color=color)
        rank_emblem.place(x=x,y=y)
    
    


