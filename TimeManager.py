import tkinter as tk
from tkinter import ttk

from capital_tab import CapitalTab
from stopwatch_tab import StopwatchTab


class App(tk.Tk):
    def __init__(self, title, size):

        # setup
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])

        # styles
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TNotebook.Tab", width=self.winfo_screenwidth(), font=('', 12))
        style.configure("time.TLabel", font=('', 16), background='gray')

        # widgets
        self.main = MainNotebook(self)
        self.main.pack(expand=True, fill="both")


class MainNotebook(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)
        self.capital_tab = CapitalTab(self)
        self.stopwatch_tab = StopwatchTab(self)
        self.add(self.capital_tab, text="Stolice")
        self.add(self.stopwatch_tab, text="Stoper")


if __name__ == "__main__":
    app = App("Time Manager", (850, 720))
    app.mainloop()
