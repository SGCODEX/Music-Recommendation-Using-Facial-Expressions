## Music-Recommendation-Using-Facial-Expressions

Please give us a ⭐ and fork this repo to get started. Thank you 🙌🙌.

### Project Overview

This Python-based application uses OpenCV for real-time facial detection and a pre-trained deep learning model (fer2013_mini_XCEPTION.102-0.66.hdf5) to recognize and analyze facial expressions from a live webcam feed. Based on the detected emotion—such as happiness, sadness, anger, or neutrality, it constructs a mood-specific YouTube search query and opens music suggestions in the user’s browser.

By combining computer vision, deep learning, and web integration, this project demonstrates how emotion-based AI systems can enhance user experience through intelligent, real-time content recommendation.

### Installation

1. **Clone the Repository**:
```bash
   git clone https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions.git
   ```

2. **Navigate to the project directory**:
```bash
   cd Music-Recommendation-Using-Facial-Expressions
   ```

3. **(Mac Users) Create and activate a virtual environment**:
```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Dependencies**:
```bash
   pip install -r requirements.txt --quiet
   ```
   Streamlit should already be installed via requirements.txt, but if not, install it manually using `pip install streamlit.`
   
***Note for macOS users:***
- Use `python3` instead of `python` if the default version is Python 2.
- Use `source venv/bin/activate` to activate the virtual environment
- Grant camera access: *System Settings > Privacy > Camera > Enable Terminal or VS Code*
- If you face OpenCV issues, try `xcode-select --install` to install developer tools
    
### How to Run & Interface Options

This project supports three ways to interact with the emotion-based music recommendation system:

**a)CLI Mode (Terminal)**
- Run the core logic directly via terminal (no GUI).
    ```bash
    python code/ui_interfaces/cli_main.py
    ```
**b)Web Interface (Streamlit)**
- Clean, browser-based UI using Streamlit.
    ```bash
    streamlit run code/ui_interfaces/app_local_streamlit.py
    ```
**c)Desktop App (PySimpleGUI)**
- Native desktop GUI that runs as a standalone application.
    ```bash
    python code/ui_interfaces/app_PySimpleGUI.py
    ```
**Ignore - Deployed File**
    ```
    streamlit run code/deployment/app.py
    ```

### Core Tech Stack & Libraries

- Python: Primary programming language here, for its versatility and extensive libraries.
- OpenCV: For real-time image and video processing, including facial detection.
- TensorFlow and Keras: For building and training the deep learning model to recognize facial expressions.
- fer2013_mini_XCEPTION.102-0.66.hdf5: A pre-trained model for facial emotion recognition.
- webbrowser: To open web pages, specifically YouTube search results.
- requests: For making HTTP requests to interact with web APIs (e.g., YouTube search)

### How it Works / Usage

1.  **Facial Detection:**
    - Captures webcam feed.
    - Detects faces using OpenCV.
2.  **Emotion Recognition:**
      - Detected faces are processed by the trained model.
      - The model predicts the dominant emotion (e.g., happy, sad, angry, neutral).
      - Script captures the emotion when we click on the screen, the clicked emotion is stored as current emotion
3.  **Music Recommendation:**
      - The script constructs a YouTube search query based on the emotion detected.
      - The `webbrowser` module opens the search results in your default browser.

- Watch & Contribute to Community Demo Videos here: [Demo Videos](https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions/blob/contribution/code/new_models/demo.md)
- Example Demo Video: [Demo Video for CLI Interface](https://www.youtube.com/watch?v=Qj5yUBjSr7I)

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

We welcome all contributions. Whether it's code, documentation, UI improvements, or demos — your contributions are appreciated.
**If you have introduced a new Computer Vision Library based code or new model or using new library (such as fer), Please submit final code in new_models folder.**
Steps to Contribute:

- Fork the repository
- Create a new branch
- Make your changes
- Submit a Pull Request following the template

Here are a few useful resources to help you get started:
- For contributions, [Check out the contribution guide](https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions/blob/main/CONTRIBUTING.md) .

### PR Template

Please submit all PRs in this format: [PR Template](https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions/blob/main/CONTRIBUTING.md#pr-template)

### License

This project is licensed under the [MIT License](https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions/blob/main/LICENSE)

### Contact Us
For questions or issues, contact:
shivampilot2004@gmail.com
