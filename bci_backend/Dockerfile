# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y netcat

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install poetry
COPY pyproject.toml .
RUN poetry config virtualenvs.create false && poetry install

# Copy project bci_backend to the container
COPY . .

# Install gdown
RUN pip install gdown

# Download the model to the existing analyzeapp dir
RUN gdown https://drive.google.com/uc?id=1SK0MyAoj-un3s-YN4sfKRdFS6OjrABfJ
RUN mv best_model.pth analyzeapp/eeg_CNNautoencoder_classifier_72.07.pth

# Expose the port the app runs on
EXPOSE 8000

# Run the application: poetry run python bci_backend.py runserver 0.0.0.0:8000
CMD ["poetry", "run", "python", "bci_backend.py", "runserver", "0.0.0.0:8000"]