import customtkinter as ctk

class ModelTraining(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#1E1E1E")

        label = ctk.CTkLabel(self, text="Model Training")
        label.pack(pady=20)
