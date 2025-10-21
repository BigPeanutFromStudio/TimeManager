import math
import tkinter as tk
from tkinter import ttk


# Holds time in miliseconds
class Timer():
    def __init__(self, starting_time=0):
        self.time = starting_time
        self.running = True
        self.time_display = tk.StringVar()

    def pause(self):
        self.running = False

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

        self.timer = Timer()

        self.label = ttk.Label(self, textvariable=self.timer.time_display) 
        self.label.pack()

        self.toggle_btn = ttk.Button(self, text="Toggle timer", command=self.timer.toggle)
        self.toggle_btn.pack()

        self.update_timer()

    def update_timer(self):
        self.timer.update()
        self.after(10, self.update_timer)




