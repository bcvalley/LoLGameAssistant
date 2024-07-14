import customtkinter as ctk
import numpy as np
from PIL import Image ,ImageTk, ImageDraw
import backend,saveload
from CTkScrollableDropdown import *
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
dictionary = {}
name_of_champion = ""
profile_info = backend.Profile()
port,api = profile_info.getAPI("C:/Riot Games/League of Legends/lockfile")
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
    draw_champion_icon("Aatrox")
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
    draw_label.place(x=center,y=200)
    widgets.append(draw_label)
def draw_champion_icon(icon):
    global center
    image_size = (110,110)
    loaded_champion_image = Image.open(f"C:/Users/ivetoooooooooooo/OneDrive - Министерство на образованието и науката/Desktop/FF15/champion_icons/{icon}.png")
    ban_champ_resized = loaded_champion_image.resize(image_size)
    ban_champ_image = ImageTk.PhotoImage(ban_champ_resized)
    ban_champ = ctk.CTkLabel(app,image=ban_champ_image,text="")
    ban_champ.place(x=center-20,y=250)
    widgets.append(ban_champ)
    ban_champion_picked(icon)
def draw_combobox():
    global values
    combo_box = ctk.CTkComboBox(app,width=200,height=40)
    CTkScrollableDropdown(combo_box,values=values,command=lambda k: draw_champion_icon(k) or combo_box.set(k) or set_name_of_champion(k),autocomplete=True,button_height=30)
    combo_box.grid(row=5,column=9)
    widgets.append(combo_box)
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
    
            
    toggle_button = ctk.CTkButton(app,width=200,height=50,fg_color="#99ff33",text_color="black",text="ON/OFF",font=font,hover_color="white",command=switch)
    toggle_button.place(x=center+120,y=300)
    widgets.append(toggle_button)
    status_label = ctk.CTkLabel(app,text="status: off",text_color="red",bg_color=BACKGROUND,font=("Monsserat",16))
    status_label.place(x=center-10,y=370)
    widgets.append(status_label)
    
        


def get_widgets():
    
    return widgets

def ban_champion_picked(champ):
    saveload.ban_champion = champ




