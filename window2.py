import tkinter.messagebox
import customtkinter as ctk
import os,tkinter,json
current_path = os.getcwd()
if not os.path.exists(f"{current_path}\\saved_config\\game_dir.json"):
    path_for_lol = None
    ctk.set_appearance_mode("Dark")
    app = ctk.CTk()
    width = app.winfo_screenwidth()
    height = app.winfo_screenheight()
    app_x = 300
    app_y = 100
    app.geometry(f"{app_x}x{app_y}+{width//2-app_x//2}+{height//2-app_y//2}")
    label = ctk.CTkLabel(app, text="This is your first time using this app\nPlease open your League of Legends directory")
    label.pack()
    def open_dir():
        global path_for_lol
        temp_path = ctk.filedialog.askdirectory()
        print(temp_path)
        
        yes_no=tkinter.messagebox.askyesno("Message",f"Are you sure this is the correct path?\n{temp_path}")
        if yes_no:
            path_for_lol = temp_path
            
            
            
            
            data = {"game_dir": path_for_lol}
            json_data = json.dumps(data,indent=4)
            with open("saved_config\\game_dir.json","w") as p:
                p.write(json_data)
            app.destroy()
        else:
            open_dir()
        
    button = ctk.CTkButton(app, text="Select", command=open_dir)
    button.pack(pady=20)

    app.mainloop()