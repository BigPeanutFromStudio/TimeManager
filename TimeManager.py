import math
import tkinter as tk
from tkinter import ttk

from utils import (get_capital_time, get_distance_between, get_time_diff,
                   load_countries, str_to_capital)

capitals = load_countries('stolice_państw.csv')

class App(tk.Tk):
    def __init__(self, title, size):

        # setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])

        # styles
        style = ttk.Style(self)
        style.configure('TNotebook.Tab', width=self.winfo_screenwidth())

        # widgets
        self.main = MainNotebook(self)
        self.main.pack(expand=True, fill='both')

class MainNotebook(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)
        self.capital_tab = CapitalTab(self)
        self.stopwatch_tab = StopwatchTab(self)
        self.add(self.capital_tab, text="Stolice")
        self.add(self.stopwatch_tab, text="Stoper")

        

# TODO: divide into two containers packed vertically, upper one is grid with select and stuff, lower one is clocks also divided in half horizontally
class CapitalTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # TODO: Fix this, store the current capital please for the love of all that is holy 
        # if the text NEEDS to be a stringvar etc. just seperate the variables and make stringvar depend on current capitals
        self.selected_capital_one = tk.StringVar(value=str(capitals[0]))
        self.selected_capital_two = tk.StringVar(value=str(capitals[1]))


        # TODO: Maybe add stringvar to clock to automatically update its time
        def left_callback(var, index, mode):
            try:
                self.left_clock.pack_forget()
                self.left_clock = AnalogClock(self.left, str_to_capital(self.selected_capital_one.get(), capitals), 10)
                self.left_clock.pack(padx=5, pady=5)
            except AttributeError:
                return

        def right_callback(var, index, mode):
            try:
                self.right_clock.pack_forget()
                self.right_clock = AnalogClock(self.right, str_to_capital(self.selected_capital_two.get(), capitals), 10)
                self.right_clock.pack(padx=5, pady=5)
            except AttributeError:
                return

        self.selected_capital_one.trace_add('write', left_callback)
        self.selected_capital_two.trace_add('write', right_callback)

        self.top = ttk.Frame(self)
        self.top.pack(side='top', fill='both', expand=True)

        self.bottom = ttk.Frame(self)
        self.bottom.pack(side='bottom', fill='both', expand=True)

        self.left = ttk.Frame(self.top)
        self.left.pack(side='left', fill='both', expand=True)

        self.right = ttk.Frame(self.top)
        self.right.pack(side='right', fill='both', expand=True)

        self.country_dropdown_one = CountryDropdown(self.left, self.selected_capital_one)
        self.country_dropdown_one.pack()

        self.country_dropdown_two = CountryDropdown(self.right, self.selected_capital_two)
        self.country_dropdown_two.pack()

        self.current_time_one = tk.StringVar(value=str(get_capital_time(str_to_capital(self.selected_capital_one.get(), capitals))))
        self.current_time_two = tk.StringVar(value=str(get_capital_time(str_to_capital(self.selected_capital_two.get(), capitals))))

        # TODO: Handle negative values
        self.info_text = tk.StringVar(value="Te miasta różnią się o: " + str(get_time_diff(self.current_time_one.get(), self.current_time_two.get())))
        self.info_label = ttk.Label(self.bottom, textvariable=self.info_text)
        self.info_label.pack(side='top')


        self.capital_label_one = ttk.Label(self.left, textvariable=self.current_time_one)
        self.capital_label_one.pack()
        self.capital_label_two = ttk.Label(self.right, textvariable=self.current_time_two)
        self.capital_label_two.pack()

        self.left_clock = AnalogClock(self.left, capitals[0], 10)
        self.left_clock.pack(padx=5, pady=5)

        self.right_clock = AnalogClock(self.right, capitals[1], 10)
        self.right_clock.pack(padx=5, pady=5)

        self.update_time()

    def update_time(self):
        self.current_time_one.set(str(get_capital_time(str_to_capital(self.selected_capital_one.get(), capitals))))
        self.current_time_two.set(str(get_capital_time(str_to_capital(self.selected_capital_two.get(), capitals))))
        self.info_text.set("Te miasta różnią się o: " + str(get_time_diff(self.current_time_one.get(), self.current_time_two.get())))
        self.after(1000, self.update_time)



