import customtkinter as ctk
from tkinter import filedialog
from modules.fasttext_manager import FastTextManager

class ModelExportView(ctk.CTkScrollableFrame):
    def __init__(self, master, fasttext_manager=None, navigation_bar=None, **kwargs):
        super().__init__(master, fg_color="#1E1E1E", **kwargs)

        self.fasttext_manager = fasttext_manager

        self.title_label = ctk.CTkLabel(self, text="Model Export View", font=("Arial", 16))
        self.title_label.pack(pady=(10, 5))

        self.save_button = ctk.CTkButton(self, text="Save Model", command=self.save_model)
        self.save_button.pack(pady=(10, 5))

        self.status_label = ctk.CTkLabel(self, text="", text_color="green")
        self.status_label.pack(pady=(10, 5))

    def save_model(self):
        if self.fasttext_manager is None or self.fasttext_manager.model is None:
            self.status_label.configure(text="No trained model to save.", text_color="red")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".bin",
            filetypes=[("FastText Model", "*.bin"), ("All Files", "*.*")],
            title="Save Model"
        )

        if file_path:
            try:
                self.fasttext_manager.save_model(file_path)
                self.status_label.configure(text="Model saved successfully.", text_color="green")
            except Exception as e:
                self.status_label.configure(text=f"Error: {e}", text_color="red")