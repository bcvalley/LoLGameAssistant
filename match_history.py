import customtkinter as ctk
import tkinter as tk
import os,ast
import loader,threading,asyncio,ctypes
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageFont
import backend
from CTkScrollableDropdown import *
from collections import Counter
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception as e:
    print("Could not set DPI awareness:", e)
PATH = os.getcwd()
BACKGROUND = "#242424"  # Background color
app = None  # Main CTK
x = 220  # Start of the UI
WIDTH = 0  # Screen width
HEIGHT = 0  # Screen height
font = ('Montserrat', 30, 'bold')  # Font used
widgets = []  # Labels, buttons and etc are placed here to destroy
already_clicked = False
center = 0
count = 20
y = 0
z = 1
image_refs = []
all_games = []
canvas = None
sortable_champions = None
aaa = None
fetched = False
canvas_width=  0
row,col,rowspan,colspan = 0,4,10,9
kill_this_label = None
host= ""
region= ""
async def draw_match_history(appp,username,tagline,label_to_kill:ctk.CTkLabel):
    global app,canvas_width, center, WIDTH, HEIGHT,kill_this_label, font, widgets, y, image_refs, all_games, canvas, sortable_champions, aaa,fetched
    app = appp
    kill_this_label = label_to_kill
    try:
        canvas.destroy()
        all_games.clear()
        image_refs.clear()
        sortable_champions.clear()
        aaa = None

    except:AttributeError
    WIDTH = app.winfo_screenwidth()
    HEIGHT = app.winfo_screenheight()
    
    sortable_champions = ["FILTER BY CHAMPION"]
    # Create the backend instance and get the match history

    if fetched ==False:
        
        aaa = backend.Backend(region, host, username, tagline, "RGAPI-6e925dd7-2bdc-4a78-ba23-35b3a895a417", count)
        all_games = await aaa.returnList()
        
    # with open("matches.txt", "r") as f:
    #     all_games = ast.literal_eval(f.read()) FOR TESTING
        #['Khazix', 1514, 12, 2, 8, 173, [6701, 3142, 3047, 6694, 3814, 0, 3364], 420, 26969, 30374, True, 1723804692557]
   
    
        fetched = True
        
        offset_x = (2.8/100)*WIDTH
        
        # Create a canvas and a vertical scrollbar
        canvas_width = WIDTH - x -offset_x
        #                          ^
        #                    4,3%  |
        
        
        offset_y = (44.5/100)*HEIGHT
        
        canvas_height = HEIGHT - offset_y
        canvas = tk.Canvas(app, width=canvas_width, height=canvas_height, bg=BACKGROUND)
        widgets.append(canvas)
        
        
        
        # Place the canvas and scrollbar
        canvas.grid(row=0,column=4,columnspan=10,rowspan=9,sticky="nsew")
        bind_mousewheel(canvas)
        #scrollbar.grid(row=0,column=14,rowspan=8,sticky="ns")
        
        # Populate the canvas with rectangles and images
        y = 0  # Starting y position
        z = 330
        await refresh(all_games, canvas, aaa, sortable_champions)
        getMostPlayedChamp(all_games)
        # Update the scroll region of the canvas
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        filter_combobox, sort_combobox, combo_box, refresh_button = draw_comboboxes(sortable_champions)
        widgets.append(filter_combobox)
        widgets.append(sort_combobox)
        widgets.append(combo_box)
        widgets.append(refresh_button)
        refresh_button.configure(command=lambda: refresh_clicked(filter_combobox, sort_combobox,combo_box))
    
def refresh_clicked(filter_combobox, sort_combobox,champ_combobox):
    global all_games, canvas, aaa, sortable_champions
    if canvas is not None:
        
        filtered_sorted_games = all_games[:]
        if sort_combobox.get() != "SORT BY":
            filtered_sorted_games = sort_algo(sort_combobox.get(), filtered_sorted_games)
        if filter_combobox.get() != "FILTER BY":
            filtered_sorted_games = filter_algo(filter_combobox.get(), filtered_sorted_games)
        if champ_combobox.get() != "FILTER BY CHAMPION":
            filtered_sorted_games = champ_filter(champ_combobox.get(),filtered_sorted_games)
        refresh(filtered_sorted_games, canvas, aaa, sortable_champions)

def bind_mousewheel(canvas):
    canvas.bind_all("<MouseWheel>", on_mousewheel)
