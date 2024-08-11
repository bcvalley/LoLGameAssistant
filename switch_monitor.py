import customtkinter as ctk
from screeninfo import get_monitors

def move_to_next_monitor(app):
    # Temporarily unmaximize the window to move it
    app.state('normal')

    # Get the current window's size and position
    width = app.winfo_width()
    height = app.winfo_height()
    current_x = app.winfo_x()
    current_y = app.winfo_y()

    # Get the list of monitors
    monitors = get_monitors()

    # Determine which monitor the window is currently on
    current_monitor = None
    for monitor in monitors:
        if monitor.x <= current_x < monitor.x + monitor.width and \
           monitor.y <= current_y < monitor.y + monitor.height:
            current_monitor = monitor
            break

    if current_monitor is None:
        return

    # Calculate the next monitor index
    current_monitor_index = monitors.index(current_monitor)
    next_monitor_index = (current_monitor_index + 1) % len(monitors)
    next_monitor = monitors[next_monitor_index]

    # Move the window to the next monitor
    app.geometry(f'{next_monitor.width}x{next_monitor.height}+{next_monitor.x}+{next_monitor.y}')

    # Manually simulate the maximized state
    app.update_idletasks()  # Ensure the window updates its geometry
    app.state('zoomed')  # Attempt to maximize


