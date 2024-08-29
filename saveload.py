import customtkinter as ctk
import os, json
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import auto_spells
import auto_accept as aa
import auto_pick as ap
import auto_ban as ab
PATH = os.getcwd()
BACKGROUND = "#242424"
WIDTH = 0
HEIGHT = 0
center = 0
auto_accept = None
champ_picked = "None"
ban_champion = "None"
spell1 = "None"
spell2 = "None"
json_file_loaded_values = []
canvas = None
application = None
widgets = []
def draw_save(app, statuses):
    global canvas, center, application
    if canvas is not None:
        canvas.destroy()
    WIDTH = app.winfo_screenwidth()
    HEIGHT = app.winfo_screenheight()
    center = WIDTH / 2
    statuses[0] = auto_accept
    statuses[1] = champ_picked
    statuses[2] = ban_champion
    statuses[3] = spell1
    statuses[4] = spell2
    canvas = ctk.CTkCanvas(app, width=2000, height=3000, bg=BACKGROUND, highlightthickness=0)
    application = app
    canvas.grid(row=0, column=4,columnspan=14,rowspan=2000)
    canvas.create_rectangle(center - 335, 50, center + 100, 350, fill="dimgray")
    canvas.create_rectangle(center - 335, 370, center + 100, 670, fill="dimgray")
    canvas.create_text(center - 320, 80, text="Save Current Configuration", fill="white", font=("Montserrat", 20, "bold"), anchor="w")
    canvas.create_text(center - 300, 150, text="Pick", fill="white", font=("Montserrat", 15, "bold"), anchor="w")
    
    img_pick = draw_champion_icon(champ_picked, (90, 90))
    canvas.create_image(center - 320, 200, image=img_pick, anchor="nw")
    canvas.pick_image = img_pick

    canvas.create_text(center - 200, 150, text="Ban", fill="white", font=("Montserrat", 15, "bold"), anchor="w")
    img_ban = draw_champion_icon(ban_champion, (90, 90))
    canvas.create_image(center - 220, 200, image=img_ban, anchor="nw")
    canvas.ban_image = img_ban

    canvas.create_text(center - 100, 150, text="Spells", fill="white", font=("Montserrat", 15, "bold"), anchor="w")
    img_spell1 = draw_champion_icon(spell1, (40, 40))
    canvas.create_image(center - 110, 200, image=img_spell1, anchor="nw")
    canvas.spell1_image = img_spell1
    
    img_spell2 = draw_champion_icon(spell2, (40, 40))
    canvas.create_image(center - 70, 200, image=img_spell2, anchor="nw")
    canvas.spell2_image = img_spell2

    canvas.create_text(center, 150, text="Accept", fill="white", font=("Montserrat", 15, "bold"), anchor="w")
    if statuses[0] == True:
        canvas.create_text(center, 220, text="ON", fill="green", font=("Montserrat", 18, "bold"), anchor="w")
    else:
        canvas.create_text(center, 220, text="OFF", fill="red", font=("Montserrat", 18, "bold"), anchor="w")
    
    save_button = ctk.CTkButton(app, text="Save", command=lambda: save(statuses), bg_color="dimgray", fg_color="black", font=('Montserrat', 15, 'bold'))
    save_button.grid(row=5, column=8)
    save_button.tkraise()
    widgets.append(save_button)
    canvas.create_text(center - 320, 390, text="Load Configuration", fill="white", font=("Montserrat", 20, "bold"), anchor="w")
    canvas.create_text(center - 300, 460, text="Pick", fill="white", font=("Montserrat", 15, "bold"), anchor="w")
    canvas.create_text(center - 200, 460, text="Ban", fill="white", font=("Montserrat", 15, "bold"), anchor="w")
    canvas.create_text(center - 100, 460, text="Spells", fill="white", font=("Montserrat", 15, "bold"), anchor="w")
    canvas.create_text(center, 460, text="Accept", fill="white", font=("Montserrat", 15, "bold"), anchor="w")
    
    load_button = ctk.CTkButton(app, text="Load", command=lambda: load(), bg_color="dimgray", fg_color="black", font=('Montserrat', 15, 'bold'))
    load_button.grid(row=9, column=8)
    widgets.append(load_button)
    widgets.append(canvas)

    canvas.create_rectangle(5,50,300,130,fill="dimgray")
    game_dir_label = ctk.CTkLabel(app,font=('Montserrat', 16, 'bold'),bg_color="dimgray")
    game_dir_label.grid(row=1,column=2,columnspan=4,sticky="e")
    #game_dir_label.tkraise()
    widgets.append(game_dir_label)
    def open_folder():
        directory = ctk.filedialog.askdirectory()
        game_dir_label.configure(text=directory)
        save_game_dir(directory)
    
    get_game_dir = ctk.CTkButton(app, text="Change Game Directory", command=open_folder, bg_color="dimgray", fg_color="black", font=('Montserrat', 15, 'bold'))
    get_game_dir.grid(row=2, column=3,columnspan=4,rowspan=1,sticky='n')
    widgets.append(get_game_dir)
    config_path = f"{PATH}\\saved_config\\game_dir.json"
    if os.path.exists(config_path):
        with open(config_path) as p:
            config = json.load(p)
            game_dir_label.configure(text=config["game_dir"])
            

    else:
        game_dir_label.configure(text="Game directory not found")

    all_on_button = ctk.CTkButton(app, text="All ON ", command=lambda: all_on(), bg_color=BACKGROUND, fg_color="green", font=('Montserrat', 20, 'bold'),corner_radius=200)
    all_off_button = ctk.CTkButton(app, text="All OFF", command=lambda: all_off(), bg_color=BACKGROUND, fg_color="red", font=('Montserrat', 20, 'bold'),corner_radius=200)
    all_off_button.place(relx=0.3,rely=0.25,anchor="c")
    all_on_button.place(relx=0.3,rely=0.2,anchor="c")
    widgets.append(all_on_button)
    widgets.append(all_off_button)
