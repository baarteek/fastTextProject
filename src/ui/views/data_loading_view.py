import customtkinter as ctk
from tkinter import filedialog, ttk
from modules.data_manager import DataManager

class DataLoadingView(ctk.CTkFrame):
    def __init__(self, master, data_manager=None, navigation_bar=None, on_data_loaded=None, **kwargs):
        super().__init__(master, fg_color="#1E1E1E", **kwargs)
        
        self.data_manager = data_manager or DataManager()
        self.on_data_loaded = on_data_loaded
        self.navigation_bar = navigation_bar 

        self.label = ctk.CTkLabel(self, text="Load Data for Classification", font=("Arial", 16, "bold"))
        self.label.pack(pady=(20, 10))
        
        self.load_button = ctk.CTkButton(self, text="Load Data", command=self.load_data)
        self.load_button.pack(pady=(10, 20))

        self.status_label = ctk.CTkLabel(self, text="No file loaded", text_color="grey")
        self.status_label.pack(pady=10)
        
        self.table_frame = ctk.CTkFrame(self)
        
        self.data_table = ttk.Treeview(self.table_frame, show='headings')
        self.data_table.pack(side="left", fill="both", expand=True)

        self.v_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.data_table.yview)
        self.v_scrollbar.pack(side="right", fill="y")
        self.data_table.configure(yscrollcommand=self.v_scrollbar.set)

        self.record_info_label = ctk.CTkLabel(self, text="", text_color="grey")
        self.record_info_label.pack(pady=(5, 15))

    def load_data(self):
        file_path = filedialog.askopenfilename(
            title="Select Data File", 
            filetypes=[("CSV and JSON Files", "*.csv *.json"), ("CSV Files", "*.csv"), ("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path:
            success = self.data_manager.load_data(file_path)
            if success:
                self.status_label.configure(text=f"Loaded: {file_path}", text_color="green")
                self.display_data_in_table()
                if self.navigation_bar:
                    self.navigation_bar.set_next_enabled(True) 
                if self.on_data_loaded:
                    self.on_data_loaded(file_path)
            else:
                self.status_label.configure(text="Failed to load data", text_color="red")
                if self.navigation_bar:
                    self.navigation_bar.set_next_enabled(False)
        else:
            self.status_label.configure(text="No file selected", text_color="red")
    
    def display_data_in_table(self, limit=50):
        data = self.data_manager.get_data()
        if data is not None:
            self.table_frame.pack(pady=10, fill="both", expand=True)

            self.data_table.delete(*self.data_table.get_children())

            columns = ["Number"] + list(data.columns)
            self.data_table["columns"] = columns
            for col in columns:
                if col == "Number":
                    self.data_table.heading(col, text=col)
                    self.data_table.column(col, width=50, stretch=False)
                else:
                    self.data_table.heading(col, text=col)
                    self.data_table.column(col, minwidth=100, width=150, stretch=True)

            for i, (_, row) in enumerate(data.head(limit).iterrows(), start=1):
                row_values = [i] + list(row)
                self.data_table.insert("", "end", values=row_values)

            total_records = len(data)
            if limit < total_records:
                self.record_info_label.configure(text=f"Displaying first {limit} of {total_records} records")
            else:
                self.record_info_label.configure(text=f"Displaying all {total_records} records")
        else:
            self.status_label.configure(text="No data available for display", text_color="red")
            self.table_frame.pack_forget()
            self.record_info_label.configure(text="")
