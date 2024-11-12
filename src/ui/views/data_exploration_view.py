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

        self.convert_to_string_button = ctk.CTkButton(self, text="Convert All Columns to String",command=self.convert_all_to_string)
        self.convert_to_string_button.pack(pady=(10, 5), fill="x")

        self.delete_column_label = ctk.CTkLabel(self, text="Select Column to Delete", font=("Arial", 14))
        self.delete_column_label.pack(pady=(10, 5))

        self.delete_column_var = ctk.StringVar()
        self.delete_column_select = ctk.CTkOptionMenu(self, variable=self.delete_column_var, values=[], command=self.on_delete_column_selected)
        self.delete_column_select.pack(pady=(5, 5), fill="x")

        self.delete_column_button = ctk.CTkButton(self, text="Delete Selected Column", fg_color="#c24c4c", hover_color="#9c3636",command=self.delete_selected_column)
        self.delete_column_button.pack(pady=(5, 10), fill="x")

        self.text_stats_label = ctk.CTkLabel(self, text="Text Length Statistics", font=("Arial", 16, "bold"))
        self.text_stats_label.pack(pady=(20, 5))

        self.column_var = ctk.StringVar()
        self.column_select = ctk.CTkOptionMenu(self, variable=self.column_var, values=[], command=self.on_column_selected)
        self.column_select.pack(pady=(10, 5), fill="x")

        self.text_stats_table = UniversalTable(self, data_list=[], empty_message="No text statistics available")
        self.text_stats_table.pack(pady=5, fill="both", expand=True)

        self.show_plot_button = ctk.CTkButton(self, text="Show Text Length Distribution", fg_color="#31459e", hover_color="#202b5c",command=self.show_text_length_distribution)
        self.show_plot_button.pack(pady=10, fill="x")

        self.display_basic_info()
        self.populate_column_options()
        self.populate_delete_column_options()
        self.populate_columns_table()
        self.check_all_columns_are_strings()

    def populate_column_options(self):
        columns = [col for col in self.data_manager.get_data().columns if self.data_manager.get_data()[col].dtype == 'string']
        self.column_select.configure(values=columns if columns else ["No text columns available"])
        self.column_var.set(columns[0] if columns else "")

    def populate_delete_column_options(self):
        columns = list(self.data_manager.get_data().columns)
        self.delete_column_select.configure(values=columns if columns else ["No columns available"])
        self.delete_column_var.set(columns[0] if columns else "")

    def populate_columns_table(self):
        column_data = [{"Column": col, "Data Type": str(dtype)} for col, dtype in self.data_manager.get_basic_info()["Data Types"].items()]
        self.columns_table.display_data(column_data)

    def on_column_selected(self, selected_column):
        self.display_text_stats()

    def on_delete_column_selected(self, selected_column):
        pass

    def display_basic_info(self):
        info = self.data_manager.get_basic_info()
        info_data = [
            {"Property": "Number of records", "Value": info.get("Number of records", "N/A")},
            {"Property": "Number of columns", "Value": info.get("Number of columns", "N/A")},
            {"Property": "Columns", "Value": ", ".join(info.get("Columns", []))},
            {"Property": "Data Types", "Value": str(info.get("Data Types", {}))}
        ]
        self.info_table.display_data(info_data)

    def display_text_stats(self):
        stats = self.data_manager.get_text_column_stats(self.column_var.get())
        stats_data = [{"Statistic": stat, "Value": value} for stat, value in stats.items()]
        self.text_stats_table.display_data(stats_data)

    def show_text_length_distribution(self):
        column = self.column_var.get()
        if column and column in self.data_manager.get_data():
            text_lengths = self.data_manager.get_data()[column].str.len()
            plt.figure(figsize=(8, 4))
            plt.hist(text_lengths, bins=30, color='skyblue', edgecolor='black')
            plt.title(f"Text Length Distribution for '{column}'")
            plt.xlabel("Text Length")
            plt.ylabel("Frequency")
            plt.show()

    def convert_all_to_string(self):
        self.data_manager.convert_non_string_columns_to_string()
        self.display_basic_info()
        self.populate_columns_table()
        self.populate_column_options()
        self.populate_delete_column_options()
        self.check_all_columns_are_strings()

    def delete_selected_column(self):
        column = self.delete_column_var.get()
        if column and column != "No columns available":
            self.data_manager.remove_column(column)
            self.display_basic_info()
            self.populate_columns_table()
            self.populate_column_options()
            self.populate_delete_column_options()
            self.check_all_columns_are_strings()

    def check_all_columns_are_strings(self):
        all_strings = self.data_manager.are_all_columns_strings()
        self.navigation_bar.set_next_enabled(all_strings)
