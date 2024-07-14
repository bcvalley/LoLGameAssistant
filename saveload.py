import customtkinter as ctk
import os, json
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

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
    canvas.place(x=220, y=0)
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
    save_button.place(x=center + 150, y=300)

    canvas.create_text(center - 320, 390, text="Load Configuration", fill="white", font=("Montserrat", 20, "bold"), anchor="w")
    canvas.create_text(center - 300, 460, text="Pick", fill="white", font=("Montserrat", 15, "bold"), anchor="w")
    canvas.create_text(center - 200, 460, text="Ban", fill="white", font=("Montserrat", 15, "bold"), anchor="w")
    canvas.create_text(center - 100, 460, text="Spells", fill="white", font=("Montserrat", 15, "bold"), anchor="w")
    canvas.create_text(center, 460, text="Accept", fill="white", font=("Montserrat", 15, "bold"), anchor="w")
    
    load_button = ctk.CTkButton(app, text="Load", command=lambda: load(), bg_color="dimgray", fg_color="black", font=('Montserrat', 15, 'bold'))
    load_button.place(x=center + 150, y=615)

def save(statuses):
    save_to_json(statuses)

def load():
    global center, canvas
    path = "C:/Users/ivetoooooooooooo/OneDrive - Министерство на образованието и науката/Desktop/FF15/saved_config/config.json"

    if os.path.exists(path):
        with open(path) as p:
            config = json.load(p)
            auto_accept = config["auto_accept"]
            auto_pick = config["auto_pick"]
            auto_ban = config["auto_ban"]
            spell1 = config["spell1"]
            spell2 = config["spell2"]
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
    path = f"C:/Users/ivetoooooooooooo/OneDrive - Министерство на образованието и науката/Desktop/FF15/champion_icons/{icon}.png"
    if not os.path.exists(path):
        path = f"C:/Users/ivetoooooooooooo/OneDrive - Министерство на образованието и науката/Desktop/FF15/spell_icons/Summoner{icon}.png"
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
    path = "C:/Users/ivetoooooooooooo/OneDrive - Министерство на образованието и науката/Desktop/FF15/saved_config/config.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w') as f:
        f.write(json_file)
