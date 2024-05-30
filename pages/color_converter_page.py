import tkinter as tk
import customtkinter
from config.utils import ClipboardUtils, rgb_to_hex, hex_to_rgb, rgb_to_cmyk, cmyk_to_rgb, rgb_to_hsl, hsl_to_rgb, rgb_to_hsv, hsv_to_rgb, format_color_values

class ColorConverterPage(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.rgb_values = [0, 0, 0]  # Initialize RGB values
        self.hex_value = ""  # Initialize HEX value
        self.cmyk_values = [0, 0, 0, 0]  # Initialize CMYK values
        self.hsl_values = [0, 0, 0]  # Initialize HSL values
        self.hsv_values = [0, 0, 0]  # Initialize HSV values
        
        # Label for the page title
        label = customtkinter.CTkLabel(self, text="Color Converter Page", font=("Segoe UI", 24, "bold"))
        label.pack(pady=10, padx=10)

        self.error_container = None
        self.output_container = None

        self.button_styles = {
            'border_spacing' : 5,
            'hover': True,
        }
        # Button Container for Color Type Selection
        self.button_container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_container.pack(pady=20)

        self.color_types = ["RGB", "HEX", "CMYK", "HSL", "HSV"]
        self.selected_color_type = customtkinter.StringVar(value=self.color_types[0])

        # Define color schemes for light and dark modes
        self.light_mode_colors = {
            "fg_color": "white",
            "hover_color": "lightgray",
            "selected_border_width": 3,
            "normal_border_width": 1,
            "text_color": "black",
            "bg_color": "white"
        }
        self.dark_mode_colors = {
            "fg_color": "#232323",
            "hover_color": "#404040",
            "selected_border_width": 3,
            "normal_border_width": 1,
            "text_color": "white",
            "bg_color": "#252525"
        }

        # Select appropriate color scheme based on current appearance mode
        self.color_scheme = self.dark_mode_colors if self.parent.appearance_mode == "dark" else self.light_mode_colors

        self.configure(fg_color=self.color_scheme["bg_color"])
        # Create buttons for each color type
        self.buttons = {}
        for color_type in self.color_types:
            button = customtkinter.CTkButton(
                self.button_container,
                text=color_type,
                command=lambda ct=color_type: self.select_color_type(ct),
                width=75,
                height=75,
                corner_radius=10,
                fg_color=self.color_scheme["fg_color"],
                text_color=self.color_scheme["text_color"],
                hover_color=self.color_scheme["hover_color"],
                border_width=self.color_scheme["normal_border_width"],
                font=("Segoe UI", 12)  # Normal text style
            )
            button.pack(side="left", padx=5)
            self.buttons[color_type] = button

        # Highlight the default selected button
        self.update_button_styles(self.selected_color_type.get())
        self.input_container = customtkinter.CTkFrame(master=self, width=300, height=300, fg_color="transparent")
        self.input_container.pack(pady=20, padx=10)
        
        # Button to trigger conversion
        self.convert_button = customtkinter.CTkButton(self, text="Convert", command=self.convert_values, **self.button_styles)
        self.convert_button.pack(pady=20, padx=10)

        # Button to navigate to Home page
        self.home_button = customtkinter.CTkButton(self, text="Go to Home", command=self.parent.open_home_page, **self.button_styles)
        self.home_button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
        
        # Update input fields based on the selected color type
        self.update_inputs()

    def select_color_type(self, color_type):
        self.selected_color_type.set(color_type)
        self.update_button_styles(color_type)
        self.update_inputs()

    def update_button_styles(self, selected_color_type):
        self.color_scheme = self.dark_mode_colors if self.parent.appearance_mode.lower() == "dark" else self.light_mode_colors
        for color_type, button in self.buttons.items():
            if color_type == selected_color_type:
                button.configure(
                    border_width=self.color_scheme["selected_border_width"],
                    font=("Segoe UI", 12, "bold")  # Bold text for selected button
                )
            else:
                button.configure(
                    border_width=self.color_scheme["normal_border_width"],
                    font=("Segoe UI", 12)  # Normal text style
                )

    def create_label_and_entry(self, container, label_text):
        label = customtkinter.CTkLabel(container, text=label_text)
        label.pack(side="left")
        entry = customtkinter.CTkEntry(container)
        entry.pack(side="left", padx=10, pady=10)
        return entry
    
    def update_inputs(self, *args):
        # Clear existing input fields
        for widget in self.input_container.winfo_children():
            widget.destroy()
        
        # Add input fields based on the selected color type
        color_type = self.selected_color_type.get()
        if color_type == "RGB":
            self.add_rgb_inputs()
        elif color_type == "HEX":
            self.add_hex_input()
        elif color_type == "CMYK":
            self.add_cmyk_inputs()
        elif color_type == "HSL":
            self.add_hsl_inputs()
        elif color_type == "HSV":
            self.add_hsv_inputs()

    def add_hex_input(self):
        # Add 1 input field for HEX value
        self.hex_entry = self.create_label_and_entry(self.input_container, "HEX: ")
    
    def add_rgb_inputs(self):
        # Add 3 input fields for RGB values
        self.rgb_entries = []
        for label_text in ["R:", "G:", "B:"]:
            entry = self.create_label_and_entry(self.input_container, label_text)
            self.rgb_entries.append(entry)
    
    def add_cmyk_inputs(self):
        # Add 4 input fields for CMYK values
        self.cmyk_entries = []
        for label_text in ["C:", "M:", "Y:", "K:"]:
            entry = self.create_label_and_entry(self.input_container, label_text)
            self.cmyk_entries.append(entry)
    
    def add_hsl_inputs(self):
        # Add 3 input fields for HSL values
        self.hsl_entries = []
        for label_text in ["H:", "S:", "L:"]:
            entry = self.create_label_and_entry(self.input_container, label_text)
            self.hsl_entries.append(entry)
    
    def add_hsv_inputs(self):
        # Add 3 input fields for HSV values
        self.hsv_entries = []
        for label_text in ["H:", "S:", "V:"]:
            entry = self.create_label_and_entry(self.input_container, label_text)
            self.hsv_entries.append(entry)

    def update_rgb_values(self):
        self.rgb_values = [self.validate_input(entry.get(), 0, 255) for entry in self.rgb_entries]

    def update_cmyk_values(self):
        self.cmyk_values = [self.validate_input(entry.get(), 0, 100) for entry in self.cmyk_entries]

    def update_hsl_values(self):
        self.hsl_values = [self.validate_input(entry.get(), 0, 360) if i == 0 else self.validate_input(entry.get(), 0, 100) for i, entry in enumerate(self.hsl_entries)]

    def update_hsv_values(self):
        self.hsv_values = [self.validate_input(entry.get(), 0, 360) if i == 0 else self.validate_input(entry.get(), 0, 100) for i, entry in enumerate(self.hsv_entries)]

    def validate_input(self, value, min_value, max_value):
        try:
            int_value = int(value)
            if min_value <= int_value <= max_value:
                return int_value
            else:
                # Value out of range, show error message
                self.destroy_error_container()
                self.display_error_message(f"VALUE ENTERED MUST BE BETWEEN {min_value} AND {max_value}")
                return None
        except ValueError:
            # Invalid input, show error message
            self.destroy_error_container()
            self.display_error_message("INVALID INPUT")
            return None

    def is_valid_hex(self, hex_value):
        try:
            int(hex_value, 16)
            return len(hex_value) == 6
        except ValueError:
            return False

    def convert_values(self):
        if self.error_container is not None: 
            self.destroy_error_container()

        color_type = self.selected_color_type.get()
        if color_type == "RGB":
            self.update_rgb_values()
            if None in self.rgb_values:
                return
            self.convert_rgb_to_other_formats()
        elif color_type == "HEX":
            hex_value = self.hex_entry.get()
            # Check if the Hex Value entered contains a '#' at the beginning
            if hex_value.startswith('#'):
                hex_value = hex_value[1:]  # Remove the leading '#'
            if not self.is_valid_hex(hex_value):
                self.display_error_message("INVALID HEX VALUE")
                return
            self.hex_value = '#' + hex_value
            self.convert_hex_to_other_formats()
        elif color_type == "CMYK":
            self.update_cmyk_values()
            if None in self.cmyk_values:
                return
            self.convert_cmyk_to_other_formats()
        elif color_type == "HSL":
            self.update_hsl_values()
            if None in self.hsl_values:
                return
            self.convert_hsl_to_other_formats()
        elif color_type == "HSV":
            self.update_hsv_values()
            if None in self.hsv_values:
                return
            self.convert_hsv_to_other_formats()

        self.display_converted_values()

    def display_error_message(self, message):
        if self.output_container is not None: 
            self.destroy_output_container()
        self.error_container = customtkinter.CTkFrame(self, height=100, width=100)
        self.error_container.pack(pady=20, padx=10)
        self.error_label = customtkinter.CTkLabel(self.error_container, text=message, font=("Impact", 20), text_color="RED")
        self.error_label.pack(expand=True, fill="both", padx=25, pady=15)

        # After 3 seconds, error message is removed
        self.after(3000, self.error_container.destroy)

    def destroy_output_container(self):
        if self.output_container is not None and self.output_container.winfo_exists():
            self.output_container.pack_forget()

    def destroy_error_container(self):
        if self.error_container is not None and self.error_container.winfo_exists():  # Check if the error label still exists
            self.error_container.pack_forget()

    def convert_rgb_to_other_formats(self):
        self.hex_value = rgb_to_hex(self.rgb_values) # Convert RGB to HEX
        self.cmyk_values = rgb_to_cmyk(self.rgb_values) # Convert RGB to CMYK
        self.hsl_values = rgb_to_hsl(self.rgb_values) # Convert RGB to HSL
        self.hsv_values = rgb_to_hsv(self.rgb_values) # Convert RGB to HSV

    def convert_hex_to_other_formats(self):
        self.rgb_values = hex_to_rgb(self.hex_value) # Convert HEX to RGB
        self.cmyk_values = rgb_to_cmyk(self.rgb_values) # Convert RGB to CMYK  
        self.hsl_values = rgb_to_hsl(self.rgb_values) # Convert RGB to HSL
        self.hsv_values = rgb_to_hsv(self.rgb_values) # Convert RGB to HSV
 
    def convert_cmyk_to_other_formats(self):
        self.rgb_values = cmyk_to_rgb(self.cmyk_values) # Convert CMYK to RGB
        self.hex_value = rgb_to_hex(self.rgb_values) # Convert RGB to HEX
        self.hsl_values = rgb_to_hsl(self.rgb_values) # Convert RGB to HSL
        self.hsv_values = rgb_to_hsv(self.rgb_values) # Convert RGB to HSV

    def convert_hsl_to_other_formats(self):
        self.rgb_values = hsl_to_rgb(self.hsl_values) # Convert HSL to RGB
        self.hex_value = rgb_to_hex(self.rgb_values) # Convert RGB to HEX
        self.cmyk_values = rgb_to_cmyk(self.rgb_values) # Convert RGB to CMYK
        self.hsv_values = rgb_to_hsv(self.rgb_values) # Convert RGB to HSV

    def convert_hsv_to_other_formats(self):
        self.rgb_values = hsv_to_rgb(self.hsv_values) # Convert HSV to RGB
        self.hex_value = rgb_to_hex(self.rgb_values) # Convert RGB to HEX
        self.cmyk_values = rgb_to_cmyk(self.rgb_values) # Convert RGB to CMYK
        self.hsl_values = rgb_to_hsl(self.rgb_values) # Convert RGB to HSL

    def display_converted_values(self):
        # Clear existing value labels
        for widget in self.input_container.winfo_children():
            if isinstance(widget, customtkinter.CTkLabel):
                widget.destroy()
        
        if self.output_container is not None: self.output_container.destroy()
        self.output_container = customtkinter.CTkFrame(master=self, width=300, height=300)
        self.output_container.pack(pady=20, padx=10)

        color_box = customtkinter.CTkFrame(self.output_container, width = 150, height = 50, fg_color=self.hex_value, border_color="grey")
        color_box.pack(padx=10, pady=5)

        # Iterate over color types and display converted values
        for color_type in self.color_types:
            if color_type == self.selected_color_type.get():
                continue  # Skip the selected color type
            
            converted_values = self.get_converted_values(color_type)
            label_text = format_color_values(color_type, converted_values)
            label = customtkinter.CTkLabel(self.output_container, text=label_text)
            label.pack(padx=10, pady=10)

            # Add copy to clipboard functionality to each label
            stripped_label = label_text.split(' ', 1)[1]
            label.bind("<Button-1>", lambda event, value=stripped_label: ClipboardUtils.copy_to_clipboard(self.output_container, value))

    def get_converted_values(self, color_type):
        if color_type == "RGB":
            return self.rgb_values
        elif color_type == "HEX":
            return self.hex_value
        elif color_type == "CMYK":
            return self.cmyk_values
        elif color_type == "HSL":
            return self.hsl_values
        elif color_type == "HSV":
            return self.hsv_values