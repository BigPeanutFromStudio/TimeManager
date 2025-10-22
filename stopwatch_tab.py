import math
import tkinter as tk
from tkinter import ttk


# Holds time in miliseconds
class Timer():
    def __init__(self, starting_time=0):
        self.time = starting_time
        self.running = False
        self.time_display = tk.StringVar(value="00:00:00")

    def reset(self):
        self.time = 0
        self.time_display.set("00:00:00")

    def toggle(self):
        self.running = not self.running

    def update(self):
        if self.running:
            self.time += 10
            self.time_display.set(self.get_time())

    def get_time(self, formatted=True):
        if formatted:
            hours = math.floor(self.time / 3600000)
            minutes = math.floor(self.time / 60000) % 60
            seconds = math.floor(self.time / 1000) % 60
            # display only 2 first digits of miliseconds
            miliseconds = math.floor(self.time / 10) % 1000
            return f'{minutes:02d}:{seconds:02d}:{miliseconds:02d}' if hours == 0 else f'{hours}:{minutes:02d}:{seconds:02d}' 
        else:
            return str(self.time)



class StopwatchTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.left = ttk.Frame(self)
        self.left.pack(side='left', fill='both', expand=True)

        self.right = ttk.Frame(self)
        self.right.pack(side='right', fill='both', expand=True)

        self.timer = Timer()
        self.time_list = []
        self.time_labels = []
        self.min_time = tk.StringVar(value="Min: 00:00:00")
        self.min_time_label = ttk.Label(self.right, textvariable=self.min_time)
        self.min_time_label.pack(side='bottom')
        self.max_time = tk.StringVar(value="Max: 00:00:00")
        self.max_time_label = ttk.Label(self.right, textvariable=self.max_time)
        self.max_time_label.pack(side='bottom')

        self.label = ttk.Label(self.left, textvariable=self.timer.time_display) 
        self.label.pack()

        self.toggle_btn_text = tk.StringVar(value="Start")
        self.toggle_btn = ttk.Button(self.left, textvariable=self.toggle_btn_text, command=self.timer.toggle)
        self.toggle_btn.pack()

        self.stop_btn = ttk.Button(self.left, text="Stop", command=self.record_time)
        self.stop_btn.pack()

        self.update_timer()

    def record_time(self):
        self.timer.running = False
        self.time_list.append(int(self.timer.get_time(formatted=False))) 

        self.min_time.set(value=f"Min {min(self.time_list)}")
        self.max_time.set(value=f"Max {max(self.time_list)}")

        label = ttk.Label(self.right, text=self.timer.get_time())
        label.pack()
        self.time_labels.append(label)
        self.timer.reset()


    def update_timer(self):
        self.timer.update()
        self.toggle_btn_text.set("Pauza" if self.timer.running else "Start")
        self.after(10, self.update_timer)




