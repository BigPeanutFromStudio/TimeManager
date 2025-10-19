import math
import tkinter as tk


class AnalogClock(tk.Canvas):
    def __init__(self, parent, capital, pad):
        super().__init__(parent)
        self.pad = pad
        self.capital_var = capital
        self.current_time = self.capital_var.capital.get_current_time()
        self.radius = self.winfo_reqheight() - self.pad
        self.center_x = self.winfo_reqwidth() / 2
        self.center_y = (self.radius + self.pad) / 2
        self.face = self.create_oval(0, 0, self.radius, self.radius)
        self.update_clock()

    # TODO: maybe don't redraw the whole clock?
    def update_clock(self):
        self.current_time = self.capital_var.capital.get_current_time()
        self.delete(tk.ALL)
        self.face = self.create_oval(
            (self.winfo_reqwidth() / 2) - (self.radius / 2),
            self.pad,
            (self.winfo_reqwidth() / 2) + (self.radius / 2),
            self.radius,
            fill="white",
            width=2,
        )
        self.draw_numbers()
        self.draw_hands()
        self.after(200, self.update_clock)

    def draw_numbers(self):
        self.create_text(
            self.center_x,
            self.center_y - 0.8 * self.center_y,
            text="12",
            font=("TkDefaultFont", 16),
        )
        for i in range(1, 12):
            angle = i * (360 / 12)
            # TODO: get your head around this
            x = self.center_x + 0.8 * self.center_y * math.sin(math.radians(angle))
            y = self.center_y - 0.8 * self.center_y * math.cos(math.radians(angle))
            self.create_text(x, y, text=i, font=("TkDefaultFont", 16))

    def draw_hands(self):
        # Draw a point in the middle
        self.create_oval(
            self.center_x - 2,
            self.center_y + 2,
            self.center_x + 4,
            self.center_y - 4,
            fill="black",
        )

        current_second = self.current_time.second
        current_minute = self.current_time.minute
        current_hour = self.current_time.hour % 12

        # Draw an hour hand
        hour_angle = (current_hour * 60 * 60 + current_minute * 60 + current_second) * (
            360 / (60 * 60 * 12)
        )
        hour_hand_length = 0.5 * self.center_y
        x = self.center_x + hour_hand_length * math.sin(math.radians(hour_angle))
        y = self.center_y - hour_hand_length * math.cos(math.radians(hour_angle))
        self.create_line(self.center_x, self.center_y, x, y, fill="blue", width=3)

        # Draw a minute hand
        minute_angle = (current_minute * 60 + current_second) * (360 / (60 * 60))
        minute_hand_length = 0.7 * self.center_y
        x = self.center_x + minute_hand_length * math.sin(math.radians(minute_angle))
        y = self.center_y - minute_hand_length * math.cos(math.radians(minute_angle))
        self.create_line(self.center_x, self.center_y, x, y, fill="green", width=2)

        # Draw a second hand
        minute_angle = (current_second) * (360 / 60)
        minute_hand_length = 0.8 * self.center_y
        x = self.center_x + minute_hand_length * math.sin(math.radians(minute_angle))
        y = self.center_y - minute_hand_length * math.cos(math.radians(minute_angle))
        self.create_line(self.center_x, self.center_y, x, y, fill="red", width=1)
