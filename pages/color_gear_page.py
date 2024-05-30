import tkinter as tk
from tkinter import ttk, colorchooser
import customtkinter
import os
import csv
from config.utils import ClipboardUtils, hex_to_rgb, rgb_to_cmyk, rgb_to_hex, rgb_to_hsl, rgb_to_hsv, format_color_values, read_saved_colors_from_csv, display_colors

class ColorGearPage(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Define colors for dark and light modes
        self.dark_mode_colors = {
            "bg": "#333333",
            "frame_bg": "#292929",
            "button_fg": "#505050",
            "button_text": "#FFFFFF",
            "button_hover": "#686868",
            "label_text": "#FFFFFF",
            "palette_box_bg": "#e0e0e0",
            "color_box_bg": "#FFFFFF",
            "instructions_text": "lightgray"
        }
        
        self.light_mode_colors = {
            "bg": "#FFFFFF",
            "frame_bg": "#F0F0F0",
            "button_fg": "#E0E0E0",
            "button_text": "#000000",
            "button_hover": "#C0C0C0",
            "label_text": "#000000",
            "palette_box_bg": "#F8F8F8",
            "color_box_bg": "#C0C0C0",
            "instructions_text": "black"
        }

        # Select colors based on the current appearance mode
        self.color_scheme = self.dark_mode_colors if self.parent.appearance_mode == "dark" else self.light_mode_colors

        self.configure(fg_color=self.color_scheme["bg"])  # Dark grey background for the frame
        self.selected_colors_1 = [None] * 5  # First set of 5 colors
        self.selected_colors_2 = [None] * 5  # Second set of 5 colors

        self.main_frame = customtkinter.CTkFrame(self, width=500, height=600, fg_color=self.color_scheme["frame_bg"])
        self.main_frame.place(relx=0.375, rely=0.3, anchor=tk.CENTER)

        self.side_frame = customtkinter.CTkFrame(self, width=350, height=400, fg_color=self.color_scheme["frame_bg"])
        self.side_frame.place(relx=0.85, rely=0.3, anchor=tk.CENTER)
        self.saved_colors_container = None

        self.instructions_label = customtkinter.CTkLabel(self.side_frame, text="Use the 'Display Saved Colors' button to view and import colors.",
                                                         font=('Arial', 10, 'italic'), text_color=self.color_scheme["instructions_text"])
        self.instructions_label.pack(pady=(10, 0))
        self.confirmation_label = None
        
        self.display_saved_button = customtkinter.CTkButton(self.side_frame, text="Display Saved Colors", command=self.display_saved_colors, font=("Segoe UI", 12))
        self.display_saved_button.pack(padx=20, pady=10)
        # Guidance Text
        self.info_label = customtkinter.CTkLabel(self.main_frame, text="Select a color using 'Select Color' buttons. Click on RGB labels to view color details.",
                                                 font=('Arial', 10, 'italic'), text_color=self.color_scheme["instructions_text"])
        self.info_label.grid(row=0, column=0, columnspan=10, pady=(10, 10), sticky="ew")

        # Styling adjustments for dark mode
        self.button_styles = {
            'border_spacing': 5,
            'hover': True,
            'fg_color': self.color_scheme["button_fg"],  # Dark button color
            'text_color': self.color_scheme["button_text"],  # White text color
            'hover_color': self.color_scheme["button_hover"]  # Lighter grey on hover
        }
        self.label_font = ('Arial', 12, 'normal')
        self.palette_font = ('Arial', 14, 'bold')
        self.label_color = self.color_scheme["label_text"]  # White color for labels

        # Setup color selection and palettes for two sets
        self.setup_color_set(1)
        self.setup_color_set(2)

        # Separator
        self.separator = ttk.Separator(self.main_frame, orient='vertical')
        self.separator.grid(row=1, column=5, rowspan=10, sticky="ns")

        # Navigation Button
        self.home_button = customtkinter.CTkButton(self, text="Go to Home", command=self.parent.open_home_page, **self.button_styles)
        self.home_button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

        self.popup = None


    def setup_color_set(self, set_number):
        offset = (set_number - 1) * 6
        for i in range(5):
            # Color selection labels and buttons
            color_label = customtkinter.CTkLabel(self.main_frame, text=f"Set {set_number}, Color {i+1}:", font=self.label_font, text_color=self.label_color)
            color_label.grid(row=2*i + 1, column=offset, padx=10, pady=5, sticky="w")

            color_btn = customtkinter.CTkButton(self.main_frame, text="Select Color",
                                                command=lambda idx=i, sn=set_number: self.select_color(idx, sn), **self.button_styles)
            color_btn.grid(row=2*i + 1, column=offset + 1, padx=10, pady=5, sticky="w")

            rgb_label = customtkinter.CTkLabel(self.main_frame, text="RGB: ", font=self.label_font, text_color=self.label_color)
            rgb_label.grid(row=2*i + 1, column=offset + 2, padx=10, pady=5, sticky="w")
            rgb_label.bind("<Button-1>", lambda event, idx=i, sn=set_number: self.show_color_popup(idx, sn))

            color_box = customtkinter.CTkCanvas(self.main_frame, width=30, height=30, bg=self.color_scheme["color_box_bg"])
            color_box.grid(row=2*i + 1, column=offset + 3, padx=10, pady=5, sticky="w")

            color_list = self.selected_colors_1 if set_number == 1 else self.selected_colors_2
            color_list[i] = {"color_btn": color_btn, "rgb_label": rgb_label, "color_box": color_box}

            if i == 4:  # Only create palette after last color
                self.create_palette_widgets(set_number, offset)

    def select_color(self, idx, set_number):
        color = colorchooser.askcolor()[0]
        if color:
            hex_color = rgb_to_hex(color)
            color_list = self.selected_colors_1 if set_number == 1 else self.selected_colors_2
            color_list[idx]["rgb_label"].configure(text=f"RGB: {color}")
            color_list[idx]["color_box"].configure(bg=hex_color)
            self.update_palette(set_number)

    def create_palette_widgets(self, set_number, offset):
        palette_frame = customtkinter.CTkFrame(self.main_frame)
        palette_frame.grid(row=12, column=offset, columnspan=4, padx=20, pady=10, sticky="ew")
        palette_label = customtkinter.CTkLabel(palette_frame, text=f"Set {set_number} Selected Colors Palette", font=self.palette_font)
        palette_label.pack(padx=11, pady=10)

        palette_box = customtkinter.CTkFrame(palette_frame, fg_color=self.color_scheme["palette_box_bg"])  # Lighter grey background for the palette box
        palette_box.pack(fill="both", expand=True, padx=10, pady=10)

        palette_colors = [customtkinter.CTkCanvas(palette_box, width=100, height=100, bg=self.color_scheme["color_box_bg"]) for _ in range(5)]
        for color_box in palette_colors:
            color_box.pack(side=tk.LEFT, padx=5, pady=5)
        if set_number == 1:
            self.palette_colors_1 = palette_colors
        else:
            self.palette_colors_2 = palette_colors

    def update_palette(self, set_number):
        color_list = self.selected_colors_1 if set_number == 1 else self.selected_colors_2
        palette_colors = self.palette_colors_1 if set_number == 1 else self.palette_colors_2
        for i, color_box in enumerate(palette_colors):
            color = color_list[i]["color_box"].cget("bg")
            color_box.configure(bg=color)

    def show_color_popup(self, idx, set_number):
        color_list = self.selected_colors_1 if set_number == 1 else self.selected_colors_2
        color_text = color_list[idx]["rgb_label"].cget("text").split(' ', 1)[1]
        if not color_text.strip():
            return  # Do nothing if color is not set

        color = eval(color_text)
        rgb_text = format_color_values("RGB", color)
        hex_color = rgb_to_hex(color)
        hex_text = format_color_values("HEX", hex_color)
        cmyk_text = format_color_values("CMYK", rgb_to_cmyk(color))
        hsl_text = format_color_values("HSL", rgb_to_hsl(color))
        hsv_text = format_color_values("HSV", rgb_to_hsv(color))

        if self.popup:
            self.popup.destroy()

        self.popup = customtkinter.CTkFrame(self, width=300, height=200)
        self.popup.place(relx=0.5, rely=0.7, anchor="center")

        # Color Details Title
        popup_title = customtkinter.CTkLabel(self.popup, text="Color Details", font=("Arial", 14, 'bold'), text_color=self.color_scheme["label_text"])
        popup_title.pack(pady=(10, 5))

        color_box = customtkinter.CTkFrame(self.popup, width=150, height=50, fg_color=hex_color)
        color_box.pack(padx=10, pady=5)

        for text in [rgb_text, hex_text, cmyk_text, hsl_text, hsv_text]:
            label = customtkinter.CTkLabel(self.popup, text=text, font=("Arial", 12))
            label.pack(pady=2, padx=5)
            label.bind("<Button-1>", lambda event, value=text.split(' ', 1)[1]: ClipboardUtils.copy_to_clipboard(self.popup, value))

        
    def display_saved_colors(self):
        # Remove the button from the screen
        self.display_saved_button.pack_forget()

        # Read colors from the CSV file
        saved_colors = read_saved_colors_from_csv()

        # Display the saved colors
        self.display_saved_color_list(saved_colors)

    def display_saved_color_list(self, colors):
        if self.saved_colors_container is not None and self.saved_colors_container.winfo_exists():
            self.saved_colors_container.pack_forget()
            self.import_colors_button.pack_forget()

        self.saved_colors_container = customtkinter.CTkScrollableFrame(self.side_frame, label_text="Saved Colors", label_anchor="n", height=100, width=200)
        self.saved_colors_container.pack(padx=20, pady=10)
        display_colors(self, self.saved_colors_container, colors, color_gear_element=True)
        self.import_colors_button = customtkinter.CTkButton(self.side_frame, text="Import to Palette 1", command=self.import_selected_colors, font=("Segoe UI", 12))
        self.import_colors_button.pack(padx=20, pady=10)

    def limit_selection(self, check_var, check_vars):
        if sum(var.get() for var in check_vars) > 5:
            check_var.set(0)  # Reset the last checked box
            if self.confirmation_label is not None and self.confirmation_label.winfo_exists:
                self.confirmation_label.pack_forget()
            self.confirmation_label = customtkinter.CTkLabel(self.side_frame, text="You can select up to 5 colors only.")
            self.confirmation_label.pack(padx=20, pady=10)
            self.after(2000, self.confirmation_label.destroy)  # Remove the pop-up frame after 2 second

    def import_selected_colors(self):
        # Fetch all selected colors
        selected_colors = [color for var, color in zip(self.check_vars, read_saved_colors_from_csv()) if var.get()]

        # If there are no colors selected, abort
        if not selected_colors:
            return
         # Deselect all checkboxes
        for var in self.check_vars:
            var.set(0)  # Reset each checkbox variable to its off value

        # Update the colors in the first palette set
        for idx, color_info in enumerate(self.selected_colors_1):
            if idx < len(selected_colors):
                color = selected_colors[idx]
                rgb_color = hex_to_rgb(color)
                color_info["rgb_label"].configure(text=f"RGB: {rgb_color}")  # Update the RGB label text
                color_info["color_box"].configure(bg=color)  # Update the color box background
            else:
                # Clear any remaining slots if fewer than 5 colors are selected
                color_info["rgb_label"].configure(text="RGB: ")
                color_info["color_box"].configure(bg=self.color_scheme["color_box_bg"])  # Default/no color

        # Refresh the display to reflect the new colors
        self.update_palette(1)

