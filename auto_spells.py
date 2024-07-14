import customtkinter as ctk
import tkinter as tk
from PIL import Image ,ImageTk, ImageDraw
from CTkScrollableDropdown import *
import backend,saveload
profile_info = backend.Profile()
port,api = profile_info.getAPI("C:/Riot Games/League of Legends/lockfile")
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
ifel = []
left_spell_selected = ""
right_spell_selected = ""
icons_update_left = []
icons_update_right = []
dictionary_classic = {
    "Flash":4,
    "Heal":7,
    "Ghost":6,
    "Teleport":12,
    "Barrier":21,
    "Cleanse":1,
    "Ignite":14,
    "Exhaust":3,
    "Smite":11
}
combo_boxes = []

dictionary_aram = {
    "Flash":4,
    "Heal":7,
    "Ghost":6,
    "Clarity":30,
    "Snowball":32,
    "Barrier":21,
    "Cleanse":1,
    "Ignite":14,
    "Exhaust":3,
    "Smite":11
}
def draw_spells(appp):
    global app,WIDTH,HEIGHT,font,widgets,center
    app = appp
     # Configure the grid layout on the parent widget (app)
    
    WIDTH = app.winfo_screenwidth()
    HEIGHT = app.winfo_screenheight()
    center = (WIDTH-x)/2

    widgets.clear()
    combo_boxes.clear()
    ifel.clear()
    icons_update_left.clear()
    icons_update_right.clear()
    
    #backend.AutoSpells.download_spells() # UNCOMMENT TO DOWNLOAD ICONS
    draw_radiobutton()
    draw_label()
    draw_spell_one("None")
    draw_spell_two("None")
    draw_toggle()
    draw_left_combobox()
    draw_right_combobox()

def draw_label():
    global center,widgets
    
    draw_label = ctk.CTkLabel(app,text="Auto Spells",bg_color=BACKGROUND,font=font,anchor="center")
    draw_label.place(x=center,y=200)
    widgets.append(draw_label)
image_size = (90,90)
gamemode = "Classic"

def set_gamemode(value):
    global gamemode
    gamemode = value
    for x in ifel:
        x.destroy()
    draw_left_combobox()
    draw_right_combobox()
    print(f"Game mode set to: {gamemode}")

def get_gamemode():
    global gamemode
    return gamemode

def draw_radiobutton():
    global center, app  # Assuming app and center are defined elsewhere

    # Create a control variable for the radio buttons
    gamemode_var = ctk.StringVar(value="Classic")

    Radiobutton_classic = ctk.CTkRadioButton(app, text="Classic", value="Classic", variable=gamemode_var, command=lambda: set_gamemode("Classic"))
    Radiobutton_classic.grid(row=3, column=6)
    
    Radiobutton_aram = ctk.CTkRadioButton(app, text="ARAM", value="ARAM", variable=gamemode_var, command=lambda: set_gamemode("ARAM"))
    Radiobutton_aram.grid(row=3, column=8)
    widgets.append(Radiobutton_classic)
    widgets.append(Radiobutton_aram)
import customtkinter as ctk

def draw_left_combobox():
    
    if get_gamemode() == "Classic":
        values = list(dictionary_classic.keys())
    elif get_gamemode() == "ARAM":
        values = list(dictionary_aram.keys())

    left_combo_box = ctk.CTkComboBox(app, width=200, height=40, values=values)
    left_combo_box.configure(command=lambda k: set_icon_left(k) or left_combo_box.set(k) or check_both_comboboxes(left_combo_box))
    left_combo_box.grid(row=5, column=5)
    left_combo_box.set("Spell 1")

   

    ifel.append(left_combo_box)
    return values

