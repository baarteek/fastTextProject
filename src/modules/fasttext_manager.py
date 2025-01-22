import fasttext

class FastTextManager:
    def __init__(self):
        self.train_file = None
        self.test_file = None
        self.model = None

        self.params = {
            "lr": 0.1,
            "epoch": 5,
            "wordNgrams": 1,
            "dim": 100,
            "loss": "softmax"
        }

        self.param_key_map = {
            "Epochs": "epoch",
            "Learning Rate": "lr",
            "Dimension": "dim",
            "Word N-Grams": "wordNgrams",
            "Loss Function": "loss"
        }

    def set_train_file(self, train_file_path):
        self.train_file = train_file_path

    def set_test_file(self, test_file_path):
        self.test_file = test_file_path

    def set_params(self, params):
        for user_key, value in params.items():
            if user_key in self.param_key_map:
                internal_key = self.param_key_map[user_key]
            else:
                internal_key = user_key

            if internal_key in ["lr"]:
                self.params[internal_key] = float(value)
            elif internal_key in ["epoch", "wordNgrams", "dim"]:
                self.params[internal_key] = int(value)
            else:
                self.params[internal_key] = value

        print("Parameters saved:", self.params)

    def train_model(self, lr=None, epoch=None, wordNgrams=None, dim=None, loss=None):
        if self.train_file is None:
            print("Train file not set. Please provide a train file path.")
            return False

        lr = lr if lr is not None else self.params["lr"]
        epoch = epoch if epoch is not None else self.params["epoch"]
        wordNgrams = wordNgrams if wordNgrams is not None else self.params["wordNgrams"]
        dim = dim if dim is not None else self.params["dim"]
        loss = loss if loss is not None else self.params["loss"]

        try:
            self.model = fasttext.train_supervised(
                input=self.train_file,
                lr=lr,
                epoch=epoch,
                wordNgrams=wordNgrams,
                dim=dim,
                loss=loss
            )
            print("Model trained successfully.")
            return True
        except Exception as e:
            print(f"Error training model: {e}")
            return False

    def evaluate_model(self, training=False):
        if self.model is None:
            print("No model found. Please train the model before evaluating.")
            return None

        file_path = self.train_file if training else self.test_file
        if file_path is None:
            print(f"{'Training' if training else 'Test'} file not set. Please provide a file path.")
            return None

        try:
            result = self.model.test(file_path)
            number_of_examples = result[0]
            accuracy = result[1]
            recall = result[2]

            print(f"{'Training' if training else 'Test'} evaluation results:")
            print(f"Number of examples: {number_of_examples}")
            print(f"Accuracy: {accuracy:.4f}")

            return {
                "Number of examples": number_of_examples,
                "Accuracy": accuracy,
                "Recall": recall
            }
        except Exception as e:
            print(f"Error evaluating model: {e}")
            return None

    def predict(self, text):
        if self.model is None:
            print("No model found. Please train the model before predicting.")
            return None
        return self.model.predict(text)

    def save_model(self, file_path):
        if self.model is None:
            raise ValueError("No model to save. Please train the model first.")
        try:
            self.model.save_model(file_path)
            print(f"Model saved to {file_path}")
        except Exception as e:
            raise ValueError(f"Error saving model: {e}")
        
    def load_model(self, file_path):
        if not file_path:
            raise ValueError("No file path provided for loading the model.")
        try:
            self.model = fasttext.load_model(file_path)
            print(f"Model loaded successfully from {file_path}")
        except Exception as e:
            raise ValueError(f"Error loading model: {e}")

