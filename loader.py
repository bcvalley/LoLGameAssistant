import time
thread_should_run = False
def loader_animation(app,label):
    states = ["Please wait\nLoading.", "Please wait\nLoading..", "Please wait\nLoading..."]
    while thread_should_run:
        for state in states:
            label.configure(text=state)
            time.sleep(0.2)
    label.destroy()