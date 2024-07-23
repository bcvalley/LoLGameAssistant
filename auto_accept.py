import customtkinter as ctk
from PIL import Image ,ImageTk, ImageDraw
import backend,json,os,saveload
PATH = os.getcwd()
BACKGROUND = "#242424" #BACKGROUND COLOR 
app = None # Main CTK
x =220 # start of the UI
WIDTH = 0
HEIGHT = 0 # screen height
font = ('Montserrat',30,'bold') # FONT USED 
widgets =[] # labels,buttons and etc are placed here to destroy
already_clicked = False
center = 0
def get_config_dir():
    path = f"{PATH}\\saved_config\\game_dir.json"
    if os.path.exists(path):
        with open(path) as p:
            config = json.load(p)
            return config["game_dir"]


import game_dir
game_dir.game_dir = get_config_dir()
game_dir.game_dir += "/lockfile"

port,api = backend.Profile().getAPI(game_dir.game_dir)
def draw_accpet(appp):
    global app,WIDTH,HEIGHT,font,widgets,center
    app = appp
    WIDTH = app.winfo_screenwidth()
    HEIGHT = app.winfo_screenheight()
    center = (WIDTH-x)/2
    widgets.clear()
    draw_label()
    draw_toggle()
    
def draw_label():
    global center,widgets
    
    draw_label = ctk.CTkLabel(app,text="Auto Queue Accept",bg_color=BACKGROUND,font=font,anchor="center")
    draw_label.place(x=center,y=260)
    widgets.append(draw_label)
status=False
def draw_toggle():
    global status
    if status== True:
    
    
        toggle_button = ctk.CTkButton(app,width=200,height=50,fg_color="#99ff33",text_color="black",text="ON/OFF",font=font,hover_color="white")
        toggle_button.place(x=center,y=330)
        widgets.append(toggle_button)
        status_label = ctk.CTkLabel(app,text="status: on",text_color="green",bg_color=BACKGROUND,font=("Monsserat",16))
        status_label.place(x=center,y=300)
        toggle_button.configure(command=lambda: switch(status_label))
        
        widgets.append(status_label)
    elif status ==False:
        toggle_button = ctk.CTkButton(app,width=200,height=50,fg_color="#99ff33",text_color="black",text="ON/OFF",font=font,hover_color="white")
        toggle_button.place(x=center,y=330)
        widgets.append(toggle_button)
        status_label = ctk.CTkLabel(app,text="status: off",text_color="red",bg_color=BACKGROUND,font=("Monsserat",16))
        status_label.place(x=center,y=300)
        toggle_button.configure(command=lambda: switch(status_label))
        
        widgets.append(status_label)
def get_widgets():
    
    return widgets

def switch(label):
    global status
    if status==True:
        status=False
        saveload.auto_accept = False
        label.configure(text="status: off",text_color="red")
    else:
        label.configure(text="status: on",text_color="green")

        status=True
        saveload.auto_accept = True
        app.after(3000,do)
def do():
    global app,status
    if status == True:
        backend.AutoAccept.accept_event(port,api)
        print("sent! autoaccept")
        app.after(3000,do)
    