# TODO: Add searching for capitals
class CountryDropdown(ttk.Combobox):
    def __init__(self, parent, variable):
        super().__init__(parent, textvariable=variable, state='readonly')
    
        capital_names = [str(c) for c in capitals]
        capital_names.sort()
        
        self['values'] = capital_names
        
        self.set(variable.get())

class StopwatchTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = ttk.Label(self, text="Text in stopwatch")
        self.label.pack()


# Each clock is specific for each capital
class AnalogClock(tk.Canvas):
    def __init__(self, parent, capital, pad):
        super().__init__(parent)
        self.pad = pad
        self.capital = capital
        self.current_time = get_capital_time(self.capital)
        self.radius = self.winfo_reqheight() - self.pad
        self.center_x = (self.winfo_reqwidth() / 2)
        self.center_y = (self.radius + self.pad) / 2
        self.face = self.create_oval(0, 0, self.radius, self.radius) 
        self.update_clock()

    def update_clock(self):
        self.delete(tk.ALL)
        self.current_time = get_capital_time(self.capital)
        self.face = self.create_oval((self.winfo_reqwidth() / 2) - (self.radius / 2), self.pad, (self.winfo_reqwidth() / 2) + (self.radius / 2), self.radius, fill="white") 
        self.draw_numbers()
        self.draw_hands()
        self.after(200, self.update_clock)

    def draw_numbers(self):
        self.create_text(self.center_x, self.center_y - 0.8 * self.center_y, text='12', font=('TkDefaultFont', 16))
        for i in range(1, 12):
            angle = i * (360/12)
            # TODO: get your head around this
            x = self.center_x + 0.8 * self.center_y * math.sin(math.radians(angle))
            y = self.center_y - 0.8 * self.center_y * math.cos(math.radians(angle))
            self.create_text(x, y, text=i, font=('TkDefaultFont', 16))

    def draw_hands(self):
        # Draw a point in the middle
        self.create_oval(self.center_x - 2, self.center_y + 2, self.center_x + 4, self.center_y - 4, fill='black')

        current_second = float(self.current_time[6:])
        current_minute = float(self.current_time[3:5])
        current_hour = float(self.current_time[:2]) % 12

        # Draw an hour hand
        hour_angle = (current_hour * 60 * 60 + current_minute * 60 + current_second) * (360 / (60 * 60 * 12))
        hour_hand_length = 0.5 * self.center_y 
        x = self.center_x +  hour_hand_length * math.sin(math.radians(hour_angle))
        y = self.center_y - hour_hand_length * math.cos(math.radians(hour_angle))
        self.create_line(self.center_x, self.center_y, x, y, fill='blue', width=3)

        # Draw a minute hand
        minute_angle = (current_minute * 60 + current_second) * (360 / (60 * 60))
        minute_hand_length = 0.7 * self.center_y 
        x = self.center_x +  minute_hand_length * math.sin(math.radians(minute_angle))
        y = self.center_y - minute_hand_length * math.cos(math.radians(minute_angle))
        self.create_line(self.center_x, self.center_y, x, y, fill='green', width=2)

        # Draw a second hand
        minute_angle = (current_second) * (360 / 60)
        minute_hand_length = 0.8 * self.center_y 
        x = self.center_x +  minute_hand_length * math.sin(math.radians(minute_angle))
        y = self.center_y - minute_hand_length * math.cos(math.radians(minute_angle))
        self.create_line(self.center_x, self.center_y, x, y, fill='red', width=1)
        



if __name__ == "__main__":
    app = App("Time Manager", (850, 720))
    app.mainloop()

