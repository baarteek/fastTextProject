import customtkinter as ctk

class MainWindow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(master=self, text="Hello", font=("Arial", 20), text_color="#ffcc70")
        self.label.place(relx=0.5, rely=0.5, anchor="center")