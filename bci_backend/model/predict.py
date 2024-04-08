import json
import os
import torch
from cog import BasePredictor, Input, Path

try:
    from model.eeg_autoencoder_classifier import EEGAutoencoderClassifier
except ImportError or ModuleNotFoundError:
    from eeg_autoencoder_classifier import EEGAutoencoderClassifier


class Predictor(BasePredictor):
    # constructor
    def __init__(self):
        self.model = EEGAutoencoderClassifier(num_classes=5)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_dir = os.path.dirname(__file__)

    def set_model_dir(self, model_dir: str):
        self.model_dir = model_dir

    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        # model_path = os.path.join(self.model_dir, './eeg_CNNautoencoder_classifier_72.07.pth')
        model_path = os.path.join(self.model_dir, 'eeg_CNNautoencoder_classifier_72.07.pth')
        print("Model size: ", os.path.getsize(model_path))
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

    def predict_local(self, eeg_data) -> int:
        input_tensor = torch.Tensor(eeg_data).to(self.device)
        input_tensor = input_tensor.unsqueeze(0)  # shape: [1, 64, 795]
        with torch.no_grad():
            output = self.model(input_tensor)
            _, predicted = torch.max(output.data, 1)
            predicted_label = predicted.item()
        return predicted_label

    def predict(
            self,
            eeg_data: Path = Input(description="EEG data array"),
    ) -> str:
        """Run a single prediction on the model"""
        with open(eeg_data, 'r') as f:
            eeg_data = f.read()
        data = json.loads(eeg_data).get('data')
        return str(self.predict_local(data))
