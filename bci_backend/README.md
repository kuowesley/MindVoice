
# Django EEG Autoencoder Classifier

This Django project implements an API for classifying EEG signals using a pretrained autoencoder model. The API accepts EEG data in JSON format, performs prediction using the autoencoder classifier, and returns the predicted label along with the provided timestamp and username.

## Setup

To get started with this project, follow these steps:

### Requirements
See the [pyproject.toml](pyproject.toml) file for the required Python packages. The project uses [Poetry](https://python-poetry.org/) for dependency management.

### Installation
1. Install the required Python packages:

```bash
poetry install
```

2. Initialize the database:

```bash
poetry run python bci_backend.py migrate
```

### Downloading the Model
In your `${repository}/bci_backend` directory, run the following commands to download the model file:
```bash
pip install gdown
gdown "https://drive.google.com/uc?id=1SK0MyAoj-un3s-YN4sfKRdFS6OjrABfJ"
mv best_model.pth ./model/eeg_CNNautoencoder_classifier_72.07.pth
```

### Run Unit Tests
```bash
echo "DEV_MODE=True" > .env
poetry run pytest --cov=analyzeapp
```

### Start The Server
To start the Django development server, run:

```bash
echo "DEV_MODE=True" > .env
poetry run python bci_backend.py runserver 0.0.0.0:8000 
```

The API will be available at `http://127.0.0.1:8000/api/analyze/`.

## REST APIs

To use the API, send a POST request to `/api/analyze/` with a JSON payload containing the EEG data, timestamp, and username. Example payload:

```json
{
  "data": [/* Your EEG data array */],
  "time": "2023-01-01T12:00:00",
  "UserName": "JohnDoe"
}
```

## Enter virtual environment in command line

```bash
poetry shell
```

## Deployment
### Deploying the Django Application
(TODO)
### Deploying the Model
See: [EEG Model Inference - Deployment](./model/README.md#deployment)

## Contributing

Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.