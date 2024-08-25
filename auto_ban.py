import customtkinter as ctk
import numpy as np
from PIL import Image ,ImageTk, ImageDraw
import backend,json,os,game_dir
from CTkScrollableDropdown import *
import saveload
PATH = os.getcwd()
BACKGROUND = "#242424" #BACKGROUND COLOR 
app = None # Main CTK
x =220 # start of the UI
WIDTH = 0
0 #screen width
HEIGHT = 0 # screen height
font = ('Montserrat',30,'bold') # FONT USED 
widgets =[] # labels,buttons and etc are placed here to destroy
already_clicked = False
center = 0
values = None
keys= None
loaded_ban_champion_from_config ="None"
dictionary = {}
name_of_champion = ""
profile_info = backend.Profile()
import game_dir
def get_config_dir():
    path = f"{PATH}\\saved_config\\game_dir.json"
    
    if os.path.exists(path):
        with open(path) as p:
            config = json.load(p)
            return config["game_dir"]


game_dir.game_dir = get_config_dir()
game_dir.game_dir += "/lockfile"
port,api = profile_info.getAPI(game_dir.game_dir)

ban = backend.AutoBan()
def draw_auto_ban(appp):
    global app,WIDTH,HEIGHT,font,widgets,center,values,keys,name_of_champion,dictionary
    dictionary = backend.getChampionsWithID()
    values = list(dictionary.keys())
    keys = list(dictionary.values())
    for i in values:
        backend.getIcon(i)
    app = appp
    WIDTH = app.winfo_screenwidth()
    HEIGHT = app.winfo_screenheight()
    center = (WIDTH-x)/2
    widgets.clear()
    draw_label()
    draw_champion_icon(loaded_ban_champion_from_config)
    draw_combobox()
    draw_toggle()


def name_to_id(name):
    global dictionary
    return int(dictionary[f"{name}"])


def set_name_of_champion(name):

    global name_of_champion
    name_of_champion = name

def do():
    if status == True:
        try:
            pickable_champs = ban.getBannableChamps(port,api)
            cellId=ban.getActorCellId(port,api)
            id = name_to_id(name_of_champion)
            ban.ban_event(id,cellId,pickable_champs,port,api)
            app.after(4000,do)
        except (KeyError) as e:
            pass
def draw_label():
    global center
    
    draw_label = ctk.CTkLabel(app,text="Auto Ban Champion",bg_color=BACKGROUND,font=font,anchor="center")
    draw_label.place(relx=0.5,rely=0.2)
    widgets.append(draw_label)
def draw_champion_icon(icon):
    global center
    image_size = (110,110)
    loaded_champion_image = Image.open(f"{PATH}\\champion_icons\\{icon}.png")
    ban_champ_resized = loaded_champion_image.resize(image_size)
    ban_champ_image = ImageTk.PhotoImage(ban_champ_resized)
    ban_champ = ctk.CTkLabel(app,image=ban_champ_image,text="")
    ban_champ.place(relx=0.45,rely=0.25)
    widgets.append(ban_champ)
    ban_champion_picked(icon)
def draw_combobox():
    global values
    combo_box = ctk.CTkComboBox(app,width=200,height=40)
    wait_label = ctk.CTkLabel(app,text="Please wait...",bg_color=BACKGROUND,font=font,anchor="center")
    wait_label.place(relx=0.5,rely=0.5)
    def do_my_job(combobox ,k):
        global loaded_ban_champion_from_config
        if loaded_ban_champion_from_config == "None":
            draw_champion_icon(k)
            combobox.set(k)
            set_name_of_champion(k)
        else:
            draw_champion_icon(loaded_ban_champion_from_config)
            combobox.set(loaded_ban_champion_from_config)
            set_name_of_champion(loaded_ban_champion_from_config)
    CTkScrollableDropdown(combo_box,values=values,command=lambda k: do_my_job(combo_box,k),autocomplete=True,button_height=30)
    combo_box.place(relx=0.55,rely=0.25)
    do_my_job(combo_box,loaded_ban_champion_from_config)
    widgets.append(combo_box)
    wait_label.destroy()
status=False
def draw_toggle():
    
    def switch():
        global status
        if status:
            status=False
            status_label.configure(text="status: off",text_color="red")
        else:
            status_label.configure(text="status: on",text_color="green")
            status=True
            app.after(4000,do)
    def loaded_switch():
        global status
        if status:
            status_label.configure(text="status: on",text_color="green")
        else:
            status_label.configure(text="status: off",text_color="red")
            
            
            
    toggle_button = ctk.CTkButton(app,width=200,height=50,fg_color="#99ff33",text_color="black",text="ON/OFF",font=font,hover_color="white",command=switch)
    toggle_button.place(relx=0.55,rely=0.3)
    widgets.append(toggle_button)
    status_label = ctk.CTkLabel(app,text="status: off",text_color="red",bg_color=BACKGROUND,font=("Monsserat",16))
    status_label.place(relx=0.46,rely=0.37)
    loaded_switch()
    widgets.append(status_label)
    
        


def get_widgets():
    
    return widgets

def ban_champion_picked(champ):
    saveload.ban_champion = champ




