import customtkinter as ctk
from ..components.universal_table import UniversalTable
from ..components.progress_dialog import ProgressDialog

class LabelPreparationView(ctk.CTkScrollableFrame):
    def __init__(self, master, data_manager=None, navigation_bar=None, **kwargs):
        super().__init__(master, fg_color="#1E1E1E", **kwargs)

        self.data_manager = data_manager
        self.column_var = ctk.StringVar()

        self.column_select_label = ctk.CTkLabel(self, text="Select Label Column")
        self.column_select_label.pack(pady=(10, 5))
        
        self.column_select = ctk.CTkOptionMenu(self, variable=self.column_var, values=[])
        self.column_select.pack(pady=(5, 10), fill="x", expand=True)

        self.add_prefix_button = ctk.CTkButton(
            self, text="Add fastText Label Prefix", command=self.add_fasttext_prefix
        )
        self.add_prefix_button.pack(pady=5, fill="x", expand=True)

        self.processed_data_table = UniversalTable(self, data_list=[], empty_message="No prepared labels to display")
        self.processed_data_table.pack(pady=10, fill="both", expand=True)

        self.populate_column_options()
        self.display_processed_data()

    def populate_column_options(self):
        columns = list(self.data_manager.get_data().columns)
        self.column_select.configure(values=columns)
        if columns:
            self.column_var.set(columns[0])

    def add_fasttext_prefix(self):
        column = self.column_var.get()
        progress_dialog = ProgressDialog(self, title="Adding fastText Prefix", message="Adding __label__ prefix to labels...")
        
        self.data_manager.add_fasttext_prefix(column)
        
        progress_dialog.stop_progress()
        self.display_processed_data()

    def display_processed_data(self):
        processed_data = self.data_manager.get_data().head(50).to_dict("records")
        self.processed_data_table.display_data(processed_data)
