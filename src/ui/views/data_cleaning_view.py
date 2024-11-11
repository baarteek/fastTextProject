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

        self.missing_details_table = UniversalTable(self, data_list=[], empty_message="No missing values")
        self.missing_details_table.pack(pady=5, fill="both", expand=True)

        self.missing_info_label = ctk.CTkLabel(self, text="Total records with missing values: 0", font=("Arial", 12))
        self.missing_info_label.pack(pady=(5, 10))

        self.manual_entry_frame = ctk.CTkFrame(self, fg_color="#2B2B2B")
        self.manual_entry_frame.pack(pady=10, fill="x", expand=True)

        self.column_var = ctk.StringVar()
        self.index_var = ctk.StringVar()
        self.value_var = ctk.StringVar()

        self.column_label = ctk.CTkLabel(self.manual_entry_frame, text="Column:")
        self.column_label.pack(side="left", padx=5)

        self.column_select = ctk.CTkOptionMenu(self.manual_entry_frame, variable=self.column_var, values=[])
        self.column_select.pack(side="left", padx=5)

        self.index_label = ctk.CTkLabel(self.manual_entry_frame, text="Index:")
        self.index_label.pack(side="left", padx=5)

        self.index_entry = ctk.CTkEntry(self.manual_entry_frame, textvariable=self.index_var)
        self.index_entry.pack(side="left", padx=5)

        self.value_label = ctk.CTkLabel(self.manual_entry_frame, text="Value:")
        self.value_label.pack(side="left", padx=5)

        self.value_entry = ctk.CTkEntry(self.manual_entry_frame, textvariable=self.value_var)
        self.value_entry.pack(side="left", padx=5)

        self.apply_button = ctk.CTkButton(self.manual_entry_frame, text="Apply", command=self.apply_manual_entry)
        self.apply_button.pack(side="left", padx=5)

        self.fill_buttons_frame = ctk.CTkFrame(self, fg_color="#2B2B2B")
        self.fill_buttons_frame.pack(pady=10, fill="x", expand=True)
        
        self.fill_above_button = ctk.CTkButton(self.fill_buttons_frame, text="Fill from Above", command=self.fill_missing_from_above, state="disabled")
        self.fill_above_button.pack(side="left", padx=5, fill="x", expand=True)

        self.fill_below_button = ctk.CTkButton(self.fill_buttons_frame, text="Fill from Below", command=self.fill_missing_from_below, state="disabled")
        self.fill_below_button.pack(side="left", padx=5, fill="x", expand=True)

        self.remove_missing_button = ctk.CTkButton(self.fill_buttons_frame, text="Remove Missing Values", command=self.remove_missing_values, fg_color="#c24c4c", hover_color="#9c3636", state="disabled")
        self.remove_missing_button.pack(side="right", padx=5, fill="x", expand=True)

        self.duplicates_label = ctk.CTkLabel(self, text="Duplicate Records", font=("Arial", 16, "bold"))
        self.duplicates_label.pack(pady=(20, 5))

        self.duplicates_table = UniversalTable(self, data_list=[], empty_message="No duplicate records found")
        self.duplicates_table.pack(pady=5, fill="both", expand=True)

        self.duplicates_info_label = ctk.CTkLabel(self, text="Total duplicate records: 0", font=("Arial", 12))
        self.duplicates_info_label.pack(pady=(5, 10))

        self.remove_duplicates_button = ctk.CTkButton(self, text="Remove Duplicates", command=self.remove_duplicates, fg_color="#c24c4c", hover_color="#9c3636")
        self.remove_duplicates_button.pack(pady=10, fill="x", expand=True)

        self.display_missing_details()
        self.display_duplicates()
        self.populate_column_options()

    def populate_column_options(self):
        columns = [col for col in self.data_manager.get_data().columns]
        self.column_select.configure(values=columns)
        if columns:
            self.column_var.set(columns[0])

    def display_missing_details(self):        
        total_records = len(self.data_manager.get_data())
        missing_rows = self.data_manager.get_data()[self.data_manager.get_data().isnull().any(axis=1)]
        missing_count = len(missing_rows)
        
        if missing_count > 0:
            missing_rows = missing_rows.reset_index().rename(columns={"index": "Index"})
            missing_details = missing_rows.to_dict("records")
            
            self.missing_details_table.display_data(missing_details)
            self.missing_info_label.configure(text=f"Total records with missing values: {missing_count}/{total_records}")
            self.fill_above_button.configure(state="normal")
            self.fill_below_button.configure(state="normal")
            self.remove_missing_button.configure(state="normal")
        else:
            self.missing_details_table.display_data([{"Column": "No missing values", "Index": ""}])
            self.missing_info_label.configure(text=f"Total records with missing values: 0/{total_records}")
            self.fill_above_button.configure(state="disabled")
            self.fill_below_button.configure(state="disabled")
            self.remove_missing_button.configure(state="disabled")


    def display_duplicates(self):
        total_records = len(self.data_manager.get_data())
        duplicates = self.data_manager.get_duplicates()
        duplicates_count = len(duplicates)
        
        if not duplicates.empty:
            duplicates_data = duplicates.to_dict("records")
            self.duplicates_table.display_data(duplicates_data)
            self.duplicates_info_label.configure(text=f"Total duplicate records: {duplicates_count}/{total_records}")
            self.remove_duplicates_button.configure(state="normal")
        else:
            self.duplicates_table.display_data([{"Message": "No duplicate records found"}])
            self.duplicates_info_label.configure(text=f"Total duplicate records: 0/{total_records}")
            self.remove_duplicates_button.configure(state="disabled")

    def fill_missing_from_above(self):
        progress_dialog = ProgressDialog(self, title="Filling Missing Values", message="Filling missing values from above...")
        self.data_manager.fill_missing_from_above()
        progress_dialog.stop_progress()
        self.display_missing_details()

    def fill_missing_from_below(self):
        progress_dialog = ProgressDialog(self, title="Filling Missing Values", message="Filling missing values from below...")
        self.data_manager.fill_missing_from_below()
        progress_dialog.stop_progress()
        self.display_missing_details()

    def remove_missing_values(self):
        progress_dialog = ProgressDialog(self, title="Removing Missing Values", message="Removing missing values...")
        self.data_manager.drop_missing_values()
        progress_dialog.stop_progress()
        self.display_missing_details()

    def apply_manual_entry(self):
        column = self.column_var.get()
        try:
            index = int(self.index_var.get())
            value = self.value_var.get()
            self.data_manager.fill_manual(column, index, value)
            self.display_missing_details()
            self.index_var.set("")
            self.value_var.set("")
        except ValueError:
            print("Invalid index value. Please enter a numeric index.")

    def remove_duplicates(self):
        progress_dialog = ProgressDialog(self, title="Removing Duplicates", message="Removing duplicate records...")
        self.data_manager.remove_duplicates()
        progress_dialog.stop_progress()
        self.display_duplicates()
