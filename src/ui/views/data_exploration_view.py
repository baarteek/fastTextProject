import customtkinter as ctk
import matplotlib.pyplot as plt
from ..components.universal_table import UniversalTable

class DataExplorationView(ctk.CTkScrollableFrame):
    def __init__(self, master, data_manager=None, navigation_bar=None, **kwargs):
        super().__init__(master, fg_color="#1E1E1E", **kwargs)
        
        self.data_manager = data_manager
        self.navigation_bar = navigation_bar

        self.info_section_label = ctk.CTkLabel(self, text="Dataset Information", font=("Arial", 16, "bold"))
        self.info_section_label.pack(pady=(10, 5))

        self.info_table = UniversalTable(self, data_list=[], empty_message="No dataset information available")
        self.info_table.pack(pady=5, fill="both", expand=True)

        self.columns_section_label = ctk.CTkLabel(self, text="All Columns", font=("Arial", 16, "bold"))
        self.columns_section_label.pack(pady=(20, 5))

        self.columns_table = UniversalTable(self, data_list=[], empty_message="No columns available")
        self.columns_table.pack(pady=5, fill="both", expand=True)

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

        self.text_stats_label = ctk.CTkLabel(self, text="Text Length Statistics", font=("Arial", 16, "bold"))
        self.text_stats_label.pack(pady=(20, 5))

        self.column_var = ctk.StringVar()
        self.column_select = ctk.CTkOptionMenu(self, variable=self.column_var, values=[], command=self.on_column_selected)
        self.column_select.pack(pady=(10, 5), fill="x")

        self.text_stats_table = UniversalTable(self, data_list=[], empty_message="No text statistics available")
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
        column_data = [{"Column": col, "Data Type": str(dtype)} for col, dtype in self.data_manager.get_basic_info()["Data Types"].items()]
        self.columns_table.display_data(column_data)

    def on_column_selected(self, selected_column):
        self.display_text_stats()

    def display_basic_info(self):
        info = self.data_manager.get_basic_info()
        info_data = [
            {"Property": "Number of records", "Value": info["Number of records"]},
            {"Property": "Number of columns", "Value": info["Number of columns"]},
            {"Property": "Columns", "Value": ", ".join(info["Columns"])},
            {"Property": "Data Types", "Value": str(info["Data Types"])}
        ]
        self.info_table.display_data(info_data)

    def display_missing_values(self):
        missing_values = self.data_manager.get_missing_values()
        missing_data = [{"Column": col, "Missing Values": count} for col, count in missing_values.items() if count > 0]
        if missing_data:
            self.missing_table.display_data(missing_data)
            self.fill_above_button.configure(state="normal")
            self.fill_below_button.configure(state="normal")
        else:
            self.missing_table.display_data([{"Column": "No missing values", "Missing Values": ""}])
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
        stats_data = [{"Statistic": stat, "Value": value} for stat, value in stats.items()]
        self.text_stats_table.display_data(stats_data)

    def show_text_length_distribution(self):
        text_lengths = self.data_manager.get_data()[self.column_var.get()].str.len()
        plt.figure(figsize=(8, 4))
        plt.hist(text_lengths, bins=30, color='skyblue', edgecolor='black')
        plt.title(f"Text Length Distribution for '{self.column_var.get()}'")
        plt.xlabel("Text Length")
        plt.ylabel("Frequency")
        plt.show()