def draw_right_combobox():
    if get_gamemode() == "Classic":
        values = list(dictionary_classic.keys())
    else:
        values = list(dictionary_aram.keys())

    right_combo_box = ctk.CTkComboBox(app, width=200, height=40, values=values)
    right_combo_box.configure(command=lambda k: set_icon_right(k) or right_combo_box.set(k) or check_both_comboboxes(right_combo_box))
    right_combo_box.grid(row=5, column=9)
    right_combo_box.set("Spell 2")
    

    ifel.append(right_combo_box)
    return values

def draw_spell_one(name):
    global icons_update_left
    loaded_spell_image = Image.open(f"C:/Users/ivetoooooooooooo/OneDrive - Министерство на образованието и науката/Desktop/FF15/spell_icons/Summoner{name}.png")
    spell_one_resized = loaded_spell_image.resize(image_size)
    spell_image = ImageTk.PhotoImage(spell_one_resized)
    spell = ctk.CTkLabel(app,image=spell_image,text="")
    spell.place(x=center,y=250)
    spell1_picked(name)
    icons_update_left.append(spell)
    hotkey_D = ctk.CTkLabel(app,text="D",bg_color=BACKGROUND,font=font)
    hotkey_D.place(x=center+35,y=350)
    widgets.append(hotkey_D)
def draw_spell_two(name):
    global icons_update_right
    loaded_spell_image = Image.open(f"C:/Users/ivetoooooooooooo/OneDrive - Министерство на образованието и науката/Desktop/FF15/spell_icons/Summoner{name}.png")
    spell_two_resized = loaded_spell_image.resize(image_size)
    spell_image = ImageTk.PhotoImage(spell_two_resized)
    spell = ctk.CTkLabel(app,image=spell_image,text="")
    spell.place(x=center+100,y=250)
    spell2_picked(name)
    icons_update_right.append(spell)
    hotkey_F = ctk.CTkLabel(app,text="F",bg_color=BACKGROUND,font=font)
    hotkey_F.place(x=center+135,y=350)
    widgets.append(hotkey_F)
status=False
def draw_toggle():
    
    def switch():
        global status,spell,combo_boxes,app
        if status:
            status=False
            status_label.configure(text="status: off",text_color="red")
        else:
            status_label.configure(text="status: on",text_color="green")
            status=True
            app.after(4000,do)

    toggle_button = ctk.CTkButton(app,width=200,height=50,fg_color="#99ff33",text_color="black",text="ON/OFF",font=font,hover_color="white",command=switch)
    toggle_button.place(x=center,y=430)
    widgets.append(toggle_button)
    status_label = ctk.CTkLabel(app,text="status: off",text_color="red",bg_color=BACKGROUND,font=("Monsserat",16))
    status_label.place(x=center,y=400)
    widgets.append(status_label)

def get_widgets():
    
    return widgets+ifel+icons_update_right+icons_update_left

def set_icon_left(name):
    global icons_update_left
    for icon in icons_update_left:
        icon.destroy()
    draw_spell_one(name)
def set_icon_right(name):
    global icons_update_right
    for icon in icons_update_right:
        icon.destroy()
    draw_spell_two(name)
def check_both_comboboxes(cb):
    global combo_boxes
    
    try:
        
        if combo_boxes and combo_boxes[0] == cb:
            print("Same widget")
        else:
            combo_boxes.append(cb)
            print(combo_boxes)
    except IndexError:
        pass


    if len(combo_boxes) == 2:
        try:
            left = combo_boxes[0]
            right = combo_boxes[1]
            if left.get() == right.get():
                tk.messagebox.showerror(title="Error", message="Please choose different spells")

                left.set("Spell 1")
                set_icon_left("None")
                right.set("Spell 2")
                set_icon_right("None")
                
                combo_boxes.clear()  
        except IndexError:
            pass

def do():
    global status,api,port,combo_boxes
    if status:
        backend.AutoSpells.spells_event(combo_boxes[0].get(),combo_boxes[1].get(),port,api)
        app.after(4000,do)
    
def spell1_picked(spell):
    saveload.spell1 = spell


def spell2_picked(spell):
    saveload.spell2 = spell