import tkinter as tk
from tkinter import ttk

from analog_clock import AnalogClock
from utils import get_time_diff, load_countries, str_to_capital, time_to_string


class CapitalVar:
    def __init__(self, capital, capital_list):
        self.capital = capital
        self.capital_list = capital_list
        self.str_var = tk.StringVar(value=self.capital.name)
        def callback_func(var, *_):
            self.capital = str_to_capital(self.str_var.get(), self.capital_list) 
        self.str_var.trace_add('write', callback_func)

# TODO: seperate self. to stuff that is actually needed, else can be local variables
# TODO: make it so it says do tylu and do przodu 

# TODO: IT WAS SUPPOSED TO BE A BTN :skull:
# TODO: Make it so a couple of clocks are always visible (timezone you're in and rest is configurable)

class CapitalTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.capitals = load_countries("stolice_państw.csv")

        self.selected_capital_one = CapitalVar(self.capitals[0], self.capitals)
        self.selected_capital_two = CapitalVar(self.capitals[1], self.capitals) 

        self.top = ttk.Frame(self)
        self.top.pack(side="top", fill="both", expand=True)

        self.bottom = ttk.Frame(self)
        self.bottom.pack(side="bottom", fill="both", expand=True)

        self.left = ttk.Frame(self.top)
        self.left.pack(side="left", fill="both", expand=True)

        self.right = ttk.Frame(self.top)
        self.right.pack(side="right", fill="both", expand=True)

        self.country_dropdown_one = CountryDropdown(
            self.left, self.selected_capital_one.str_var, self.capitals
        )

        self.country_dropdown_one.pack()

        self.country_dropdown_two = CountryDropdown(
            self.right, self.selected_capital_two.str_var, self.capitals
        )
        self.country_dropdown_two.pack()

        self.current_time_one = tk.StringVar(
            value=time_to_string(self.selected_capital_one.capital.get_current_time())
        )
        
        self.current_time_two = tk.StringVar(
            value=time_to_string(self.selected_capital_two.capital.get_current_time())
        )

        self.info_text = tk.StringVar(
            value="Te miasta różnią się o: " + str(get_time_diff(self.selected_capital_one.capital.get_current_time(), self.selected_capital_two.capital.get_current_time()))
        )
        self.info_label = ttk.Label(self.bottom, textvariable=self.info_text)
        self.info_label.pack(side="top")

        self.capital_label_one = ttk.Label(
            self.left, textvariable=self.current_time_one
        )
        self.capital_label_one.pack()
        self.capital_label_two = ttk.Label(
            self.right, textvariable=self.current_time_two
        )
        self.capital_label_two.pack()

        # Each clock is specific for each capital
        self.left_clock = AnalogClock(self.left, self.selected_capital_one, 10)
        self.left_clock.pack(padx=5, pady=5)

        self.right_clock = AnalogClock(self.right, self.selected_capital_two, 10)
        self.right_clock.pack(padx=5, pady=5)

        self.update_time()

    def update_time(self):
        self.current_time_one.set(time_to_string(self.selected_capital_one.capital.get_current_time()))
        self.current_time_two.set(time_to_string(self.selected_capital_two.capital.get_current_time()))
        self.info_text.set(
            "Te miasta różnią się o: " + str(get_time_diff(self.selected_capital_one.capital.get_current_time(), self.selected_capital_two.capital.get_current_time()))
            
        )
        self.after(1000, self.update_time)


# TODO: Add searching for capitals
class CountryDropdown(ttk.Combobox):
    def __init__(self, parent, variable, capitals):
        super().__init__(parent, textvariable=variable, state="readonly")

        capital_names = [c.name for c in capitals]
        capital_names.sort()

        self["values"] = capital_names

        self.set(variable.get())
