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

    def evaluate_model(self):
        if self.model is None:
            print("No model found. Please train the model before evaluating.")
            return None
        if self.test_file is None:
            print("Test file not set. Please provide a test file path.")
            return None

        try:
            result = self.model.test(self.test_file)
            number_of_examples = result[0]
            accuracy = result[1]

            print("Model evaluation results:")
            print(f"Number of examples: {number_of_examples}")
            print(f"Accuracy: {accuracy:.4f}")

            return {
                "Number of examples": number_of_examples,
                "Accuracy": accuracy
            }
        except Exception as e:
            print(f"Error evaluating model: {e}")
            return None


    def predict(self, text):
        if self.model is None:
            print("No model found. Please train the model before predicting.")
            return None
        return self.model.predict(text)
