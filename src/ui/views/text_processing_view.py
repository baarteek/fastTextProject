import customtkinter as ctk
from ..components.universal_table import UniversalTable
from ..components.progress_dialog import ProgressDialog

class TextProcessingView(ctk.CTkScrollableFrame):
    def __init__(self, master, data_manager=None, navigation_bar=None, **kwargs):
        super().__init__(master, fg_color="#1E1E1E", **kwargs)

        self.data_manager = data_manager
        self.navigation_bar = navigation_bar
        self.is_tokenized = False

        self.column_var = ctk.StringVar()

        self.column_select = ctk.CTkOptionMenu(self, variable=self.column_var, values=[])
        self.column_select.pack(pady=(5, 10), fill="x", expand=True)

        self.normalize_case_button = ctk.CTkButton(self, text="Normalize Case", command=self.normalize_case)
        self.normalize_case_button.pack(pady=5, fill="x", expand=True)

        self.remove_buttons_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        self.remove_buttons_frame.pack(pady=5, fill="x", expand=True)

        self.remove_special_chars_button = ctk.CTkButton(
            self.remove_buttons_frame, 
            text="Remove Special Characters", 
            command=self.remove_special_characters, 
            fg_color="#c24c4c", 
            hover_color="#9c3636"
        )
        self.remove_special_chars_button.pack(side="left", padx=5, fill="x", expand=True)

        self.remove_numbers_button = ctk.CTkButton(
            self.remove_buttons_frame, 
            text="Remove Numbers", 
            command=self.remove_numbers, 
            fg_color="#c24c4c", 
            hover_color="#9c3636"
        )
        self.remove_numbers_button.pack(side="left", padx=5, fill="x", expand=True)

        self.tokenize_button = ctk.CTkButton(self, text="Tokenize Text", command=self.tokenize_text)
        self.tokenize_button.pack(pady=5, fill="x", expand=True)

        self.process_buttons_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        self.process_buttons_frame.pack(pady=5, fill="x", expand=True)

        self.remove_stopwords_button = ctk.CTkButton(
            self.process_buttons_frame, text="Remove Stopwords", command=self.remove_stopwords,
            fg_color="#c24c4c", hover_color="#9c3636", state="disabled"
        )
        self.remove_stopwords_button.pack(side="left", padx=5, fill="x", expand=True)

        self.lemmatize_button = ctk.CTkButton(
            self.process_buttons_frame, text="Lemmatize Text", command=self.lemmatize_text,
            state="disabled"
        )
        self.lemmatize_button.pack(side="left", padx=5, fill="x", expand=True)

        self.processed_data_table = UniversalTable(self, data_list=[], empty_message="No processed data to display")
        self.processed_data_table.pack(pady=5, fill="both", expand=True)

        self.populate_column_options()
        self.display_processed_data()

    def populate_column_options(self):
        string_columns = [col for col in self.data_manager.get_data().select_dtypes(include='string').columns]
        self.column_select.configure(values=["All Columns"] + string_columns)
        if string_columns:
            self.column_var.set("All Columns")

    def normalize_case(self):
        column = self.column_var.get()
        columns_to_process = self._get_columns_to_process(column)
        progress_dialog = ProgressDialog(self, title="Normalizing Case", message="Normalizing text case...")
        for col in columns_to_process:
            self.data_manager.normalize_case(col)
        progress_dialog.stop_progress()
        self.display_processed_data()

    def remove_special_characters(self):
        column = self.column_var.get()
        columns_to_process = self._get_columns_to_process(column)
        progress_dialog = ProgressDialog(self, title="Removing Special Characters", message="Removing special characters...")
        for col in columns_to_process:
            self.data_manager.remove_special_chars(col)
        progress_dialog.stop_progress()
        self.display_processed_data()

    def remove_numbers(self):
        column = self.column_var.get()
        columns_to_process = self._get_columns_to_process(column)
        progress_dialog = ProgressDialog(self, title="Removing Numbers", message="Removing numbers from text...")
        for col in columns_to_process:
            self.data_manager.remove_numbers(col)
        progress_dialog.stop_progress()
        self.display_processed_data()

    def tokenize_text(self):
        column = self.column_var.get()
        columns_to_process = self._get_columns_to_process(column)
        progress_dialog = ProgressDialog(self, title="Tokenizing Text", message="Tokenizing text...")
        for col in columns_to_process:
            self.data_manager.tokenize(col)
        progress_dialog.stop_progress()

        self.is_tokenized = True
        self.remove_stopwords_button.configure(state="normal")
        self.lemmatize_button.configure(state="normal")
        self.disable_initial_buttons()
        self.display_processed_data()

    def disable_initial_buttons(self):
        self.normalize_case_button.configure(state="disabled")
        self.remove_special_chars_button.configure(state="disabled")
        self.remove_numbers_button.configure(state="disabled")

    def remove_stopwords(self):
        column = self.column_var.get()
        columns_to_process = self._get_columns_to_process(column)
        progress_dialog = ProgressDialog(self, title="Removing Stopwords", message="Removing stopwords...")
        for col in columns_to_process:
            self.data_manager.remove_stopwords(col)
        progress_dialog.stop_progress()
        self.display_processed_data()

    def lemmatize_text(self):
        column = self.column_var.get()
        columns_to_process = self._get_columns_to_process(column)
        progress_dialog = ProgressDialog(self, title="Lemmatizing Text", message="Lemmatizing text...")
        for col in columns_to_process:
            self.data_manager.lemmatize_column(col)
        progress_dialog.stop_progress()
        self.display_processed_data()

    def display_processed_data(self):
        if self.data_manager.data is not None:
            processed_data = self.data_manager.get_data().head(50).to_dict("records")
            self.processed_data_table.display_data(processed_data)
        else:
            self.processed_data_table.display_data([{"Message": "No data to display"}])

    def _get_columns_to_process(self, column):
        if column == "All Columns":
            return self.data_manager.get_data().columns
        else:
            return [column]
