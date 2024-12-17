import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, callback, steps, **kwargs):
        super().__init__(master, fg_color="#2b2b2b", **kwargs)
        self.callback = callback
        self.steps = steps 
        self.labels = []
        self.current_index = 0

        self.button_state = "go_to_training"

        self.create_sidebar()

    def create_sidebar(self):
        title_label = ctk.CTkLabel(self, text="fastText Project", font=("Arial", 16, "bold"), text_color="white")
        title_label.pack(pady=(10, 20))

        for step in self.steps:
            lbl = ctk.CTkLabel(self, text=step, font=("Arial", 12, "bold"), text_color="#555555", fg_color="#2b2b2b", corner_radius=10)
            lbl.pack(fill='both', pady=5, padx=15)
            self.labels.append(lbl)

        self.dynamic_btn = ctk.CTkButton(self, text="Go to Model Training", fg_color="#4CAF50", command=self.toggle_button_action)
        self.dynamic_btn.pack(side="bottom", fill="both", pady=20, padx=10)

    def toggle_button_action(self):
        if self.button_state == "go_to_training":
            model_training_index = self.steps.index("Model Configuration")
            self.callback(model_training_index)

            self.button_state = "go_to_prepare"
            self.dynamic_btn.configure(text="Go to Prepare Data")
        else:
            prepare_data_index = self.steps.index("Data Loading")
            self.callback(prepare_data_index)
            self.button_state = "go_to_training"
            self.dynamic_btn.configure(text="Go to Model Training")

    def highlight_step(self, index):
        for i, lbl in enumerate(self.labels):
            if i < index:
                lbl.configure(text_color="#4CAF50", fg_color="#333333")
            elif i == index:
                lbl.configure(text_color="white", fg_color="#4CAF50")
            else:
                lbl.configure(text_color="#555555", fg_color="#2b2b2b")
