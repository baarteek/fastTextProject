import pandas as pd
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load("en_core_web_sm")

class DataManager:
    def __init__(self):
        self.data = None

    def load_data(self, file_path):
        try:
            if file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                self.data = pd.read_json(file_path, lines=True)
            else:
                print("Unsupported file format. Only CSV and JSON files are supported.")
                return False
            self.data = self.data.convert_dtypes()
            self.data.replace("", None, inplace=True)
            print("Data loaded successfully.")
            return True
        except ValueError as ve:
            print(f"ValueError loading data: {ve}")
            return False
        except FileNotFoundError:
            print("File not found. Please check the file path.")
            return False
        except Exception as e:
            print(f"Unexpected error loading data: {e}")
            return False

    def get_data(self):
        return self.data

    def get_basic_info(self):
        if self.data is not None:
            return {
                "Number of records": len(self.data),
                "Number of columns": len(self.data.columns),
                "Columns": list(self.data.columns),
                "Data Types": self.data.dtypes.to_dict()
            }
        return {}
    
    def are_all_columns_strings(self):
        if self.data is not None and not self.data.empty:
            return all(self.data.dtypes == 'string')
        return False

    def get_missing_values(self):
        if self.data is not None:
            return self.data.isnull().sum().to_dict()
        return {}
    
    def get_missing_values_count(self):
        if self.data is not None:
            return self.data.isnull().any(axis=1).sum()
        return 0

    def fill_missing_from_above(self):
        if self.data is not None:
            self.data.ffill(inplace=True)

    def fill_missing_from_below(self):
        if self.data is not None:
            self.data.bfill(inplace=True)

    def fill_manual(self, column, index, value):
        if self.data is not None:
            if column in self.data.columns and index < len(self.data):
                self.data.at[index, column] = value
                print(self.data.at[index, column])

    def drop_missing_values(self):
        if self.data is not None:
            self.data.dropna(inplace=True)

    def get_duplicates(self):
        if self.data is not None:
            return self.data[self.data.duplicated(keep=False)]
        return pd.DataFrame()

    def get_duplicates_count(self):
        if self.data is not None:
            return self.data.duplicated().sum()
        return 0
    
    def remove_duplicates(self):
        if self.data is not None:
            self.data.drop_duplicates(inplace=True)

    def remove_column(self, column):
        if self.data is not None and column in self.data.columns:
            self.data = self.data.drop(columns=[column])
            return True
        return False

    def get_text_column_stats(self, column):
        if self.data is not None and column in self.data.columns and pd.api.types.is_string_dtype(self.data[column]):
            text_lengths = self.data[column].str.len()
            return {
                "Analyzed Column": column,
                "Average Length": text_lengths.mean(),
                "Min Length": text_lengths.min(),
                "Max Length": text_lengths.max(),
                "Median Length": text_lengths.median()
            }
        return {}
    
    def normalize_case(self, column):
        if self.data is not None and column in self.data.columns and pd.api.types.is_string_dtype(self.data[column]):
            self.data[column] = self.data[column].str.lower()

    def remove_excess_spaces(self, column):
        if self.data is not None and column in self.data.columns and pd.api.types.is_string_dtype(self.data[column]):
            self.data[column] = self.data[column].str.replace('\s{2,}', ' ', regex=True)

    def remove_special_chars(self, column):
        if self.data is not None and column in self.data.columns and pd.api.types.is_string_dtype(self.data[column]):
            self.data[column] = self.data[column].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
            self.remove_excess_spaces(column)
        
    def remove_numbers(self, column):
        if self.data is not None and column in self.data.columns and pd.api.types.is_string_dtype(self.data[column]):
            self.data[column] = self.data[column].str.replace(r'\d+', '', regex=True)
            self.remove_excess_spaces(column)

    def convert_non_string_columns_to_string(self):
        if self.data is not None:
            datetime_columns = self.data.select_dtypes(include=['datetime64[ns]', 'datetime64']).columns
            for col in datetime_columns:
                has_time = self.data[col].dt.hour.any() or self.data[col].dt.minute.any() or self.data[col].dt.second.any()
                if has_time:
                    format_str = '%Y-%m-%d %H:%M:%S'
                else:
                    format_str = '%Y-%m-%d'
                self.data[col] = self.data[col].dt.strftime(format_str).astype('string')
            non_string_columns = self.data.select_dtypes(exclude=['string']).columns
            self.data[non_string_columns] = self.data[non_string_columns].astype('string')

    def tokenize(self, column):
        if self.data is not None and column in self.data.columns:
            if pd.api.types.is_string_dtype(self.data[column]):

                self.data[column] = self.data[column].apply(
                    lambda x: [token.text for token in nlp(x)] if pd.notnull(x) else x
                ).astype('object')

    def remove_stopwords(self, column):
        if self.data is not None and column in self.data.columns:
            stopwords = STOP_WORDS
            self.data[column] = self.data[column].apply(
                lambda tokens: [token for token in tokens if token.lower() not in stopwords] if isinstance(tokens, list) else tokens
            )
    
    def lemmatize_column(self, column):
        if self.data is not None and column in self.data.columns:
            self.data[column] = self.data[column].apply(
                    lambda tokens: [nlp(token)[0].lemma_ for token in tokens] if tokens else tokens
                )