def on_mousewheel(event):
    if event.num == 5 or event.delta == -120:
        canvas.yview_scroll(2, "units")
    elif event.num == 4 or event.delta == 120:
        canvas.yview_scroll(-2, "units")
def draw_comboboxes(values: list):
    my_row = 4
    my_row = check_grid(my_row)
    filter_values = ["FILTER BY", "WINS", "LOSSES", "NORMAL", "FLEX", "SOLO/DUO", "ARAM"]
    filter_combobox = ctk.CTkComboBox(app, values=filter_values, width=200, height=40)
    filter_combobox.grid(row=my_row-1, column=5,padx=10,sticky="n")
    
    sort_values = ["SORT BY", "Most Played Champion", "Most Kills", "Most Deaths", "Most Assists", "Least Kills", "Least Assists", "Least Deaths", "Best K/D/A"]
    sort_combobox = ctk.CTkComboBox(app, values=sort_values, width=200, height=40)
    sort_combobox.grid(row=my_row-1, column=6,sticky="n")

    loaded_refresh_image = Image.open(f"{PATH}\\icons\\refresh.png")
    refresh_resized_image = loaded_refresh_image.resize((30, 30))
    refresh_image = ImageTk.PhotoImage(refresh_resized_image)
    
    refresh_button = ctk.CTkButton(app, image=refresh_image, text="", fg_color=BACKGROUND, bg_color=BACKGROUND, height=30, width=30, hover_color="white", corner_radius=0)
    refresh_button.grid(row=my_row-1, column=8,sticky="n")
    
    combo_box = ctk.CTkComboBox(app,values=values, width=200, height=40)
    
    combo_box.grid(row=my_row-1, column=7,sticky="n",padx=10)
    
    return filter_combobox, sort_combobox, combo_box, refresh_button
def check_grid(my_row):
    if my_row<=rowspan:
        my_row =rowspan
        return my_row
    return my_row
