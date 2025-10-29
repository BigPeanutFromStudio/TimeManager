import tkinter as tk
from tkinter import ttk

from analog_clock import AnalogStopwatch
from utils import format_ms


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
            return format_ms(self.time)
        else:
            return str(self.time)



class StopwatchTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.left = ttk.Frame(self)
        self.left.pack(side='left', fill='both', expand=True, pady=5, padx=5)

        self.right = ttk.Frame(self)
        self.right.pack(side='right', fill='both', expand=True, padx=5, pady=5)

        self.right_title = ttk.Label(self.right, text="Ostatnie czasy:", font=('', 20))
        self.right_title.pack()

        self.timer = Timer()
        self.time_list = []
        self.time_labels = []
        self.min_time = tk.StringVar(value="Najszybszy: 00:00:00")
        self.min_time_label = ttk.Label(self.right, textvariable=self.min_time, font=('', 18))
        self.min_time_label.pack(side='bottom')
        self.max_time = tk.StringVar(value="Najwolniejszy: 00:00:00")
        self.max_time_label = ttk.Label(self.right, textvariable=self.max_time, font=('', 18))
        self.max_time_label.pack(side='bottom')

        self.clock_space = ttk.Frame(self.left)
        self.clock_space.pack(side='top', fill='both', expand=True)
        self.analog_stopwatch = AnalogStopwatch(self.clock_space, self.timer, 5)
        self.analog_stopwatch.configure(width=350, height=350)
        self.analog_stopwatch.pack()

        self.other_space = ttk.Frame(self.left)
        self.other_space.pack(side='bottom', fill='both', expand=True)

        self.label = ttk.Label(self.other_space, textvariable=self.timer.time_display, font=('', 20)) 
        self.label.pack()

        self.toggle_btn_text = tk.StringVar(value="Start")
        self.toggle_btn = ttk.Button(self.other_space, textvariable=self.toggle_btn_text, command=self.timer.toggle)
        self.toggle_btn.pack()

        self.stop_btn = ttk.Button(self.other_space, text="Stop", command=self.record_time)
        self.stop_btn.pack()

        self.reset_btn = ttk.Button(self.other_space, text="Resetuj czasy", command=self.reset_times)
        self.reset_btn.pack()

        self.update_timer()

    def record_time(self):
        if self.timer.running:
            self.timer.running = False
            self.time_list.append(int(self.timer.get_time(formatted=False))) 

            self.min_time.set(value=f"Najszybszy {format_ms(min(self.time_list))}")
            self.max_time.set(value=f"Najwolniejszy {format_ms(max(self.time_list))}")

            label = ttk.Label(self.right, text=self.timer.get_time(), font=('', 16), padding=10)
            label.pack()
            self.time_labels.append(label)
            self.timer.reset()

    def reset_times(self):
        self.time_list.clear()
        for label in self.time_labels:
            label.destroy()
        self.time_labels.clear()
        self.min_time.set(value=f'Najszybszy {format_ms(0)}')
        self.max_time.set(value=f'Najwolniejszy {format_ms(0)}')
        self.timer.running = False
        self.timer.reset()


    def update_timer(self):
        self.timer.update()
        self.toggle_btn_text.set("Pauza" if self.timer.running else "Start")
        self.after(10, self.update_timer)




