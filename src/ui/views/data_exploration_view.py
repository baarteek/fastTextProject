import customtkinter as ctk

class DataExplorationView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#1E1E1E", **kwargs)
        label = ctk.CTkLabel(self, text="Data Exploration View")
        label.pack(pady=20, padx=20)