async def refresh(all_games, canvas : tk.Canvas, aaa, sortable_champions):
    global y, z, image_refs,WIDTH
    ## offset spacings
    #icon dimentions
    x1,x2 = int((7.81/100)*WIDTH),int((7.81/100)*WIDTH)
    element0 = (4/100)*WIDTH # image 4.69% 60
    
    element1 = (13.28/100)*WIDTH # kda and duration 13.28% 170
    element3 = (18.75/100)*WIDTH # cs 18.75% 240
    element4 = (25/100)*WIDTH # items 25.78% 330
    mini_space = (3.13/100)*WIDTH # spacing between items 3.13% 40
    element5 = (51.23/100)*WIDTH # mode and map 52.23% 670
    element6 = (62.41/100)*WIDTH # damage and taken 66.41% 850
    element7 = (74.86/100)*WIDTH # win and date 80.86% 1035
   
    
    
    if canvas is None:
        return
    canvas.delete("all")
    y = 0 
    
    for each_game in all_games:
        
        items_start = element4
        icon_ending = y +(x1/2)
        if each_game[-2] == True:
            canvas.create_rectangle(10, y, canvas_width, y + x1, fill="#6C8EBF")
        else:
            canvas.create_rectangle(10, y, canvas_width, y + x1, fill="#db5e56")
        aaa.getIcon(each_game[0])
        if each_game[0] not in sortable_champions:
            sortable_champions.append(each_game[0])
        aaa.getItems(each_game[6])
        image_size = (x1, x2)
        loaded_champion_image = Image.open(f"{PATH}\\champion_icons\\{each_game[0]}.png")
        champ_resized = loaded_champion_image.resize(image_size)
        champ_image = ImageTk.PhotoImage(champ_resized)
        canvas.create_image(element0, icon_ending, image=champ_image)
        
        image_refs.append(champ_image)
        canvas.create_text(element1, icon_ending-30, text=f"{each_game[1]//60}m{each_game[1]%60}s ", fill="white", font=("Montserrat", 16, "bold"))
        canvas.create_text(element1, icon_ending+20, text=f"{each_game[2]}/{each_game[3]}/{each_game[4]} ", fill="black", font=("Montserrat", 16, "bold"))
        
        
        canvas.create_text(element3, icon_ending+20, text=f"CS:{each_game[5]}", font=("Montserrat", 12, "bold"))
        for each_item in each_game[6]:
            mini_image_size = (x1//3, x1//3)
            image_size = (mini_image_size)
            empty_item_size = x1//3
            if each_item == 0:
                canvas.create_rectangle(items_start-((x1/3)/2),icon_ending-((x1/3)/2),items_start+((x1/3)/2),icon_ending+((x1/3)/2), fill="grey")
                items_start += mini_space
            else:
                
                loaded_item_image = Image.open(f"{PATH}\\items\\{each_item}.png")
                item_resized = loaded_item_image.resize(image_size)
                item_image = ImageTk.PhotoImage(item_resized)
                canvas.create_image(items_start, icon_ending, image=item_image)
                image_refs.append(item_image)
                items_start += mini_space
        await aaa.getQueues()
        game_map, description = aaa.loadJsonQueues(each_game[7])
        canvas.create_text(element5, icon_ending-40, text=f"{game_map}", font=("Montserrat", 12, "bold"))
        canvas.create_text(element5, icon_ending+22, text=f"{description}", font=("Montserrat", 12, "bold"))
        canvas.create_text(element6,icon_ending-mini_space,text=f"DMG Dealt:{each_game[8]}",font=("Montserrat", 12, "bold"))
        canvas.create_text(element6,icon_ending+mini_space,text=f"DMG Taken:{each_game[9]}",font=("Montserrat", 12, "bold"))
        if each_game[10] == True:
            canvas.create_text(element7, icon_ending-20, text=f"WIN", font=font)
        else:
            canvas.create_text(element7, icon_ending-20, text="LOSS", font=font)
        canvas.create_text(element7, icon_ending+20, text=f"{aaa.timestamp_to_days_ago(each_game[11])} days ago", font=("Montserrat", 15, "bold"))
        y += x1  # Increment y position for the next rectangle
    canvas.update_idletasks()
    # Adjust the canvas height dynamically
    canvas.config(scrollregion=(0, 0, canvas.winfo_width(), y))
    loader.thread_should_run = False
    
def filter_algo(filtr, all_games):
    filtered_games = []
    if filtr == "WINS":
        filtered_games = [game for game in all_games if game[10] == True]
    elif filtr == "LOSSES":
        filtered_games = [game for game in all_games if game[10] == False]
    elif filtr == "NORMAL":
        filtered_games = [game for game in all_games if game[7] == 400]
        print(filtered_games)
    elif filtr == "FLEX":
        filtered_games = [game for game in all_games if game[7] == 440]
    elif filtr == "SOLO/DUO":
        filtered_games = [game for game in all_games if game[7] == 420]
    elif filtr == "ARAM":
        filtered_games = [game for game in all_games if game[7] == 450]
    return filtered_games

def champ_filter(filtr,all_games):
    temp_list = []
    for curr_game in all_games:
        if curr_game[0] == filtr:
            temp_list.append(curr_game)
    return temp_list
def sort_algo(sort_by, all_games):
    if sort_by == "Most Played Champion":
        # Implement sorting logic for Most Played Champion
        all_games = getSOm(all_games)
    elif sort_by == "Most Kills":
        all_games.sort(key=lambda x: x[2], reverse=True)
    elif sort_by == "Most Deaths":
        all_games.sort(key=lambda x: x[3], reverse=True)
    elif sort_by == "Most Assists":
        all_games.sort(key=lambda x: x[4], reverse=True)
    elif sort_by == "Least Kills":
        all_games.sort(key=lambda x: x[2])
    elif sort_by == "Least Deaths":
        all_games.sort(key=lambda x: x[3])
    elif sort_by == "Least Assists":
        all_games.sort(key=lambda x: x[4])
    elif sort_by == "Best K/D/A":
        all_games.sort(key=lambda x: (x[2] + x[4]) / (x[3] if x[3] != 0 else 1), reverse=True)
    return all_games

def getMostPlayedChamp(all_games):
    champion_counter = Counter(game[0] for game in all_games)
    most_played_champion = champion_counter.most_common(1)


def getSOm(all_games: list):
    all_played_champions = []
    sorted_by_most_common = []
    
    # Collect all played champions
    for game in all_games:
        all_played_champions.append(game[0])
    
    # Count occurrences of each champion
    counter = Counter(all_played_champions)
    
    # Sort by most common champion
    sorted_champions = counter.most_common()

    # Create sorted list by iterating through sorted champions list
    for champ, count in sorted_champions:
        for game in all_games:
            if game[0] == champ:
                sorted_by_most_common.append(game)

    return sorted_by_most_common

def get_widgets():
    
    return widgets 
