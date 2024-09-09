import tkinter as tk
import ctypes

# Make the application DPI aware
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception as e:
    print("Could not set DPI awareness:", e)

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

print(f"Screen width: {screen_width}, Screen height: {screen_height}")

root.mainloop()
