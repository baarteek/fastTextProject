import customtkinter as ctk
from tkinter import filedialog
from modules.fasttext_manager import FastTextManager

class ModelConfigurationView(ctk.CTkFrame):
    def __init__(self, master, fasttext_manager=None, navigation_bar=None, **kwargs):
        super().__init__(master, fg_color="#1E1E1E", **kwargs)
        
        self.fasttext_manager = fasttext_manager or FastTextManager()
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
            "Min Count": ("1", "Minimum count of word occurrences", "int")
        }

        self.loss_options = ["softmax", "ova"]
        self.parameters_added = False
        self.save_button = None 

        self.create_ui()

    def create_ui(self):
        title_label = ctk.CTkLabel(self, text="Model Training Configuration", 
                                  font=("Arial", 16, "bold"), text_color="white")
        title_label.pack(pady=(20, 10))
        
        self.create_file_selection_section()
        
        self.param_section = ctk.CTkScrollableFrame(self, fg_color="#2b2b2b", corner_radius=8)
        self.param_section.pack_forget()

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
        if self.parameters_added:
            return

        header_frame = ctk.CTkFrame(self.param_section, fg_color="#333333", corner_radius=8)
        header_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(header_frame, text="Parameter", font=("Arial", 12, "bold"), text_color="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(header_frame, text="Value", font=("Arial", 12, "bold"), text_color="white").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(header_frame, text="Description", font=("Arial", 12, "bold"), text_color="white").grid(row=0, column=2, padx=10, pady=5, sticky="w")

        self.table_frame = ctk.CTkFrame(self.param_section, fg_color="transparent")
        self.table_frame.pack(fill="x", padx=10, pady=5)

        row = 0
        for param, (default, desc, validator) in self.default_values.items():
            name_label = ctk.CTkLabel(self.table_frame, text=param, text_color="white", font=("Arial", 11))
            name_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

            if param == "Loss Function":
                widget = ctk.CTkComboBox(self.table_frame, values=self.loss_options)
                widget.set(default)
            else:
                widget = ctk.CTkEntry(self.table_frame)
                widget.insert(0, default)

            widget.configure(state="normal")
            widget.grid(row=row, column=1, padx=10, pady=5, sticky="we")

            desc_label = ctk.CTkLabel(self.table_frame, text=desc, text_color="grey", font=("Arial", 10))
            desc_label.grid(row=row, column=2, padx=10, pady=5, sticky="w")

            self.param_entries[param] = (widget, validator)
            row += 1

        self.table_frame.grid_columnconfigure(1, weight=1)

        self.save_button = ctk.CTkButton(self.param_section, text="Save Parameters", fg_color="#4CAF50", command=self.save_parameters)
        self.save_button.pack(pady=(20, 10))

        self.parameters_added = True

    def confirm_paths(self):
        if self.train_data_path and self.test_data_path:
            self.fasttext_manager.set_train_file(self.train_data_path)
            self.fasttext_manager.set_test_file(self.test_data_path)
            self.status_label.configure(text="Paths confirmed successfully!", text_color="green")
            self.param_section.pack(fill="both", expand=True, padx=20, pady=(10, 20))
            self.setup_parameter_table()
        else:
            self.status_label.configure(text="Please select both training and testing data files.", text_color="red")

    def save_parameters(self):
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
        
        self.fasttext_manager.set_params(params)
        self.status_label.configure(text="Parameters saved successfully!", text_color="green")
        self.navigation_bar.set_next_enabled(True)

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
