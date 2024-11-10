import customtkinter as ctk

class NavigationBar(ctk.CTkFrame):
    def __init__(self, master, title, on_back=None, on_next=None, **kwargs):
        super().__init__(master, fg_color="#2F2F2F", **kwargs)

        self.back_btn = ctk.CTkButton(
            self, text="Back", command=on_back, 
            state="normal" if on_back else "disabled", 
            fg_color="#6c757d", text_color="white"
        )
        self.back_btn.pack(side="left", padx=30, pady=20, fill="both")

        self.title_label = ctk.CTkLabel(
            self, text=title, font=("Arial", 16, "bold"), text_color="white"
        )
        self.title_label.pack(side="left", expand=True)

        self.next_btn = ctk.CTkButton(
            self, text="Next Step", command=on_next, 
            state="normal" if on_next else "disabled", 
            fg_color="#4CAF50", text_color="white"
        )
        self.next_btn.pack(side="right", padx=30, pady=20, fill="both")

    def update_title(self, title):
        self.title_label.configure(text=title)

    def set_back_enabled(self, enabled):
        state = "normal" if enabled else "disabled"
        self.back_btn.configure(state=state)

    def set_next_enabled(self, enabled):
        state = "normal" if enabled else "disabled"
        self.next_btn.configure(state=state)
