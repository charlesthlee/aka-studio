import customtkinter
import tkinter
import json
import os
import ctypes

from pages.home_page import HomePage
from pages.settings_page import SettingsPage
from pages.tutorials_page import TutorialsPage
from pages.color_gear_page import ColorGearPage
from pages.color_grab_page import ColorGrabPage
from pages.color_converter_page import ColorConverterPage

class MainApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

        # Load theme and appearance mode from JSON file
        self.load_settings_from_json("settings.json")

        customtkinter.set_appearance_mode(self.appearance_mode)
        customtkinter.set_default_color_theme(self.theme.lower())

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{int(screen_width * 0.8)}x{int(screen_height * 0.8)}")
        self.after(0, lambda: self.wm_state('zoomed'))

        self.title("NCM App")
        self.home_page = HomePage(self)
        self.home_page.pack(expand=True, fill="both")
        self.frames = {}

    def load_settings_from_json(self, filename):
        # Get the directory path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the settings file in the config directory
        config_directory = os.path.join(current_directory, "config")
        settings_path = os.path.join(config_directory, filename)
        
        try:
            with open(settings_path, "r") as file:
                settings = json.load(file)
                self.appearance_mode = settings.get("appearance_mode", "dark")
                self.theme = settings.get("theme", "Blue")
        except FileNotFoundError or json.JSONDecodeError:
            # If file not found, use default settings
            self.appearance_mode = "dark"
            self.theme = "Blue"
        except json.JSONDecodeError:
            # If JSON decoding error, use default settings
            self.appearance_mode = "dark"
            self.theme = "Blue"

    def save_settings_to_json(self, filename):
        settings = {
            "appearance_mode": self.appearance_mode,
            "theme": self.theme
        }

        # Get the directory path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the settings file in the config directory
        config_directory = os.path.join(current_directory, "config")
        settings_path = os.path.join(config_directory, filename)

        with open(settings_path, "w") as file:
            json.dump(settings, file)

    def change_geometry(self, new_geometry):
        # Change the window geometry
        self.geometry(new_geometry)

    def change_title(self, new_title):
        # Change the window geometry
        self.title(new_title)
    
    def change_appearance_mode(self, new_mode):
        self.appearance_mode = new_mode
        self.save_settings_to_json("settings.json")
    
    def change_theme(self, new_theme):
        self.theme = new_theme
        self.save_settings_to_json("settings.json")
    
    def open_color_grab(self):
        self.home_page.destroy()
        self.grab_page = ColorGrabPage(self)
        self.frames["grab_page"] = self.grab_page
        self.grab_page.pack(expand=True, fill="both")
    
    def open_color_gear(self):
        self.home_page.destroy()
        self.gear_page = ColorGearPage(self)
        self.frames["gear_page"] = self.gear_page
        self.gear_page.pack(expand=True, fill="both")
    
    def open_color_converter(self):
        self.home_page.destroy()
        self.converter_page = ColorConverterPage(self)
        self.frames["converter_page"] = self.converter_page
        self.converter_page.pack(expand=True, fill="both")

    def open_home_page(self):
        self.destroy_all_frames()
        self.change_title("NCM App")
        self.home_page = HomePage(self)
        self.home_page.pack(expand=True, fill="both")

    def open_settings(self):
        self.home_page.destroy()
        self.destroy_all_frames()
        self.change_title("Settings")
        self.settings_page = SettingsPage(self)
        self.frames["settings_page"] = self.settings_page
        self.settings_page.pack(expand=True, fill="both")
    
    def open_tutorials(self):
        self.home_page.destroy()
        self.destroy_all_frames()
        self.change_title("Tutorials")
        self.tutorials_page = TutorialsPage(self)
        self.frames["tutorials_page"] = self.tutorials_page
        self.tutorials_page.pack(expand=True, fill="both")



    def destroy_all_frames(self):
        # Destroy all frames in the dictionary
        for frame_name, frame in self.frames.items():
            frame.destroy()
        self.frames = {}  # Clear the dictionary


if __name__ == "__main__":
    app = MainApp()
    app.iconbitmap("assets/icon.ico")
    app.mainloop()
