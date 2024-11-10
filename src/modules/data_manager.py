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
