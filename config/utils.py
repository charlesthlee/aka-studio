import customtkinter
import pyperclip
import tkinter as tk
import os
import csv

class ClipboardUtils:
    @staticmethod
    def copy_to_clipboard(master, value):
        pyperclip.copy(value)
        ClipboardUtils.show_copy_confirmation(master, "Value copied to clipboard")

    @staticmethod
    def show_copy_confirmation(master, message):
        # Destroy existing spacer label if it exists
        existing_spacer_labels = master.winfo_children()
        for widget in existing_spacer_labels:
            if isinstance(widget, customtkinter.CTkLabel) and widget.cget("text") == "":
                widget.destroy()
                
        pop_up_frame = customtkinter.CTkFrame(master, width=175, height=35)
        pop_up_frame.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        # Add space after the last label
        spacer_label = customtkinter.CTkLabel(master, text="", font=('Arial', 12))
        spacer_label.pack(pady=10)
        confirmation_label = customtkinter.CTkLabel(pop_up_frame, text=message)
        confirmation_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        master.after(2000, spacer_label.destroy)
        master.after(2000, pop_up_frame.destroy)  # Remove the pop-up frame after 2 seconds

from typing import Callable, Union

class CTkSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: int = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(self, width=width-(2*height)+90, height=height-6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")
        self.entry.configure(justify="center")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "1")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) + self.step_size
            if value < 11:
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) - self.step_size
            if value >= 1:
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[int, None]:
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))


def rgb_to_hex(rgb):
    r, g, b = rgb
    r, g, b = round(r), round(g), round(b)
    return '#{0:02x}{1:02x}{2:02x}'.format(r, g, b)

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hsv(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin

    if delta == 0:
        h = 0
    elif cmax == r:
        h = 60 * (((g - b) / delta) % 6)
    elif cmax == g:
        h = 60 * ((b - r) / delta + 2)
    else:
        h = 60 * ((r - g) / delta + 4)

    if cmax == 0:
        s = 0
    else:
        s = delta / cmax

    v = cmax

    return h, s * 100, v * 100

def hsv_to_rgb(hsv):
    h, s, v = hsv
    h, s, v = h / 360, s / 100, v / 100
    c = v * s
    x = c * (1 - abs((h * 6) % 2 - 1))
    m = v - c

    if 0 <= h < 1/6:
        r, g, b = c, x, 0
    elif 1/6 <= h < 1/3:
        r, g, b = x, c, 0
    elif 1/3 <= h < 1/2:
        r, g, b = 0, c, x
    elif 1/2 <= h < 2/3:
        r, g, b = 0, x, c
    elif 2/3 <= h < 5/6:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    r = (r + m) * 255
    g = (g + m) * 255
    b = (b + m) * 255
    
    return r, g, b

def rgb_to_hsl(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin

    if delta == 0:
        h = 0
    elif cmax == r:
        h = 60 * (((g - b) / delta) % 6)
    elif cmax == g:
        h = 60 * ((b - r) / delta + 2)
    else:
        h = 60 * ((r - g) / delta + 4)

    l = (cmax + cmin) / 2

    if delta == 0:
        s = 0
    else:
        s = delta / (1 - abs(2 * l - 1))

    return h, s * 100, l * 100

def hsl_to_rgb(hsl):
    h, s, l = hsl
    h, s, l = h / 360, s / 100, l / 100
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h * 6) % 2 - 1))
    m = l - c / 2

    if 0 <= h < 1/6:
        r, g, b = c, x, 0
    elif 1/6 <= h < 1/3:
        r, g, b = x, c, 0
    elif 1/3 <= h < 1/2:
        r, g, b = 0, c, x
    elif 1/2 <= h < 2/3:
        r, g, b = 0, x, c
    elif 2/3 <= h < 5/6:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    r = (r + m) * 255
    g = (g + m) * 255
    b = (b + m) * 255

    return r, g, b

def rgb_to_cmyk(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    k = 1 - max(r, g, b)
    if k == 1:
        c, m, y = 0, 0, 0
    else:
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)

    return c, m, y, k

def cmyk_to_rgb(cmyk):
    c, m, y, k = cmyk
    c, m, y, k = c/100, m/100, y/100, k/100

    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)

    return r, g, b


def format_color_values(color_type, values):
        if color_type == "RGB":
            return f"{color_type}: {color_type.lower()}({round(values[0])}, {round(values[1])}, {round(values[2])})"
        elif color_type == "HEX":
            return f"{color_type}: {values.upper()}"
        elif color_type == "CMYK":
            return f"{color_type}: {color_type.lower()}({round(values[0]*100)}%, {round(values[1]*100)}%, {round(values[2]*100)}%, {round(values[3]*100)}%)"
        elif color_type == "HSL":
            return f"{color_type}: {color_type.lower()}({round(values[0])}, {round(values[1])}%, {round(values[2])}%)"
        elif color_type == "HSV":
            return f"{color_type}: {color_type.lower()}({round(values[0])}, {round(values[1])}%, {round(values[2])}%)"

def read_saved_colors_from_csv():
    # Read colors from CSV file
    saved_colors = []
    # Get the directory path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_directory, "..", "config", "saved_colors.csv")
    try:
        with open(csv_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                for color in row:
                    saved_colors.append(color)
    except FileNotFoundError:
        # Handle the case where the file is not found
        print("Error: saved_colors.csv file not found!")

    return saved_colors

def display_colors(self, container, colors, color_gear_element=False):
    check_vars = []  # To store the checkbox state variables

    for i, color in enumerate(colors):
        text = color.upper()
        if color_gear_element:
            check_var = customtkinter.IntVar()
            # Pass a lambda that calls limit_selection with the current state of check_vars
            checkbox = customtkinter.CTkCheckBox(container, variable=check_var, text="  "+text, font=("Segoe UI", 14),
                                                 onvalue=1, offvalue=0, command=lambda chk_var=check_var: self.limit_selection(chk_var, check_vars))
            checkbox.grid(row=i, column=0, padx=10, pady=5)
            check_vars.append(check_var)
        else:
            color_label = customtkinter.CTkLabel(container, text=text, font=("Segoe UI", 14))
            color_label.grid(row=i, column=0, padx=10, pady=5)
            color_label.bind("<Button-1>", lambda event, value=text: ClipboardUtils.copy_to_clipboard(self, value))

        color_block_frame = customtkinter.CTkFrame(container, width=30, height=30, fg_color=color)
        color_block_frame.grid(row=i, column=1, padx=10, pady=5)

        delete_button = customtkinter.CTkLabel(container, text='X', font=("Segoe UI", 15))
        delete_button.grid(row=i, column=2, padx=10, pady=0)
        delete_button.bind("<Button-1>", lambda event, value=color: delete_color(self, value))

    self.check_vars = check_vars

def delete_color(self, color_to_delete):
    colors = read_saved_colors_from_csv()
    # Get the directory path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_directory, "..", "config", "saved_colors.csv")
        
    # Filter out the color to delete
    updated_colors = [color for color in colors if color != color_to_delete]

    # Write the updated list back to the CSV
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for color in updated_colors:
            writer.writerow([color])
        
    self.display_saved_color_list(updated_colors)  # Refresh the displayed list of colors after deletion
