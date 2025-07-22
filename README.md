## Music-Recommendation-Using-Facial-Expressions

Please give us a ⭐ and fork this repo to get started. Thank you 🙌🙌.

### Project Overview

This project is a Python-based application that uses OpenCV for real-time facial detection and a pre-trained deep learning model (fer2013_mini_XCEPTION.102-0.66.hdf5) to recognize and analyze facial expressions. By capturing live video feed from the user’s webcam, it identifies the user’s emotions—such as happiness, sadness, anger, or neutrality—based on facial cues.

Once the emotion is detected, the application constructs a YouTube search query tailored to the identified mood. Using the webbrowser module, the application automatically opens relevant YouTube search results in the user’s default browser, allowing them to access music that aligns with their current emotional state. The requests library further supports this functionality by enabling API interactions for a smoother YouTube search experience.

This project combines elements of computer vision and deep learning with web integration to create a personalized and interactive music recommendation system. It demonstrates the potential of AI-powered emotion detection in real-world applications, where user experience can be enhanced through real-time responsiveness and intelligent content recommendations.

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions.git
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt --quiet
    ```
    
### How to Run & Interface Options

This project supports three ways to interact with the emotion-based music recommendation system:

**a)CLI Mode (Terminal)**
- Run the core logic directly via terminal (no GUI).
    ```bash
    python code\ui_interfaces\cli_main.py
    ```
**b)Web Interface (Streamlit)**
- Clean, browser-based UI using Streamlit.
    ```bash
    streamlit run code\ui_interfaces\app_local_streamlit.py
    ```
**c)Desktop App (PySimpleGUI)**
- Native desktop GUI that runs as a standalone application.
    ```bash
    python code\ui_interfaces\app_PySimpleGUI.py
    ```
**Ignore - Deployed File**
    ```
    streamlit run code\deployment\app.py
    ```

### Core Tech Stack & Libraries

- Python: As the primary programming language for its versatility and extensive libraries.
- OpenCV: For real-time image and video processing, including facial detection.
- TensorFlow and Keras: For building and training the deep learning model to recognize facial expressions.
- fer2013_mini_XCEPTION.102-0.66.hdf5: A pre-trained model for facial emotion recognition.
- webbrowser: To open web pages, specifically YouTube search results.
- requests: For making HTTP requests to interact with web APIs (e.g., YouTube search).

### How it Works / Usage

1.  **Facial Detection:**
      - The script captures a video feed from your webcam.
      - OpenCV is used to detect faces in each frame.
2.  **Emotion Recognition:**
      - Detected faces are processed by the trained model.
      - The model predicts the dominant emotion (e.g., happy, sad, angry, neutral).
      - Script captures the emotion when we click on the screen, the clicked emotion is stored as current emotion
3.  **Music Recommendation:**
      - Based on the predicted emotion, the script constructs a YouTube search query.
      - The `webbrowser` module opens the search results in your default browser.

- [Demo Video for CLI Interface](https://www.youtube.com/watch?v=Qj5yUBjSr7I)

### Main Features
**1. Real-time Facial Detection and Emotion Recognition:**
   - Uses OpenCV to capture live video feed from the user's webcam.
   - Employs a pre-trained deep learning model (fer2013_mini_XCEPTION.102-0.66.hdf5) to accurately identify facial expressions.
   - Recognizes a range of emotions, including happiness, sadness, anger, and neutrality.

**2. Emotion-Based YouTube Search and Recommendation:** 
   - Utilizes the webbrowser module to automatically open relevant search results in the user's default browser.
   - Leverages the requests library to interact with YouTube's API for a more efficient search process.
   - Constructs a YouTube search query based on the detected emotion

**3. Intuitive User Interface:**
   - Provides a simple and user-friendly interfaces to interact with the application.
   - Displays the detected emotion in real-time.
   - Presents a clear visual representation of the search results.

### Customization & Additional Considerations

  - **Model:** Experiment with different pre-trained models or fine-tune the existing one for more accurate emotion recognition.
  - **Search Queries:** Adjust the search query construction to refine the music recommendations.
  - **User Interface:** Consider creating a user-friendly GUI / Front end to enhance the experience.
  - **Privacy:** Be mindful of privacy concerns when capturing and processing facial data.
  - **Performance:** Optimize the code for real-time performance, especially on resource-constrained devices.
  - **Error Handling:** Implement robust error handling to gracefully handle exceptions.

### Contribution

**NOTE: Please create PRs only to the contribution branch. All others will be automatically closed.**

We welcome contributions to this project. Feel free to fork the repository, make improvements, and submit pull requests.
We value all contributions, whether it's through code, documentation, creating demos or just spreading the word.
**If you have introduced a new Computer Vision Library based code or new model or using new library (such as fer), Please submit final code in new_models folder.**
Here are a few useful resources to help you get started:
- For contributions, [Check out the contribution guide](https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions/blob/main/CONTRIBUTING.md) .

### PR Template

Please submit all PRs in this format: [PR Template](https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions/blob/main/CONTRIBUTING.md#pr-template)

### License

This project is licensed under the [MIT License](https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions/blob/main/LICENSE)

### Contact Us

For any questions or issues, please contact us at shivampilot2004@gmail.com
