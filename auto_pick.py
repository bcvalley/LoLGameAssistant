import customtkinter as ctk
import numpy as np
from PIL import Image ,ImageTk, ImageDraw
import backend,json,os
from CTkScrollableDropdown import *
import saveload
PATH = os.getcwd()
BACKGROUND = "#242424" #BACKGROUND COLOR 
app = None # Main CTK
x =220 # start of the UI
WIDTH = 0
0 #screen width
HEIGHT = 0 # screen height
def get_config_dir():
    path = f"{PATH}\\saved_config\\game_dir.json"
    
    if os.path.exists(path):
        with open(path) as p:
            config = json.load(p)
            return config["game_dir"]


font = ('Montserrat',30,'bold') # FONT USED 
widgets =[] # labels,buttons and etc are placed here to destroy
already_clicked = False
center = 0
values = None
keys= None
loaded_champion_from_config = "None"
dictionary = {}
champ_picked = ""
name_of_champion = ""
def draw_auto_pick(appp):
    global app,WIDTH,HEIGHT,font,widgets,center,x,values,keys,dictionary
    dictionary = backend.getChampionsWithID()
   
    values = list(dictionary.keys())
    keys = list(dictionary.values())
    for i in values:
        backend.getIcon(i)
    widgets.clear()
    app = appp
    WIDTH = app.winfo_screenwidth()
    HEIGHT = app.winfo_screenheight()
    center = (WIDTH-x)/2
    draw_label()
    draw_champion_icon(loaded_champion_from_config)
    draw_combobox()
    
    draw_toggle()

def draw_label():
    global center
    
    draw_label = ctk.CTkLabel(app,text="Auto Pick Champion",bg_color=BACKGROUND,font=font,anchor="center")
    draw_label.place(relx=0.5,rely=0.2)

    widgets.append(draw_label)
def draw_champion_icon(icon):
    global center,champ_picked
    champ_picked = icon
    image_size = (110,110)
    loaded_champion_image = Image.open(f"{PATH}\\champion_icons\\{icon}.png")
    pick_champ_resized = loaded_champion_image.resize(image_size)
    pick_champ_image = ImageTk.PhotoImage(pick_champ_resized)
    pick_champ = ctk.CTkLabel(app,image=pick_champ_image,text="")
    pick_champ.place(relx=0.45,rely=0.25)

    widgets.append(pick_champ)
    champions_picked(champ_picked)
def draw_combobox():
    global values
    combo_box = ctk.CTkComboBox(app,width=200,height=40)
    wait_label = ctk.CTkLabel(app,text="Please wait...",bg_color=BACKGROUND,font=font,anchor="center")
    wait_label.place(relx=0.5,rely=0.5)
    def do_my_job(combobox ,k):
        global loaded_champion_from_config
        if loaded_champion_from_config == "None":
            draw_champion_icon(k)
            combobox.set(k)
            set_name_of_champion(k)
        else:
            draw_champion_icon(loaded_champion_from_config)
            combobox.set(loaded_champion_from_config)
            set_name_of_champion(loaded_champion_from_config)
    CTkScrollableDropdown(combo_box,values=values,command=lambda k: do_my_job(combo_box,k),autocomplete=True,button_height=30)
    combo_box.place(relx=0.55,rely=0.25)
    do_my_job(combo_box,loaded_champion_from_config)
    widgets.append(combo_box)
    wait_label.destroy()


status=False
profile_info = backend.Profile()
import game_dir
game_dir.game_dir = get_config_dir()
game_dir.game_dir += "/lockfile"
port,api = profile_info.getAPI(game_dir.game_dir)
pick = backend.AutoPick()

def name_to_id(name):
    global dictionary
    return int(dictionary[f"{name}"])
def set_name_of_champion(name):

    global name_of_champion
    name_of_champion = name

def do():
    if status == True:
        try:
            pickable_champs = pick.getPickableChamps(port,api)
            cellId=pick.getActorCellId(port,api)
            id = name_to_id(name_of_champion)
            pick.pick_event(id,cellId,pickable_champs,port,api)
            app.after(4000,do)
        except KeyError as e:
            app.after(4000,do)
            
def draw_toggle():
    
    def switch():
        global status , name_of_champion ,app
        if status:
            status=False
            status_label.configure(text="status: off",text_color="red")
            
        else:
            status_label.configure(text="status: on",text_color="green")
            status=True
            app.after(4000,do)
            
               

    
            
    toggle_button = ctk.CTkButton(app,width=200,height=50,fg_color="#99ff33",text_color="black",text="ON/OFF",font=font,hover_color="white",command=switch)
    toggle_button.place(relx=0.55,rely=0.3)
    widgets.append(toggle_button)
    status_label = ctk.CTkLabel(app,text="status: off",text_color="red",bg_color=BACKGROUND,font=("Monsserat",16))
    #status_label.grid(row=7,column=11,columnspan=2,sticky="n")
    status_label.place(relx=0.46,rely=0.37)
    widgets.append(status_label)
        

def get_widgets():
    
    return widgets

def champions_picked(champ):
    saveload.champ_picked = champ




