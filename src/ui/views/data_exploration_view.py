import customtkinter as ctk
from tkinter import ttk
import matplotlib.pyplot as plt

class DataExplorationView(ctk.CTkScrollableFrame):
    def __init__(self, master, data_manager=None, navigation_bar=None, **kwargs):
        super().__init__(master, fg_color="#1E1E1E", **kwargs)
        
        self.data_manager = data_manager
        self.navigation_bar = navigation_bar

        self.info_section_label = ctk.CTkLabel(self, text="Dataset Information", font=("Arial", 16, "bold"))
        self.info_section_label.pack(pady=(10, 5))

        self.info_table = ttk.Treeview(self, columns=("Property", "Value"), show="headings", height=4)
        self.info_table.heading("Property", text="Property")
        self.info_table.heading("Value", text="Value")
        self.info_table.pack(pady=5, fill="both", expand=True)

        self.columns_section_label = ctk.CTkLabel(self, text="All Columns", font=("Arial", 16, "bold"))
        self.columns_section_label.pack(pady=(20, 5))

        self.columns_table = ttk.Treeview(self, columns=("Column", "Data Type"), show="headings", height=8)
        self.columns_table.heading("Column", text="Column")
        self.columns_table.heading("Data Type", text="Data Type")
        self.columns_table.pack(pady=5, fill="both", expand=True)

        self.missing_label = ctk.CTkLabel(self, text="Missing Values", font=("Arial", 16, "bold"))
        self.missing_label.pack(pady=(10, 5))
        
        self.missing_table = ttk.Treeview(self, columns=("Column", "Missing Values"), show="headings", height=4)
        self.missing_table.heading("Column", text="Column")
        self.missing_table.heading("Missing Values", text="Missing Values")
        self.missing_table.pack(pady=5, fill="both", expand=True)

        self.fill_buttons_frame = ctk.CTkFrame(self, fg_color="#2B2B2B")
        self.fill_buttons_frame.pack(pady=10, fill="x", expand=True)
        
        self.fill_above_button = ctk.CTkButton(self.fill_buttons_frame, text="Fill from Above", command=self.fill_missing_from_above, state="disabled")
        self.fill_above_button.pack(side="left", padx=5, fill="x", expand=True)

        self.fill_below_button = ctk.CTkButton(self.fill_buttons_frame, text="Fill from Below", command=self.fill_missing_from_below, state="disabled")
        self.fill_below_button.pack(side="left", padx=5, fill="x", expand=True)

        self.text_stats_label = ctk.CTkLabel(self, text="Text Length Statistics", font=("Arial", 16, "bold"))
        self.text_stats_label.pack(pady=(20, 5))
        
        self.column_var = ctk.StringVar()
        self.column_select = ctk.CTkOptionMenu(self, variable=self.column_var, values=[], command=self.on_column_selected)
        self.column_select.pack(pady=(10, 5), fill="x")

        self.text_stats_table = ttk.Treeview(self, columns=("Statistic", "Value"), show="headings", height=4)
        self.text_stats_table.heading("Statistic", text="Statistic")
        self.text_stats_table.heading("Value", text="Value")
        self.text_stats_table.pack(pady=5, fill="both", expand=True)

        self.show_plot_button = ctk.CTkButton(self, text="Show Text Length Distribution", command=self.show_text_length_distribution)
        self.show_plot_button.pack(pady=10, fill="x")

        self.display_basic_info()
        self.display_missing_values()
        self.populate_column_options()
        self.populate_columns_table()

    def populate_column_options(self):
        columns = [col for col in self.data_manager.get_data().columns if self.data_manager.get_data()[col].dtype == 'string']
        self.column_select.configure(values=columns if columns else ["No text columns available"])
        self.column_var.set(columns[0] if columns else "")

    def populate_columns_table(self):
        self.columns_table.delete(*self.columns_table.get_children())
        for col, dtype in self.data_manager.get_basic_info()["Data Types"].items():
            self.columns_table.insert("", "end", values=(col, dtype))

    def on_column_selected(self, selected_column):
        self.display_text_stats()

    def display_basic_info(self):
        info = self.data_manager.get_basic_info()
        self.info_table.insert("", "end", values=("Number of records", info["Number of records"]))
        self.info_table.insert("", "end", values=("Number of columns", info["Number of columns"]))
        self.info_table.insert("", "end", values=("Columns", ", ".join(info["Columns"])))
        self.info_table.insert("", "end", values=("Data Types", info["Data Types"]))

    def display_missing_values(self):
        self.missing_table.delete(*self.missing_table.get_children())
        missing_values = self.data_manager.get_missing_values()
        if any(value > 0 for value in missing_values.values()):
            for col, count in missing_values.items():
                if count > 0:
                    self.missing_table.insert("", "end", values=(col, count))
            self.fill_above_button.configure(state="normal")
            self.fill_below_button.configure(state="normal")
        else:
            self.missing_table.insert("", "end", values=("No missing values", ""))
            self.fill_above_button.configure(state="disabled")
            self.fill_below_button.configure(state="disabled")

    def fill_missing_from_above(self):
        self.data_manager.fill_missing_from_above()
        self.display_missing_values()

    def fill_missing_from_below(self):
        self.data_manager.fill_missing_from_below()
        self.display_missing_values()

    def display_text_stats(self):
        stats = self.data_manager.get_text_column_stats(self.column_var.get())
        self.text_stats_table.delete(*self.text_stats_table.get_children())
        for stat_name, value in stats.items():
            self.text_stats_table.insert("", "end", values=(stat_name, value))

    def show_text_length_distribution(self):
        text_lengths = self.data_manager.get_data()[self.column_var.get()].str.len()
        plt.figure(figsize=(8, 4))
        plt.hist(text_lengths, bins=30, color='skyblue', edgecolor='black')
        plt.title(f"Text Length Distribution for '{self.column_var.get()}'")
        plt.xlabel("Text Length")
        plt.ylabel("Frequency")
        plt.show()
