import customtkinter as ctk
from tkinter import filedialog

class LoadModelView(ctk.CTkScrollableFrame):
    def __init__(self, master, fasttext_manager=None, navigation_bar=None, **kwargs):
        super().__init__(master, fg_color="#1E1E1E", **kwargs)

        self.fasttext_manager = fasttext_manager
        self.navigation_bar = navigation_bar

        self.create_ui()

    def create_ui(self):
        title_label = ctk.CTkLabel(self, text="Load Pretrained Model", font=("Arial", 18, "bold"), text_color="white")
        title_label.pack(pady=(20, 10))

        self.info_label = ctk.CTkLabel(self, text="Select a saved FastText model file to load.", text_color="grey", font=("Arial", 14))
        self.info_label.pack(pady=10)

        self.load_button = ctk.CTkButton(self, text="Load Model", fg_color="#4CAF50", command=self.load_model)
        self.load_button.pack(pady=10)

        self.test_data_button = ctk.CTkButton(self, text="Load Test Data", fg_color="#FFA500", command=self.load_test_data, state="disabled")
        self.test_data_button.pack(pady=10)

        self.evaluate_button = ctk.CTkButton(self, text="Evaluate Model", fg_color="#4CAF50", command=self.evaluate_model, state="disabled")
        self.evaluate_button.pack(pady=10)

        self.log_textbox = ctk.CTkTextbox(self, height=200, wrap="word", font=("Arial", 12), text_color="white")
        self.log_textbox.pack(fill="both", padx=20, pady=(10, 20))

    def log_message(self, message):
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.see("end")

    def load_model(self):
        file_path = filedialog.askopenfilename(
            title="Select a FastText Model File",
            filetypes=(("FastText Model Files", "*.bin"), ("All Files", "*.*"))
        )

        if not file_path:
            self.log_message("Model loading canceled.")
            return

        try:
            self.fasttext_manager.load_model(file_path)
            self.log_message(f"Model loaded successfully from {file_path}.")
            self.test_data_button.configure(state="normal")
        except Exception as e:
            self.log_message(f"Failed to load model: {e}")

    def load_test_data(self):
        file_path = filedialog.askopenfilename(
            title="Select Test Data File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )

        if not file_path:
            self.log_message("Test data loading canceled.")
            return

        try:
            self.fasttext_manager.set_test_file(file_path)
            self.log_message(f"Test data loaded successfully from {file_path}.")
            self.evaluate_button.configure(state="normal")
        except Exception as e:
            self.log_message(f"Failed to load test data: {e}")

    def evaluate_model(self):
        try:
            results = self.fasttext_manager.evaluate_model()

            if not results:
                self.log_message("Evaluation failed. Check the model and test data.")
                return

            accuracy = results.get("Accuracy", 0)
            num_examples = results.get("Number of examples", "N/A")
            recall = results.get("Recall", 0)

            self.log_message("Evaluation Results:")
            self.log_message(f"Number of Examples: {num_examples}")
            self.log_message(f"Accuracy: {accuracy:.4f}")
            self.log_message(f"Recall: {recall:.4f}")
        except Exception as e:
            self.log_message(f"Failed to evaluate model: {e}")
