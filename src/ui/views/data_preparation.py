import customtkinter as ctk

class DataPreparation(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#1E1E1E")
        
        label = ctk.CTkLabel(self, text="Data Preparation")
        label.pack(pady=20)

