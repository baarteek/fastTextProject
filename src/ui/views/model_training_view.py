import customtkinter as ctk
import threading
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from modules.fasttext_manager import FastTextManager
from ..components.universal_table import UniversalTable


class ModelTrainingView(ctk.CTkScrollableFrame):
    def __init__(self, master, fasttext_manager=None, navigation_bar=None, **kwargs):
        super().__init__(master, fg_color="#1E1E1E", **kwargs)

        self.fasttext_manager = fasttext_manager or FastTextManager()
        self.navigation_bar = navigation_bar
        self.training_thread = None
        self.stop_training = False
        self.current_epoch = 0
        self.total_epochs = self.fasttext_manager.params.get("epoch", 5)

        self.epoch_accuracies = []

        self.create_ui()

    def create_ui(self):
        title_label = ctk.CTkLabel(self, text="Model Training", font=("Arial", 18, "bold"), text_color="white")
        title_label.pack(pady=(20, 10))

        self.info_label = ctk.CTkLabel(self, text="Click 'Start Training' to begin.", text_color="grey", font=("Arial", 14))
        self.info_label.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self, height=20)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=20, pady=10)

        self.epoch_label = ctk.CTkLabel(self, text="Epoch: 0 / 0", text_color="white", font=("Arial", 12))
        self.epoch_label.pack(pady=5)

        self.start_button = ctk.CTkButton(self, text="Start Training", fg_color="#4CAF50", command=self.start_training)
        self.start_button.pack(pady=10)

        self.stop_button = ctk.CTkButton(self, text="Stop Training", fg_color="#FF5733", command=self.stop_training_button, state="disabled")
        self.stop_button.pack(pady=10)

        log_label = ctk.CTkLabel(self, text="Training Logs", font=("Arial", 14, "bold"), text_color="white")
        log_label.pack(pady=(10, 5))

        self.log_textbox = ctk.CTkTextbox(self, height=200, wrap="word", font=("Arial", 12), text_color="white")
        self.log_textbox.pack(fill="both", padx=20, pady=(0, 10))

        plot_label = ctk.CTkLabel(self, text="Training Accuracy Plot", font=("Arial", 14, "bold"), text_color="white")
        plot_label.pack(pady=(10, 5))

        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_title("Training Accuracy by Epoch")
        self.ax.set_xlabel("Epoch")
        self.ax.set_ylabel("Accuracy")
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", padx=20, pady=(0, 10))

        self.result_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=8)
        self.result_frame.pack(fill="x", padx=20, pady=(10, 20))
        self.result_frame.pack_forget()

        self.result_label = ctk.CTkLabel(self.result_frame, text="Training Results", font=("Arial", 14, "bold"), text_color="white")
        self.result_label.pack(pady=(10, 5))

        self.table_container = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        self.table_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.results_table = None

    def log_message(self, message):
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.see("end")

    def start_training(self):
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.info_label.configure(text="Training in progress...", text_color="blue")
        self.progress_bar.set(0)
        self.current_epoch = 0
        self.stop_training = False
        self.total_epochs = self.fasttext_manager.params.get("epoch", 5)
        self.epoch_label.configure(text=f"Epoch: 0 / {self.total_epochs}")
        self.log_textbox.delete("1.0", "end")
        self.epoch_accuracies.clear()

        self.training_thread = threading.Thread(target=self.run_training)
        self.training_thread.start()

    def stop_training_button(self):
        self.stop_training = True
        self.log_message("Stopping training...")

    def run_training(self):
        start_time_total = time.time()

        for epoch in range(1, self.total_epochs + 1):
            if self.stop_training:
                self.log_message("Training stopped by user.")
                break

            start_time_epoch = time.time()
            self.log_message(f"Starting Epoch {epoch}...")
            success = self.fasttext_manager.train_model()

            if not success:
                self.after(0, self.training_failed)
                return

            end_time_epoch = time.time()
            epoch_time = end_time_epoch - start_time_epoch
            self.current_epoch = epoch
            progress = epoch / self.total_epochs
            self.log_message(f"Epoch {epoch} completed in {epoch_time:.2f} seconds.")

            results = self.fasttext_manager.evaluate_model()
            accuracy = results.get("Accuracy", 0)
            self.epoch_accuracies.append(accuracy)
            self.log_message(f"Accuracy after Epoch {epoch}: {accuracy:.4f}")

            self.after(0, lambda e=epoch, p=progress, t=epoch_time: self.update_progress(e, p, t))
            self.after(0, self.update_plot)

        end_time_total = time.time()
        total_training_time = end_time_total - start_time_total

        final_results = self.fasttext_manager.evaluate_model()
        if self.stop_training:
            self.log_message(f"Training stopped. Displaying results for completed epochs...")
        else:
            self.log_message(f"Total training time: {total_training_time:.2f} seconds.")
            self.log_message("Evaluation completed. Displaying results...")

        self.after(0, lambda: self.show_results(final_results, total_training_time))
        self.after(0, self.training_finished)

    def training_finished(self):
        self.stop_button.configure(state="disabled")
        self.start_button.configure(state="normal")
        self.info_label.configure(text="Training stopped or completed.", text_color="green")

    def update_progress(self, epoch, progress, epoch_time):
        self.progress_bar.set(progress)
        self.epoch_label.configure(text=f"Epoch: {epoch} / {self.total_epochs} - Time: {epoch_time:.2f} sec")
        self.info_label.configure(text=f"Epoch {epoch} completed in {epoch_time:.2f} seconds", text_color="yellow")

    def update_plot(self):
        self.ax.clear()
        self.ax.set_title("Training Accuracy by Epoch")
        self.ax.set_xlabel("Epoch")
        self.ax.set_ylabel("Accuracy")
        self.ax.grid(True)
        self.ax.plot(range(1, len(self.epoch_accuracies) + 1), self.epoch_accuracies, marker="o", linestyle="-", color="b")
        self.canvas.draw()

    def show_results(self, results, total_time):
        self.info_label.configure(text="Training completed!", text_color="green")
        self.start_button.configure(state="normal")
        self.result_frame.pack(fill="x", padx=20, pady=(10, 20))

        if results:
            data_list = [
                {"Metric": "Number of Examples", "Value": results.get("Number of examples", "N/A")},
                {"Metric": "Accuracy", "Value": f"{results.get('Accuracy', 0):.4f}"},
                {"Metric": "Total Training Time", "Value": f"{total_time:.2f} seconds"}
            ]
        else:
            data_list = [{"Metric": "Error", "Value": "No evaluation results available"}]

        if self.results_table:
            self.results_table.destroy()
        self.results_table = UniversalTable(self.table_container, data_list=data_list)
        self.results_table.pack(fill="both", expand=True, padx=10, pady=10)
        self.navigation_bar.set_next_enabled(True)

    def training_failed(self):
        self.log_message("Training failed. Check logs for details.")
        self.info_label.configure(text="Training failed. Check logs for details.", text_color="red")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