def all_on():
    aa.status = True
    ap.status = True
    ab.status = True
    auto_spells.status = True
def all_off():
    aa.status = False
    ap.status = False
    ab.status = False
    auto_spells.status = False
def save_game_dir(game_dir):
    path = f"{PATH}\\saved_config\\game_dir.json"
    config = {"game_dir": game_dir}
    json_config = json.dumps(config,indent=4)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w') as f:
        f.write(json_config)

def get_config_dir():
    path = f"{PATH}\\saved_config\\game_dir.json"
    if os.path.exists(path):
        with open(path) as p:
            config = json.load(p)
            return config["game_dir"]



def save(statuses):
    save_to_json(statuses)

def load():
    global center, canvas
    path = f"{PATH}\\saved_config\\config.json"

    if os.path.exists(path):
        with open(path) as p:
            config = json.load(p)
            auto_accept = config["auto_accept"]
            if auto_accept == None:
                aa.status = False
            elif auto_accept == True:
                aa.status = True
            auto_pick = config["auto_pick"]
            ap.loaded_champion_from_config = auto_pick
            auto_ban = config["auto_ban"]
            ab.loaded_ban_champion_from_config = auto_ban
            spell1 = config["spell1"]
            auto_spells.spell1 = spell1
            spell2 = config["spell2"]
            auto_spells.spell2 = spell2
            json_file_loaded_values = [auto_accept, auto_pick, auto_ban, spell1, spell2]
            print(json_file_loaded_values)

            if auto_pick != "None":
                pic_image = draw_champion_icon(auto_pick, (90, 90))
                canvas.create_image(center - 320, 520, image=pic_image, anchor="nw")
                canvas.pick_image_loaded = pic_image
            else:
                pic_image = draw_champion_icon("None", (90, 90))
                canvas.create_image(center - 320, 520, image=pic_image, anchor="nw")
                canvas.pick_image_loaded = pic_image

            if auto_ban != "None":
                ban_image = draw_champion_icon(auto_ban, (90, 90))
                canvas.create_image(center - 220, 520, image=ban_image, anchor="nw")
                canvas.ban_image_loaded = ban_image
            else:
                ban_image = draw_champion_icon("None", (90, 90))
                canvas.create_image(center - 220, 520, image=ban_image, anchor="nw")
                canvas.ban_image_loaded = ban_image

            if spell1 != "None":
                spell1_image = draw_champion_icon(spell1, (40, 40))
                canvas.create_image(center - 110, 520, image=spell1_image, anchor="nw")
                canvas.spell1_image_loaded = spell1_image
            else:
                spell1_image = draw_champion_icon("None", (40, 40))
                canvas.create_image(center - 110, 520, image=spell1_image, anchor="nw")
                canvas.spell1_image_loaded = spell1_image

            if spell2 != "None":
                spell2_image = draw_champion_icon(spell2, (40, 40))
                canvas.create_image(center - 70, 520, image=spell2_image, anchor="nw")
                canvas.spell2_image_loaded = spell2_image
            else:
                spell2_image = draw_champion_icon("None", (40, 40))
                canvas.create_image(center - 70, 520, image=spell2_image, anchor="nw")
                canvas.spell2_image_loaded = spell2_image
            if auto_accept == True:
                canvas.create_text(center, 535, text="ON", fill="green", font=("Montserrat", 18, "bold"), anchor="w")
            else:
                canvas.create_text(center, 535, text="OFF", fill="red", font=("Montserrat", 18, "bold"), anchor="w")
            tk.messagebox.showinfo("Done!", "Config loaded successfully")
def draw_champion_icon(icon, image_size):
    path = f"{PATH}\\champion_icons\\{icon}.png"
    if not os.path.exists(path):
        path = f"{PATH}\\spell_icons\\Summoner{icon}.png"
    loaded_champion_image = Image.open(path)
    ban_champ_resized = loaded_champion_image.resize(image_size)
    ban_champ_image = ImageTk.PhotoImage(ban_champ_resized)
    return ban_champ_image

def save_to_json(status):
    file = {
        "auto_accept": status[0],
        "auto_pick": status[1],
        "auto_ban": status[2],
        "spell1": status[3],
        "spell2": status[4],
    }
    json_file = json.dumps(file, indent=4)
    path = f"{PATH}\\saved_config\\config.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w') as f:
        f.write(json_file)

def get_widgets():
    return widgets