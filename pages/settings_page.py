import customtkinter
import tkinter as tk

class SettingsPage(customtkinter.CTkFrame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)

        # Add a label for the application title
        self.label = customtkinter.CTkLabel(self, text="Settings", font=("Arial", 24))
        self.label.pack(pady=50)

        self.create_widgets()

        self.focus()

    def create_widgets(self):
        # Create a container frame for the main content
        self.settings_frame = customtkinter.CTkFrame(master=self, width=400, height=150)
        self.settings_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Dark Mode checkbox
        self.dark_mode_switch = customtkinter.CTkSwitch(self.settings_frame, text="Dark Mode", command=self.toggle_dark_mode)
        if self.parent.appearance_mode == "dark":
            self.dark_mode_switch.select()
        self.dark_mode_switch.pack(padx=30, pady=10)

        # Theme selector
        self.themes = ["Blue", "Green", "Dark-Blue"]
        self.selected_theme = customtkinter.StringVar(value=self.parent.theme)
        self.theme_selector = customtkinter.CTkOptionMenu(self.settings_frame, variable=self.selected_theme, values=self.themes, command=self.update_theme)
        self.theme_selector.pack(padx=30, pady=10)

        # Button to navigate to Home page
        self.home_button = customtkinter.CTkButton(self, text="Go to Home", command=self.parent.open_home_page)
        self.home_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def recreate_widgets(self):
        # Destroy current widgets
        self.settings_frame.destroy()
        # Recreate all widgets
        self.create_widgets()

    def toggle_dark_mode(self):
        if self.parent.appearance_mode == "dark":
            customtkinter.set_appearance_mode("light")
            self.parent.change_appearance_mode("light")
        else:
            customtkinter.set_appearance_mode("dark")
            self.parent.change_appearance_mode("dark")

    def update_theme(self, selected_theme):
        new_theme = selected_theme.lower()
        customtkinter.set_default_color_theme(new_theme)
        self.parent.change_theme(new_theme)
        # Recreate the entire SettingsPage instance to reflect the theme change
        self.recreate_widgets()
