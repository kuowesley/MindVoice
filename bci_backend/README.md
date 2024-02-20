
# Django EEG Autoencoder Classifier

This Django project implements an API for classifying EEG signals using a pretrained autoencoder model. The API accepts EEG data in JSON format, performs prediction using the autoencoder classifier, and returns the predicted label along with the provided timestamp and username.

## Setup

To get started with this project, follow these steps:

### Requirements

- Python 3.8 or higher
- Django
- PyTorch
- Other dependencies listed in `requirements.txt`

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-github-username/your-repository-name.git
cd your-repository-name
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Migrate the database:

```bash
python manage.py migrate
```

### Downloading the Model

Before running the application, you need to download the pretrained model file `eeg_autoencoder_classifier_500.pth` and place it in the `analyzeapp` directory within the project. The model file can be downloaded from the following link:

[Download Pretrained Model](https://example.com/download/model)

Please ensure the model file is located at: `your-repository-name/analyzeapp/eeg_autoencoder_classifier_500.pth`

### Running the Server

To start the Django development server, run:

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/analyze/`.

## Usage

To use the API, send a POST request to `/api/analyze/` with a JSON payload containing the EEG data, timestamp, and username. Example payload:

```json
{
  "data": [/* Your EEG data array */],
  "time": "2023-01-01T12:00:00",
  "UserName": "JohnDoe"
}
```

## Contributing

Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

