import customtkinter as ctk
from tkinter import filedialog
from modules.data_manager import DataManager

class ModelTrainingView(ctk.CTkFrame):
    def __init__(self, master, data_manager=None, navigation_bar=None, **kwargs):
        super().__init__(master, fg_color="#1E1E1E", **kwargs)
        
        self.data_manager = data_manager or DataManager()
        self.navigation_bar = navigation_bar
        
        self.train_data_path = None
        self.test_data_path = None
        
        self.param_entries = {}
        self.default_values = {
            "Epochs": ("10", "Number of training iterations", "int"),
            "Learning Rate": ("0.1", "Step size for learning", "float"),
            "Dimension": ("100", "Size of word vectors", "int"),
            "Word N-Grams": ("2", "Max n-grams length", "int"),
            "Loss Function": ("softmax", "Type of loss function", None),
            "Min Word Count": ("5", "Minimum word occurrences", "int"),
            "Bucket Size": ("2000000", "Number of hash buckets", "int"),
            "Subword Min Length": ("3", "Min subword length", "int"),
            "Subword Max Length": ("6", "Max subword length", "int")
        }

        self.loss_options = ["softmax", "ns", "hs"]
        
        self.create_ui()

    def create_ui(self):
        title_label = ctk.CTkLabel(self, text="Model Training Configuration", font=("Arial", 16, "bold"), text_color="white")
        title_label.pack(pady=(20, 10))
        
        self.create_file_selection_section()
        
        self.param_section = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=8)
        # Ukryte do momentu potwierdzenia ścieżek
        self.param_section.pack_forget()

        self.train_button = ctk.CTkButton(self, text="Train Model", fg_color="#4CAF50", state="disabled", command=self.train_model)

        self.status_label = ctk.CTkLabel(self, text="", text_color="grey")
        self.status_label.pack(pady=10)

    def create_file_selection_section(self):
        train_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=8)
        train_frame.pack(fill="x", padx=20, pady=(10, 5))

        ctk.CTkLabel(train_frame, text="Training Data Path:", text_color="white").pack(side="left", padx=(10, 5))
        self.train_path_label = ctk.CTkLabel(train_frame, text="Not Selected", text_color="grey")
        self.train_path_label.pack(side="left", expand=True, padx=(5, 5))
        train_btn = ctk.CTkButton(train_frame, text="Browse", command=self.select_train_data)
        train_btn.pack(side="right", padx=(5, 10))

        test_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=8)
        test_frame.pack(fill="x", padx=20, pady=(5, 20))

        ctk.CTkLabel(test_frame, text="Testing Data Path:", text_color="white").pack(side="left", padx=(10, 5))
        self.test_path_label = ctk.CTkLabel(test_frame, text="Not Selected", text_color="grey")
        self.test_path_label.pack(side="left", expand=True, padx=(5, 5))
        test_btn = ctk.CTkButton(test_frame, text="Browse", command=self.select_test_data)
        test_btn.pack(side="right", padx=(5, 10))
        
        self.confirm_button = ctk.CTkButton(self, text="Confirm Paths", fg_color="#4CAF50", command=self.confirm_paths)
        self.confirm_button.pack(pady=(10, 20))

    def setup_parameter_table(self):
        # Nagłówek tabeli
        header_frame = ctk.CTkFrame(self.param_section, fg_color="#333333", corner_radius=8)
        header_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(header_frame, text="Parameter", font=("Arial", 12, "bold"), text_color="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(header_frame, text="Value", font=("Arial", 12, "bold"), text_color="white").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(header_frame, text="Description", font=("Arial", 12, "bold"), text_color="white").grid(row=0, column=2, padx=10, pady=5, sticky="w")

        # Tabela parametrów
        self.table_frame = ctk.CTkFrame(self.param_section, fg_color="transparent")
        self.table_frame.pack(fill="x", padx=10, pady=5)

        row = 0
        for param, (default, desc, validator) in self.default_values.items():
            name_label = ctk.CTkLabel(self.table_frame, text=param, text_color="white", font=("Arial", 11))
            name_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

            if param == "Loss Function":
                # Dropdown dla parametru z listą opcji
                widget = ctk.CTkComboBox(self.table_frame, values=self.loss_options)
                widget.set(default)
            else:
                # Pole tekstowe z domyślną wartością
                widget = ctk.CTkEntry(self.table_frame)
                widget.insert(0, default)

            widget.configure(state="disabled")
            widget.grid(row=row, column=1, padx=10, pady=5, sticky="we")

            desc_label = ctk.CTkLabel(self.table_frame, text=desc, text_color="grey", font=("Arial", 10))
            desc_label.grid(row=row, column=2, padx=10, pady=5, sticky="w")

            self.param_entries[param] = (widget, validator)
            row += 1

        # Umożliwienie rozciągania kolumny z wartością
        self.table_frame.grid_columnconfigure(1, weight=1)

    def add_parameters_section(self):
        # Dodanie sekcji parametrów
        ctk.CTkLabel(self.param_section, text="Model Parameters", font=("Arial", 14, "bold"), text_color="white").pack(pady=(10, 0))
        self.setup_parameter_table()
        self.train_button.pack(pady=(20, 10))

    def select_train_data(self):
        file_path = filedialog.askopenfilename(title="Select Training Data File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.train_data_path = file_path
            self.train_path_label.configure(text=file_path, text_color="green")

    def select_test_data(self):
        file_path = filedialog.askopenfilename(title="Select Testing Data File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.test_data_path = file_path
            self.test_path_label.configure(text=file_path, text_color="green")

    def confirm_paths(self):
        if self.train_data_path and self.test_data_path:
            self.data_manager.training_data_path = self.train_data_path
            self.data_manager.testing_data_path = self.test_data_path
            self.status_label.configure(text="Paths confirmed successfully!", text_color="green")
            self.param_section.pack(fill="x", padx=20, pady=(10, 20))
            self.add_parameters_section()
            self.enable_parameters()
        else:
            self.status_label.configure(text="Please select both training and testing data files.", text_color="red")

    def enable_parameters(self):
        for widget, _ in self.param_entries.values():
            widget.configure(state="normal")
        self.train_button.configure(state="normal")

    def train_model(self):
        params = {}
        for key, (widget, validator) in self.param_entries.items():
            value = widget.get()
            if validator == "int" and not value.isdigit():
                self.status_label.configure(text=f"Invalid value for {key}. Must be an integer.", text_color="red")
                return
            if validator == "float":
                try:
                    float(value)
                except ValueError:
                    self.status_label.configure(text=f"Invalid value for {key}. Must be a float.", text_color="red")
                    return
            params[key] = value
        print("Training with parameters:", params)  
        self.status_label.configure(text="Training started...", text_color="blue")
