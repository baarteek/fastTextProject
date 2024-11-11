import customtkinter as ctk
from ..components.universal_table import UniversalTable
from ..components.progress_dialog import ProgressDialog

class DataCleaningView(ctk.CTkScrollableFrame):
    def __init__(self, master, data_manager=None, navigation_bar=None, **kwargs):
        super().__init__(master, fg_color="#1E1E1E", **kwargs)
        
        self.data_manager = data_manager
        self.navigation_bar = navigation_bar

        self.missing_label = ctk.CTkLabel(self, text="Missing Values", font=("Arial", 16, "bold"))
        self.missing_label.pack(pady=(10, 5))

        self.missing_table = UniversalTable(self, data_list=[], empty_message="No missing values")
        self.missing_table.pack(pady=5, fill="both", expand=True)

        self.fill_buttons_frame = ctk.CTkFrame(self, fg_color="#2B2B2B")
        self.fill_buttons_frame.pack(pady=10, fill="x", expand=True)
        
        self.fill_above_button = ctk.CTkButton(self.fill_buttons_frame, text="Fill from Above", command=self.fill_missing_from_above, state="disabled")
        self.fill_above_button.pack(side="left", padx=5, fill="x", expand=True)

        self.fill_below_button = ctk.CTkButton(self.fill_buttons_frame, text="Fill from Below", command=self.fill_missing_from_below, state="disabled")
        self.fill_below_button.pack(side="left", padx=5, fill="x", expand=True)

        self.remove_missing_button = ctk.CTkButton(self.fill_buttons_frame, text="Remove Missing Values", command=self.remove_missing_values, fg_color="#c24c4c", state="disabled")
        self.remove_missing_button.pack(side="right", padx=5, fill="x", expand=True)

        self.display_missing_values()

    def display_missing_values(self):
        missing_values = self.data_manager.get_missing_values()
        missing_data = [{"Column": col, "Missing Values": count} for col, count in missing_values.items() if count > 0]
        if missing_data:
            self.missing_table.display_data(missing_data)
            self.fill_above_button.configure(state="normal")
            self.fill_below_button.configure(state="normal")
            self.remove_missing_button.configure(state="normal")
        else:
            self.missing_table.display_data([{"Column": "No missing values", "Missing Values": ""}])
            self.fill_above_button.configure(state="disabled")
            self.fill_below_button.configure(state="disabled")
            self.remove_missing_button.configure(state="disabled")

    def fill_missing_from_above(self):
        progress_dialog = ProgressDialog(self, title="Filling Missing Values", message="Filling missing values from above...")
        self.data_manager.fill_missing_from_above()
        progress_dialog.stop_progress()
        self.display_missing_values()

    def fill_missing_from_below(self):
        progress_dialog = ProgressDialog(self, title="Filling Missing Values", message="Filling missing values from below...")
        self.data_manager.fill_missing_from_below()
        progress_dialog.stop_progress()
        self.display_missing_values()

    def remove_missing_values(self):
        progress_dialog = ProgressDialog(self, title="Removing Missing Values", message="Removing missing values...")
        self.data_manager.drop_missing_values()
        progress_dialog.stop_progress()
        self.display_missing_values()
