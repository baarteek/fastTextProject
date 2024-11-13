import customtkinter as ctk
from tkinter import filedialog
from ..components.universal_table import UniversalTable
from ..components.progress_dialog import ProgressDialog

class DataSplittingView(ctk.CTkScrollableFrame):
    def __init__(self, master, data_manager=None, navigation_bar=None, **kwargs):
        super().__init__(master, fg_color="#1E1E1E", **kwargs)

        self.data_manager = data_manager

        self.split_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        self.split_frame.pack(pady=(10, 5), fill="x", expand=True)

        self.split_ratio_label = ctk.CTkLabel(self.split_frame, text="Train-Test Split Ratio (%)")
        self.split_ratio_label.pack(side="left", padx=5)

        self.split_ratio_slider = ctk.CTkSlider(self.split_frame, from_=1, to=99, command=self.update_split_entry)
        self.split_ratio_slider.set(80)
        self.split_ratio_slider.pack(side="left", padx=5, fill="x", expand=True)

        self.split_ratio_entry = ctk.CTkEntry(self.split_frame, width=50)
        self.split_ratio_entry.insert(0, "80")
        self.split_ratio_entry.pack(side="left", padx=5)
        self.split_ratio_entry.bind("<KeyRelease>", self.update_slider_from_entry)

        self.split_button = ctk.CTkButton(self, text="Split Data", command=self.split_data)
        self.split_button.pack(pady=5, fill="x", expand=True)

        self.records_label = ctk.CTkLabel(self, text="Total Records: 0")
        self.records_label.pack(pady=(5, 10))

        self.train_data_label = ctk.CTkLabel(self, text="Training Data Sample")
        self.train_data_label.pack(pady=(10, 5))
        self.train_data_table = UniversalTable(self, data_list=[], empty_message="No training data available")
        self.train_data_table.pack(pady=5, fill="both", expand=True)

        self.test_data_label = ctk.CTkLabel(self, text="Testing Data Sample")
        self.test_data_label.pack(pady=(10, 5))
        self.test_data_table = UniversalTable(self, data_list=[], empty_message="No testing data available")
        self.test_data_table.pack(pady=5, fill="both", expand=True)

        self.save_button = ctk.CTkButton(self, text="Save Splits to Files", command=self.save_splits)
        self.save_button.pack(pady=10, fill="x", expand=True)

        self.display_record_count()
        
    def update_split_entry(self, value):
        self.split_ratio_entry.delete(0, "end")
        self.split_ratio_entry.insert(0, str(int(float(value))))

    def update_slider_from_entry(self, event):
        try:
            value = int(self.split_ratio_entry.get())
            if 1 <= value <= 99:
                self.split_ratio_slider.set(value)
        except ValueError:
            pass

    def split_data(self):
        try:
            split_ratio = float(self.split_ratio_entry.get()) / 100.0
            if not 0 < split_ratio < 1:
                raise ValueError("Split ratio must be between 1 and 99.")

            progress_dialog = ProgressDialog(self, title="Splitting Data", message="Splitting data into training and testing sets...")
            self.data_manager.split_data(split_ratio)
            progress_dialog.stop_progress()

            self.display_train_test_samples()
        except ValueError as e:
            print(f"Invalid split ratio: {e}")

    def display_record_count(self):
        total_records = len(self.data_manager.get_data()) if self.data_manager.get_data() is not None else 0
        self.records_label.configure(text=f"Total Records: {total_records}")

    def display_train_test_samples(self):
        train_sample = self.data_manager.get_train_data().head(500).to_dict("records")
        test_sample = self.data_manager.get_test_data().head(500).to_dict("records")
        self.train_data_table.display_data(train_sample)
        self.test_data_table.display_data(test_sample)

    def save_splits(self):
        train_file_path = filedialog.asksaveasfilename(defaultextension=".csv", title="Save Training Data")
        test_file_path = filedialog.asksaveasfilename(defaultextension=".csv", title="Save Testing Data")
        
        if train_file_path and test_file_path:
            progress_dialog = ProgressDialog(self, title="Saving Splits", message="Saving training and testing data to files...")
            self.data_manager.save_splits(train_file_path, test_file_path)
            progress_dialog.stop_progress()
