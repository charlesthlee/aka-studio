import customtkinter as ctk
import tkinter as tk
import webbrowser

class TutorialsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Application title
        self.label = ctk.CTkLabel(self, text="Tutorials", font=("Segoe UI", 24, "bold"))
        self.label.pack(pady=20)

        # Container frame for links
        self.links_frame = ctk.CTkFrame(self, width=400, height=300)
        self.links_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Links information
        links_info = [
            ("NASA Color Usage", "https://colorusage.arc.nasa.gov/index.php", 
             "Explore NASA's guidelines and research on effective color usage in data visualizations."),
            ("Harvard Lecture on Color", "https://scholar.harvard.edu/files/schwartz/files/lecture17-color.pdf", 
             "Read a detailed Harvard lecture on the science and perception of color."),
            ("Britannica - Science of Color", "https://www.britannica.com/science/color", 
             "Learn about the science of color and its applications from Britannica.")
        ]

        # Adding links as CTkLabels
        for i, (title, url, desc) in enumerate(links_info):
            title_label = ctk.CTkLabel(self.links_frame, text=title, cursor="hand2", font=("Segoe UI", 18, "bold"), text_color="#99c3ff")
            title_label.pack(padx=5, pady=(10, 2), anchor="w")
            title_label.bind("<Button-1>", lambda e, link=url, label=title_label: (self.open_url(link), label.configure(text_color="#c58af9")))
            title_label.bind("<Enter>", lambda e, label=title_label: label.configure(font=("Segoe UI", 18, "bold", "underline")))
            title_label.bind("<Leave>", lambda e, label=title_label: label.configure(font=("Segoe UI", 18, "bold")))
            desc_label = ctk.CTkLabel(self.links_frame, text=desc, font=("Segoe UI", 14))
            desc_label.pack(padx=5, pady=(2, 10), anchor="w")

        # Button to navigate to Home page
        self.home_button = ctk.CTkButton(self, text="Go to Home", command=self.parent.open_home_page)
        self.home_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        self.focus()
    
    def open_url(self, url):
        webbrowser.open(url)
