import customtkinter as ctk
from .components.sidebar import Sidebar

class MainWindow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill="both", expand=True)

        self.sidebar = Sidebar(self, self.switch_frame)
        self.sidebar.place(relx=0, rely=0, relwidth=0.2, relheight=1.0)

        self.container = ctk.CTkFrame(self)
        self.container.place(relx=0.2, rely=0, relwidth=0.8, relheight=1.0)

        self.current_frame = None

    def switch_frame(self, index):
        self.sidebar.enable_next_step(self)
        print(f"Switching to step {index + 1}: {self.sidebar.steps[index]}")