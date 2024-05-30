import customtkinter as ctk
from customtkinter import CTkFrame, CTkCanvas, CTkLabel, CTkButton, CTkInputDialog, CTkScrollableFrame
import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog,messagebox
import numpy as np
from sklearn.cluster import KMeans
from config.utils import ClipboardUtils, CTkSpinbox, rgb_to_cmyk, rgb_to_hex, rgb_to_hsl, rgb_to_hsv, format_color_values, display_colors, read_saved_colors_from_csv
from colorthief import ColorThief
import csv
import atexit
import os

class ColorGrabPage(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.selected_colors = []  # List to store selected colors

        # Create a canvas to display the video feed and uploaded image
        self.canvas = CTkCanvas(self, width=640, height=470, cursor="tcross")
        self.canvas.pack(pady=10, padx=5)

        # Create a frame to hold color information
        color_info_frame = CTkFrame(self)
        color_info_frame.pack(pady=5)

        # Create labels to display color information
        self.color_label = CTkLabel(color_info_frame, text="Click on the canvas to grab color", font=("Segoe UI", 14, "bold"), fg_color="transparent")
        self.color_label.pack()

        # Bind mouse click event to canvas
        self.canvas.bind("<Button-1>", self.get_color)

        # Create a frame to hold control buttons
        control_frame = CTkFrame(self, fg_color="transparent")
        control_frame.pack(pady=5)

        self.color_label_container = CTkScrollableFrame(self, label_text="Selected Colors", label_anchor="n", height=160 ,width= 1000, orientation="horizontal")
        self.color_label_container.place(relx=0.5, rely=0.825, anchor="center")
        # Button to navigate to Home page
        self.home_button = CTkButton(control_frame, text="Go to Home", command=self.parent.open_home_page, font=("Segoe UI", 12))
        self.home_button.pack(side="left", padx=5)
        # Button to start capturing video or display the uploaded image
        self.start_button = CTkButton(control_frame, text="Start Camera", command=self.start_camera, font=("Segoe UI", 12))
        self.start_button.pack(side="left", padx=5)

        # Capture video flag
        self.capture_video_flag = False

        # Button to upload image
        self.upload_button = CTkButton(control_frame, text="Upload Image", command=self.upload_image, font=("Segoe UI", 12))
        self.upload_button.pack(side="left", padx=5)    

        self.display_saved_button = CTkButton(control_frame, text="Display Saved Colors", command=self.display_saved_colors, font=("Segoe UI", 12))
        self.display_saved_button.pack(side="left", padx=5)

        self.max_colors = 5

        # Button to extract dominant colors
        self.extract_colors_button = CTkButton(control_frame, text="Extract Palette", command=self.extract_dominant_colors, font=("Segoe UI", 12))
        self.extract_colors_button.pack(side="left", padx=5)

        # Slider to adjust the number of dominant colors
        self.color_spinbox = CTkSpinbox(control_frame, width=5, step_size=1)
        self.color_spinbox.pack(side="left", padx=5)

        self.palette_container = None
        self.saved_colors_container = None

        atexit.register(self.cleanup)

    def get_color(self, event):
        x, y = event.x, event.y
        # Get the color at the clicked point
        color = self.get_pixel_color(x, y)
        if color is not None:
            # Convert color to tuple for comparison
            color_tuple = tuple(color)
            # Check if the color already exists in selected_colors list
            if color_tuple not in map(tuple, self.selected_colors):
                self.selected_colors.append(color)
                # Update the color label with the color information
                self.color_label.configure(text=f"The color at ({x}, {y}) is ")
                # Calculate and display other color representations
                rgb = color
                self.save_selected_color(color)
                hex_color = rgb_to_hex(rgb)
                cmyk = rgb_to_cmyk(rgb)
                hsl = rgb_to_hsl(rgb)
                hsv = rgb_to_hsv(rgb)

                # Format the color values
                formatted_rgb = format_color_values("RGB", rgb)
                formatted_hex_color = format_color_values("HEX", hex_color)
                formatted_cmyk = format_color_values("CMYK", cmyk)
                formatted_hsl = format_color_values("HSL", hsl)
                formatted_hsv = format_color_values("HSV", hsv)

                # Display the selected colors
                self.display_selected_colors()

    def cleanup_saved_colors_csv(self):
        # Get the directory path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the saved colors CSV file
        csv_path = os.path.join(current_directory, "..", "config", "saved_colors.csv")

        # Truncate the contents of the CSV file
        with open(csv_path, mode='w', newline='') as file:
            file.truncate()
            
    def upload_image(self):
        # Stop the camera if it's currently running
        self.stop_camera()
        
        # Open file dialog for image selection
        self.file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if self.file_path:
            # Load the selected image
            image = Image.open(self.file_path)
            if image is not None:
                # Convert the image to numpy array
                image_np = np.array(image)  # This is image_np
                # Set the uploaded image attribute
                self.uploaded_image = image_np
                # Display the image on the canvas
                self.display_image(image_np)
                # Change button text and command
                self.start_button.configure(text="Start Camera", command=self.start_camera)

    def display_image(self, image):
        # Resize the image to fit the canvas
        image_resized = cv2.resize(image, (640, 470))
        # Convert the image to a format suitable for displaying in a Tkinter Canvas
        img = Image.fromarray(image_resized)
        img = ImageTk.PhotoImage(image=img)
        # Update the canvas with the new image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        # Hold a reference to the image to prevent it from being garbage collected
        self.canvas.img = img


    def display_color_block_label(self, color):
        # Convert RGB color to hexadecimal
        hex_color = rgb_to_hex(color)

        # Create a frame to display the color block
        color_block_frame = CTkFrame(self, width=50, height=50)
        color_block_frame.pack(side="left", padx=5)  # Adjust padding as needed
        color_block_frame.configure(bg=hex_color)


    def get_pixel_color(self, x, y):
        if hasattr(self, 'uploaded_image') and not self.capture_video_flag:
            # Get dimensions of the uploaded image and canvas
            image_height, image_width, _ = self.uploaded_image.shape
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # Calculate scale factors
            x_scale = image_width / canvas_width
            y_scale = image_height / canvas_height

            # Map canvas coordinates to image coordinates
            x_image = int(x * x_scale)
            y_image = int(y * y_scale)

            # Ensure coordinates are within image bounds
            if 0 <= x_image < image_width and 0 <= y_image < image_height:
                color = self.uploaded_image[y_image, x_image]
                color_type = self.detect_color_type(self.uploaded_image)
                if color_type != 'RGB':
                    color = self.convert_to_rgb(color, color_type)
                return color
                
        elif hasattr(self, 'cap') and self.capture_video_flag:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_height, frame_width, _ = frame_rgb.shape

                # Calculate scale factors
                x_scale = frame_width / self.canvas.winfo_width()
                y_scale = frame_height / self.canvas.winfo_height()

                # Map canvas coordinates to frame coordinates
                x_image = int(x * x_scale)
                y_image = int(y * y_scale)

                # Ensure coordinates are within frame bounds
                if 0 <= x_image < frame_width and 0 <= y_image < frame_height:
                    color = frame_rgb[y_image, x_image]
                    return color
                            
        return None

    
    def save_selected_color(self, color):
        # Convert RGB values to hexadecimal format
        hex_color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])

        # Get the directory path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the CSV file
        csv_path = os.path.join(current_directory, "..", "config", "selected_colors.csv")

        # Write color to CSV file
        with open(csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([hex_color])

    def read_selected_colors_from_csv(self):
        # Get the directory path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the settings file in the config directory
        csv_path = os.path.join(current_directory, "..", "config", "selected_colors.csv")
        # Read colors from CSV file
        colors = []
        try:
            with open(csv_path, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    colors.append(row[0])  # Assuming the color values are stored in the first column
        except FileNotFoundError:
            # Handle the case where the file is not found
            print("Error: selected_colors.csv file not found!")
        
        return colors

    def display_selected_colors(self):
        # Clear the previous display
        if self.color_label_container is not None and self.color_label_container.winfo_exists():
            self.color_label_container.destroy()

        # Create a new container for the selected colors
        self.color_label_container = CTkScrollableFrame(self, label_text="Selected Colors", label_anchor="n", height=170, width=1000, orientation="horizontal")
        self.color_label_container.place(relx=0.5, rely=0.825, anchor="center")

        # Display the selected colors horizontally
        for color in self.selected_colors:
            # Calculate other color representations
            rgb = color
            hex_color = rgb_to_hex(rgb)
            cmyk = rgb_to_cmyk(rgb)
            hsl = rgb_to_hsl(rgb)
            hsv = rgb_to_hsv(rgb)

            # Format the color values
            formatted_rgb = format_color_values("RGB", rgb)
            formatted_hex_color = format_color_values("HEX", hex_color)
            formatted_cmyk = format_color_values("CMYK", cmyk)
            formatted_hsl = format_color_values("HSL", hsl)
            formatted_hsv = format_color_values("HSV", hsv)

            # Create and display the ColorBlockLabel widget
            color_block_label = ColorBlockLabel(self.color_label_container, self, color, formatted_rgb, formatted_hex_color, formatted_cmyk, formatted_hsl, formatted_hsv)
            color_block_label.pack(side="left", padx=10)  # Adjust padding as needed

        # Display the count of selected colors
        count_label = CTkLabel(self, text=f"Total Selected: {len(self.selected_colors)}", font=("Segoe UI", 12))
        count_label.place(relx=0.5, rely=0.665, anchor="center")



    def display_selected_color_list(self, colors):
        self.color_label_container = CTkScrollableFrame(self, label_text="Selected Colors", label_anchor="n", height=150 ,width= 1000, orientation="horizontal")
        self.color_label_container.place(relx=0.5, rely=0.825, anchor="center")
        display_colors(self, self.color_label_container, colors)

    def detect_color_type(self, image):
        # Determine color type based on the shape of the image array
        if len(image.shape) == 2:
            return 'Grayscale'
        elif len(image.shape) == 3:
            if image.shape[2] == 1:
                return 'Grayscale'
            elif image.shape[2] == 3:
                return 'RGB'
            elif image.shape[2] == 4:
                return 'RGBA'  # Assuming the image has an alpha channel
        return 'Unknown'  # If shape doesn't match any known color type

    def convert_to_rgb(self, color, color_type):
        # Convert color to RGB format [R, G, B]
        if color_type == 'Grayscale':
            # Grayscale to RGB
            return [color, color, color]
        elif color_type == 'RGBA':
            # RGBA to RGB (ignoring alpha channel)
            return color[:3]
        # Add more conversion rules as needed for other color types
        return color  # Return as is if already RGB

    def start_camera(self):
        if not self.capture_video_flag:
            # Start capturing video
            self.capture_video_flag = True
            self.initialize_camera()
            self.capture_video()
            # Change button text and command
            self.start_button.configure(text="Stop Camera", command=self.stop_camera)
        else:
            # Stop capturing video
            self.stop_camera()
            # Change button text and command
            self.start_button.configure(text="Start Camera", command=self.start_camera)


    def stop_camera(self):
        if self.capture_video_flag:
            # Stop capturing video
            self.capture_video_flag = False
            self.release_camera()
            # Change button text and command
            self.start_button.configure(text="Start Camera", command=self.start_camera)


    def show_uploaded_image(self):
        if hasattr(self, 'uploaded_image'):
            # Display the uploaded image
            self.display_image(self.uploaded_image)
            # Change button text and command
            self.start_button.configure(text="Start Camera", command=self.start_camera)

    def initialize_camera(self):
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        # Check if the camera opened successfully
        if not self.cap.isOpened():
            print("Error: Failed to open camera.")
            return
        # Set the camera frame width and height
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def capture_video(self):
        if self.capture_video_flag:
            # Read video frame
            ret, frame = self.cap.read()
            if ret:
                # Convert frame to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Display the frame on the canvas
                self.display_image(frame_rgb)
                # Schedule the next frame capture
                self.after(10, self.capture_video)

    def release_camera(self):
        # Release the camera
        if hasattr(self, 'cap'):
            self.cap.release()

    def cleanup(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_directory, "..", "config", "selected_colors.csv")
        with open(csv_path, mode='w', newline='') as file:
            file.truncate()
        self.release_camera()
    

    # DEVANSH
    
    
    def display_saved_colors(self):
        # Read colors from the CSV file
        saved_colors = read_saved_colors_from_csv()

        if self.saved_colors_container is not None and self.saved_colors_container.winfo_exists():
            self.saved_colors_container.place_forget()

        self.display_saved_color_list(saved_colors)


    def display_saved_color_list(self, colors):
        self.saved_colors_container = CTkScrollableFrame(self, label_text="Saved Colors", label_anchor="n", height=100, width=150)
        self.saved_colors_container.place(relx=0.79, rely=0.125)
        display_colors(self, self.saved_colors_container, colors)


    def extract_dominant_colors(self):
        # Check if an image is uploaded
        if hasattr(self, 'uploaded_image'):
            dominant_count = int(self.color_spinbox.get())

            if dominant_count > 10:
                return

            if self.palette_container is not None and self.palette_container.winfo_exists(): 
                self.palette_container.destroy()

            # Get the dominant colors from the uploaded image
            dominant_colors = self.get_dominant_colors(self.file_path, dominant_count)

            # Display the dominant colors on the GUI
            self.display_dominant_colors(dominant_colors, dominant_count)
        
    def get_dominant_colors(self, image, num_colors):
        ct = ColorThief(image)
        if num_colors == 1:
            palette = [ct.get_color(quality=1)]
        else:
            palette = ct.get_palette(color_count=11, quality=5)
        return palette

    def display_dominant_colors(self, dominant_colors, dominant_count):
        self.palette_container = CTkFrame(self, height=100, width=100)
        self.palette_container.place(relx=0.165, rely=0.25, anchor=tk.CENTER)

        header = CTkLabel(self.palette_container, text="Extracted Palette", font=("Segoe UI", 15))
        header.grid(row=0, columnspan=dominant_count, pady=(10, 10))  # Place at row 0 and span all columns
        header.grid_columnconfigure(0, weight=1)  # Center the label horizontally

        for i, color in enumerate(dominant_colors):
            if i >= dominant_count:
                break  # Stop the loop if the number of displayed colors reaches dominant_count

            # Convert RGB to HEX
            hex_color = "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

            if i < 5:
                row_number = 1
            else:
                row_number = 3

            # Create a canvas to display the color block
            color_canvas = CTkCanvas(self.palette_container, width=50, height=50, bg=hex_color)
            color_canvas.grid(row=row_number, column=i%5, padx=3, pady=5)

            # Create label to display hex color value
            hex_label = CTkLabel(self.palette_container, text=hex_color.upper(), font=("Segoe UI", 12))
            hex_label.grid(row=row_number+1, column=i%5, padx=3, pady=3)
            hex_label.bind("<Button-1>", lambda event, value=hex_color: ClipboardUtils.copy_to_clipboard(self, value))



    # DEVANSH



from tkinter import Canvas
import os

class ColorBlockLabel(CTkFrame):
    def __init__(self, master, main_frame, color, formatted_rgb, formatted_hex_color, formatted_cmyk, formatted_hsl, formatted_hsv, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.color = color
        self.master = master
        self.main_frame = main_frame
        self.formatted_rgb = formatted_rgb
        self.formatted_hex_color = formatted_hex_color
        self.formatted_cmyk = formatted_cmyk
        self.formatted_hsl = formatted_hsl
        self.formatted_hsv = formatted_hsv

        # Display color block and labels using pack
        self.display_color_block()
        self.display_labels(color)

    def display_color_block(self):
        # Convert RGB color to hexadecimal
        hex_color = rgb_to_hex(self.color)

        # Create a canvas to draw the color block
        canvas = Canvas(self, width=50, height=50, bg="white")
        canvas.pack(side="left", padx=5, pady=5)

        # Draw a rectangle with the color
        canvas.create_rectangle(5, 5, 45, 45, fill=hex_color, outline="")

    def display_labels(self, color):
        labels_info = [
            ("RGB", self.formatted_rgb),
            ("HEX", self.formatted_hex_color),
            ("CMYK", self.formatted_cmyk),
            ("HSL", self.formatted_hsl),
            ("HSV", self.formatted_hsv)
        ]

        for info in labels_info:
            label = CTkLabel(self, text=info[1], font=("Segoe UI", 12))
            label.bind("<Button-1>", lambda event, value=info[1].split(' ', 1)[1]: ClipboardUtils.copy_to_clipboard(self, value))
            label.pack()

        # Add a "Save" button for the color
        save_button = CTkButton(self, text="Save", command=lambda: self.save_color(color))
        save_button.pack()
    
    def save_color(self, color):
        # Get the directory path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_directory, "..", "config", "saved_colors.csv")

        # Check if the CSV file exists
        if not os.path.exists(csv_path):
            with open(csv_path, mode='w', newline='') as file:
                pass  # File created, so nothing to write initially

        # Read existing colors from CSV
        existing_colors = []
        if os.path.exists(csv_path):
            with open(csv_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                existing_colors = [row[0] for row in reader]

        color_hex = rgb_to_hex(color) if "#" not in color else color
        # Write color to CSV file only if it is not a duplicate
        if color_hex not in existing_colors:
            with open(csv_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([color_hex])
            
        # Refresh the color display if the color container is active and exists
        if self.main_frame.saved_colors_container is not None and self.main_frame.saved_colors_container.winfo_exists():
            self.main_frame.display_saved_colors()