import customtkinter as ctk

class ProgressDialog(ctk.CTkToplevel):
    def __init__(self, master, title="Processing", message="Please wait...", **kwargs):
        super().__init__(master, **kwargs)
        self.title(title)
        self.geometry("300x100")
        self.transient(master)
        self.resizable(False, False)
        
        self.label = ctk.CTkLabel(self, text=message)
        self.label.pack(pady=20)

        self.update_idletasks()

    def stop_progress(self):
        self.destroy()
