# EEG Model Inference
This directory contains the code for the EEG model inference.

## Build And Run
> **Note**: The model inference requires the [`cog`](https://replicate.com/docs/guides/push-a-model#install-cog)  CLI tool, which is already installed in the `poetry` environment.
To build and run the model inference, follow the instructions below:
1. Install the dependencies and enable the `poetry` virtual environment:
   ```bash
   poetry install && poetry shell
   ```
2. Run the model inference:
   ```bash
   cog predict -i eeg_data=@../tests/thank_you.json
   ```

## Deployment
1. Login to your Replicate account in the terminal:
   > **Note**: Before deploying the model, make sure to have a [Replicate](https://replicate.com/) account.
   ```bash
   cog login
   ```

2. Push the model to Replicate:
   > **Note**: Replace `<your-username>` with your Replicate username and    `<your-model-name>` with the name of your model.
   ```bash
   cog push r8.im/<your-username>/<your-model-name>
   ```