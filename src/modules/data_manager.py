import pandas as pd

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

    def get_missing_values(self):
        if self.data is not None:
            return self.data.isnull().sum().to_dict()
        return {}

    def fill_missing_from_above(self):
        if self.data is not None:
            self.data.ffill(inplace=True)

    def fill_missing_from_below(self):
        if self.data is not None:
            self.data.bfill(inplace=True)


    def get_text_column_stats(self, column):
        if self.data is not None and column in self.data.columns and self.data[column].dtype == 'string':
            text_lengths = self.data[column].str.len()
            return {
                "Analyzed Column": column,
                "Average Length": text_lengths.mean(),
                "Min Length": text_lengths.min(),
                "Max Length": text_lengths.max(),
                "Median Length": text_lengths.median()
            }
        return {}
