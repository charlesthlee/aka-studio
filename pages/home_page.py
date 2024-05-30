import customtkinter
import tkinter as tk
import os
from PIL import Image
from config.utils import Tooltip

class HomePage(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Set the width and height of the frame
        self.parent = parent

        button_styles = {
            'border_spacing': 5,
            'hover': True,
        }

        # Define the image paths
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

        # Add a label for the application title
        label_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(assets_dir, "ncm_app_dark.png")),
                                             dark_image=Image.open(os.path.join(assets_dir, "ncm_app_light.png")),
                                             size=(210 / self.parent.scale_factor, 70 / self.parent.scale_factor))

        self.label = customtkinter.CTkLabel(self, image=label_image, text="")
        self.label.pack(pady=35)

        scaled_module_image_size = int (300 / self.parent.scale_factor)
        color_grab_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(assets_dir, "color_grab_light.png")),
                                                  dark_image=Image.open(os.path.join(assets_dir, "color_grab_dark.png")),
                                                  size=(scaled_module_image_size, scaled_module_image_size))
        
        color_gear_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(assets_dir, "color_gear_light.png")),
                                                  dark_image=Image.open(os.path.join(assets_dir, "color_gear_dark.png")),
                                                  size=(scaled_module_image_size, scaled_module_image_size))

        color_converter_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(assets_dir, "color_converter_light.png")),
                                                  dark_image=Image.open(os.path.join(assets_dir, "color_converter_dark.png")),
                                                  size=(scaled_module_image_size, scaled_module_image_size))

        scaled_config_image_size = int (30 / self.parent.scale_factor)
        settings_image_file = Image.open(os.path.join(assets_dir, "settings.png"))                 
        settings_image = customtkinter.CTkImage(light_image=settings_image_file, dark_image=settings_image_file, size=(scaled_config_image_size, scaled_config_image_size))

        tutorials_image_file = Image.open(os.path.join(assets_dir, "tutorials.png"))
        tutorials_image = customtkinter.CTkImage(light_image=tutorials_image_file, dark_image=tutorials_image_file, size=(scaled_config_image_size, scaled_config_image_size))

        self.button_color_grab = customtkinter.CTkButton(master=self, image=color_grab_image, text="", command=self.parent.open_color_grab, **button_styles)
        self.button_color_grab.image = color_grab_image  # Keep a reference to prevent garbage collection
        self.button_color_grab.place(relx=0.4, rely=0.3, anchor=tk.CENTER)

        self.button_color_gear = customtkinter.CTkButton(master=self, image=color_gear_image, text="", command=self.parent.open_color_gear, **button_styles)
        self.button_color_gear.image = color_gear_image  # Keep a reference to prevent garbage collection
        self.button_color_gear.place(relx=0.6, rely=0.3, anchor=tk.CENTER)

        self.button_color_converter = customtkinter.CTkButton(master=self, image=color_converter_image, text="", command=self.parent.open_color_converter, **button_styles)
        self.button_color_converter.image = color_converter_image  # Keep a reference to prevent garbage collection
        self.button_color_converter.place(relx=0.5, rely=0.675, anchor=tk.CENTER)

        self.button_settings = customtkinter.CTkButton(master=self, image=settings_image, text="", command=self.parent.open_settings, width=scaled_config_image_size, height=scaled_config_image_size, **button_styles)
        self.button_settings.place(relx=0.48, rely=0.905, anchor=tk.CENTER)
        create_tooltip(self.button_settings, "Settings")

        self.button_tutorials = customtkinter.CTkButton(master=self, image=tutorials_image, text="", command=self.parent.open_tutorials, width=scaled_config_image_size, height=scaled_config_image_size, **button_styles)
        self.button_tutorials.place(relx=0.52, rely=0.905, anchor=tk.CENTER)
        create_tooltip(self.button_tutorials, "Tutorials")
    
def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget, bg="white")
    tooltip.wm_overrideredirect(True)
    tooltip.withdraw()
    label = tk.Label(tooltip, text=text, bg="white", bd=1, relief="solid", padx=2, pady=2)
    label.pack()

    def show_tooltip(event):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        tooltip.wm_geometry(f"+{x}+{y}")
        tooltip.deiconify()

    def hide_tooltip(event):
        tooltip.withdraw()

    widget.bind("<Enter>", show_tooltip)
    widget.bind("<Leave>", hide_tooltip)
