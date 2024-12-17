import customtkinter as ctk

class ModelValidationView(ctk.CTkScrollableFrame):
    def __init__(self, master, data_manager=None, navigation_bar=None, **kwargs):
        super().__init__(master, fg_color="#1E1E1E", **kwargs)

        self.hello_label = ctk.CTkLabel(self, text="Model Validation View")
        self.hello_label.pack(pady=(10,5))