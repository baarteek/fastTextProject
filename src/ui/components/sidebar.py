import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, callback, **kwargs):
        super().__init__(master, fg_color="#2b2b2b", **kwargs)

        self.callback = callback
        self.current_step = 0
        self.steps = [
            "Data Preparation",
            "Model Training",
            "Model Evaluation",
            "Model Application",
        ]
        self.buttons = []
        self.create_sidebar()

    def create_sidebar(self):
        title_label = ctk.CTkLabel(self, text="fastText Project", font=("Arial", 16, "bold"), text_color="white")
        title_label.pack(pady=(10,20))
        for index, step in enumerate(self.steps):
            btn = ctk.CTkButton(self, text=step, command=lambda idx = index: self.on_button_click(idx))
            btn.pack(fill='both', pady=10, padx=10)
            self.buttons.append(btn)
            if index != 0:
                btn.configure(state="disabled")
    
    def on_button_click(self, index):
        if index == self.current_step:
            self.callback(index)

    def enable_next_step(self):
        self.current_step += 1
        if self.current_step < len(self.buttons):
            self.buttons[self.current_step].configure(state="normal")

    def reset(self): 
        self.current_step = 0
        for btn in self.buttons:
            btn.configure(state="disabled")
            if self.buttons: 
                self.buttons[0].configure(state="norma")