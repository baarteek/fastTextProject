import pandas as pd
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import re

nlp = spacy.load("en_core_web_sm")

class DataManager:
    def __init__(self):
        self.data = None
        self.train_data = None
        self.test_data = None

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
            self.data[column] = self.data[column].str.replace(r'\s{2,}', ' ', regex=True)


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

    def add_fasttext_prefix(self, label_column):
        if self.data is not None and label_column in self.data.columns:
            self.data[label_column] = self.data[label_column].apply(
                lambda x: f"__label__{str(x).replace(' ', '_')}" if x is not None and not str(x).startswith("__label__") else x
            )

            def create_fasttext_line(row):
                label = row[label_column] if row[label_column] is not None else ""
                other_columns = " ".join(
                    str(row[col]) for col in self.data.columns 
                    if col != label_column and row[col] is not None
                )
                return f"{label} {other_columns}".strip()

            self.data["fasttext_line"] = self.data.apply(create_fasttext_line, axis=1)
            print("FastText lines created successfully. Check the 'fasttext_line' column.")


    def split_data(self, split_ratio):
        train_data = self.data.sample(frac=split_ratio, random_state=1)
        test_data = self.data.drop(train_data.index)
        self.train_data = train_data
        self.test_data = test_data

    def get_train_data(self):
        return self.train_data

    def get_test_data(self):
        return self.test_data
    
    def convert_tokenized_to_string(self, column):
        if self.data is not None and column in self.data.columns:
            try:
                self.data[column] = self.data[column].apply(
                    lambda x: " ".join(x) if isinstance(x, list) else str(x)
                )
                print(f"Column '{column}' has been converted to strings.")
            except Exception as e:
                print(f"Error converting tokenized data to strings: {e}")
        else:
            print(f"Error: Column '{column}' not found in the data.")

    def save_splits(self, train_file_path, test_file_path, text_column="fasttext_line"):
        if self.train_data is not None and self.test_data is not None:
            try:
                if text_column not in self.train_data.columns or text_column not in self.test_data.columns:
                    print(f"Error: Column '{text_column}' not found. Run 'add_fasttext_prefix' first.")
                    return
                
                def clean_text(text):
                    if isinstance(text, list):
                        text = " ".join(text)
                    text = str(text)
                    text = re.sub(r'[^a-zA-Z0-9_\s]', '', text)
                    text = re.sub(r'\s{2,}', ' ', text)
                    return text.strip()

                self.train_data[text_column] = self.train_data[text_column].apply(clean_text)
                self.test_data[text_column] = self.test_data[text_column].apply(clean_text)

                with open(train_file_path, "w", encoding="utf-8") as train_file:
                    train_file.write("\n".join(self.train_data[text_column].dropna()))
                
                with open(test_file_path, "w", encoding="utf-8") as test_file:
                    test_file.write("\n".join(self.test_data[text_column].dropna()))

                print(f"Train data saved to: {train_file_path}")
                print(f"Test data saved to: {test_file_path}")
            except Exception as e:
                print(f"Error saving splits: {e}")
        else:
            print("Error: Train or test data is not available. Make sure to split the data first.")






