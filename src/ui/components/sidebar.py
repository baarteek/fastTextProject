import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, callback, steps, **kwargs):
        super().__init__(master, fg_color="#2b2b2b", **kwargs)
        self.callback = callback
        self.steps = steps
        self.labels = []
        self.current_index = 0
        self.create_sidebar()

    def create_sidebar(self):
        title_label = ctk.CTkLabel(self, text="fastText Project", font=("Arial", 16, "bold"), text_color="white")
        title_label.pack(pady=(10, 20))

        for step in self.steps:
            lbl = ctk.CTkLabel(self, text=step, font=("Arial", 12, "bold"), text_color="#555555", fg_color="#2b2b2b", corner_radius=10)
            lbl.pack(fill='both', pady=5, padx=15)
            self.labels.append(lbl)

        settings_btn = ctk.CTkButton(self, text="Settings", fg_color="#8a8281", command=self.open_settings)
        settings_btn.pack(side="bottom", fill="both", pady=20, padx=10)

    def highlight_step(self, index):
        for i, lbl in enumerate(self.labels):
            if i < index:
                lbl.configure(text_color="#4CAF50", fg_color="#333333") 
            elif i == index:
                lbl.configure(text_color="white", fg_color="#4CAF50") 
            else:
                lbl.configure(text_color="#555555", fg_color="#2b2b2b") 

    def open_settings(self):
        print("settings")
