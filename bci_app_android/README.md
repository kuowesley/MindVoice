

# EEG Analysis Android App

This Android application is designed to perform EEG (Electroencephalography) data analysis. It allows users to interact with a set of predefined actions, each triggering a unique analysis of EEG data. The app showcases the use of Kotlin for Android development, Retrofit for network requests, and Gson for JSON parsing.

## Features

- **User Actions**: Users can trigger EEG data analysis through five different actions: "Yes", "Help Me", "Stop", "Thank You", and "Hello".
- **Analyze Button**: Reserved for future functionality to initiate EEG data analysis.
- **Dynamic EEG Data Handling**: The app dynamically loads EEG data corresponding to user actions from the application's assets and sends it to a backend server for analysis.
- **Real-time Analysis Results**: Displays the analysis results in real-time, including the label predicted by the backend.

## Project Structure

- `EEGActivity.kt`: Main activity that handles user interactions and displays the analysis results.
- `EEGAdapter.kt`: Manages the network requests to send EEG data and receive analysis results.
- `EEGRetrofitManager.kt`: Configures Retrofit client for network communication.
- `EEGInterface.kt`: Defines the Retrofit interface for EEG data analysis API.
- `EEGCallModel.kt`: Data model for sending EEG data.
- `EEGCallbackModel.kt`: Data model for receiving analysis results.
- `assets/`: Contains `.json` files for each action, representing EEG data to be analyzed.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://your-repository-url.git
   ```
2. **Open the Project in Android Studio**:
   - Launch Android Studio and select "Open an existing Android Studio project".
   - Navigate to the cloned repository and open it.

3. **Add Required Dependencies**:
   - Ensure the following dependencies are included in your `build.gradle` file:
     ```gradle
     implementation 'com.squareup.retrofit2:retrofit:2.9.0'
     implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
     implementation 'com.google.code.gson:gson:2.8.6'
     ```

4. **Running the App**:
   - Use Android Studio's built-in emulator or connect an Android device to run the app.

5. **Adding EEG Data**:
   - Place your `.json` files representing EEG data in the `assets` folder. Each file should match an action (e.g., `yes.json` for the "Yes" action).

## Contributing

We welcome contributions to improve this project. Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Remember to replace `https://your-repository-url.git` with the actual URL of your GitHub repository and adjust the project description, setup instructions, and any other specific details to match your project's requirements.
