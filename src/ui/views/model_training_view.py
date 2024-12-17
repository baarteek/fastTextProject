import customtkinter as ctk
import threading
import time

from modules.fasttext_manager import FastTextManager

class ModelTrainingView(ctk.CTkScrollableFrame):
    def __init__(self, master, fasttext_manager=None, navigation_bar=None, **kwargs):
        super().__init__(master, fg_color="#1E1E1E", **kwargs)
        
        self.fasttext_manager = fasttext_manager or FastTextManager()
        self.navigation_bar = navigation_bar
        self.training_thread = None
        self.stop_training = False

        self.create_ui()

    def create_ui(self):
        title_label = ctk.CTkLabel(self, text="Model Training", font=("Arial", 16, "bold"), text_color="white")
        title_label.pack(pady=(20, 10))

        self.info_label = ctk.CTkLabel(self, text="Click 'Start Training' to begin.", text_color="grey")
        self.info_label.pack(pady=10)

        self.start_button = ctk.CTkButton(self, text="Start Training", fg_color="#4CAF50", command=self.start_training)
        self.start_button.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=20, pady=10)

        self.result_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=8)
        self.result_frame.pack(fill="x", padx=20, pady=(10, 20))
        self.result_frame.pack_forget()

        self.params_label = ctk.CTkLabel(self.result_frame, text="", text_color="white", font=("Arial", 12))
        self.params_label.pack(anchor="w", padx=10, pady=5)

        self.evaluation_label = ctk.CTkLabel(self.result_frame, text="", text_color="white", font=("Arial", 12))
        self.evaluation_label.pack(anchor="w", padx=10, pady=5)

    def start_training(self):
        self.start_button.configure(state="disabled")
        self.info_label.configure(text="Training in progress...", text_color="blue")
        self.progress_bar.set(0)
        self.stop_training = False

        self.training_thread = threading.Thread(target=self.run_training)
        self.training_thread.start()

    def run_training(self):
        params = self.fasttext_manager.params
        epoch = params.get("epoch", 5)
        
        success = self.fasttext_manager.train_model()
        if not success:
            self.after(0, self.training_failed)
            return

        self.after(0, lambda: self.progress_bar.set(1.0))

        params_text = "Training Parameters:\n"
        for k, v in params.items():
            params_text += f"{k}: {v}\n"

        results = self.fasttext_manager.evaluate_model()

        if results is not None:
            eval_text = (f"Evaluation Results:\n"
                         f"Number of examples: {results['Number of examples']}\n"
                         f"Precision: {results['Precision']}\n"
                         f"Recall: {results['Recall']}")
        else:
            eval_text = "No evaluation results available (no test file or model not trained)."

        self.after(0, lambda: self.show_results(params_text, eval_text))

    def show_results(self, params_text, eval_text):
        self.info_label.configure(text="Training completed!", text_color="green")
        self.start_button.configure(state="normal")
        self.result_frame.pack(fill="x", padx=20, pady=(10, 20))
        self.params_label.configure(text=params_text)
        self.evaluation_label.configure(text=eval_text)

    def training_failed(self):
        self.info_label.configure(text="Training failed. Check logs for details.", text_color="red")
        self.start_button.configure(state="normal")
