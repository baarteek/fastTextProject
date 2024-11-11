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

        self.text_stats_label = ctk.CTkLabel(self, text="Text Length Statistics", font=("Arial", 16, "bold"))
        self.text_stats_label.pack(pady=(20, 5))

        self.column_var = ctk.StringVar()
        self.column_select = ctk.CTkOptionMenu(self, variable=self.column_var, values=[], command=self.on_column_selected)
        self.column_select.pack(pady=(10, 5), fill="x")

        self.text_stats_table = UniversalTable(self, data_list=[], empty_message="No text statistics available")
        self.text_stats_table.pack(pady=5, fill="both", expand=True)

        self.show_plot_button = ctk.CTkButton(self, text="Show Text Length Distribution", fg_color="#31459e", hover_color="#202b5c", command=self.show_text_length_distribution)
        self.show_plot_button.pack(pady=10, fill="x")

        self.display_basic_info()
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
