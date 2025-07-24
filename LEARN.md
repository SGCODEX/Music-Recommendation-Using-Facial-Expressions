# LEARN.md - Onboarding Guide for Music Recommendation via Facial Emotion

Welcome to the Music-Recommendation-Using-Facial-Expressions project! This guide reflects existing repository content and key GitHub sections to help you navigate and contribute easily.

## Contents
1. [Project Overview](#project-overview)  
2. [Key Features](#key-features)  
3. [Directory Layout](#directory-layout)  
4. [Tech Stack](#tech-stack)
5. [Interface Options](#interface-options)  
6. [Getting Started Locally](#getting-started-locally)  
7. [Dependencies](#dependencies)  
8. [How to Contribute](#how-to-contribute) 
9. [How to Extend the Project](#how-to-extend-the-project)  
10. [Debugging Tips](#debugging-tips) 
11. [Additional Resources](#additional-resources)  
12. [Next Steps](#next-steps)  
13. [Code of Conduct](#code-of-conduct)
14. [License](#license) 

---

## Project Overview
This project is a Python-based application that uses OpenCV for real-time facial detection and a pre-trained deep learning model (fer2013_mini_XCEPTION.102-0.66.hdf5) to recognize and analyze facial expressions. By capturing live video feed from the user’s webcam, it identifies the user’s emotions—such as happiness, sadness, anger, or neutrality—based on facial cues.

Once the emotion is detected, the application constructs a YouTube search query tailored to the identified mood. Using the webbrowser module, the application automatically opens relevant YouTube search results in the user’s default browser, allowing them to access music that aligns with their current emotional state. The requests library further supports this functionality by enabling API interactions for a smoother YouTube search experience.

This project combines elements of computer vision and deep learning with web integration to create a personalized and interactive music recommendation system. It demonstrates the potential of AI-powered emotion detection in real-world applications, where user experience can be enhanced through real-time responsiveness and intelligent content recommendations.

---
<table>
  <tr>
    <td width="50%">
      <img
        src="https://i.ibb.co/Jj1FBCD0/Screenshot-2025-07-22-204754.png"
        alt="Screenshot 1"
        width="100%"
      />
    </td>
    <td width="50%">
      <img
        src="https://i.ibb.co/23Cbp7mB/Screenshot-2025-07-22-205043.png"
        alt="Screenshot 2"
        width="100%"
      />
    </td>
  </tr>
</table>


## Key Features
1. **Real-time Facial Detection and Emotion Recognition**  
   - Captures live video from the webcam using OpenCV.  
   - Uses a pre-trained model (`fer2013_mini_XCEPTION.102-0.66.hdf5`) to identify emotions like happiness, sadness, anger, and neutrality.

2. **Emotion-Based YouTube Search and Recommendation**  
   - Constructs YouTube search queries based on detected emotions.  
   - Opens results automatically in the default browser via the `webbrowser` module.  
   - Optionally leverages `requests` for API-based searches.

3. **Intuitive User Interface**  
   - Provides simple CLI, Streamlit, and PySimpleGUI interfaces.  
   - Displays detected emotion in real time.  
   - Shows a clear visual of search results.

4. **Customization & Considerations**  
   - Swap or fine-tune models for improved accuracy.  
   - Tweak search query logic to refine recommendations.  
   - Enhance the front-end GUI for a better user experience.  
   - Be mindful of privacy when processing facial data.

---

## Directory Layout
```
Music-Recommendation-Using-Facial-Expressions/
├── code/
│   ├── deployment/             # Streamlit deployment script (app.py)
│   ├── model/                  # Pre-trained model files
│   ├── new_models/             # Additional or alternative models
│   └── ui_interfaces/          # CLI, Streamlit, and PySimpleGUI scripts
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LEARN.md                    # This guide
├── LICENSE
├── README.md
├── packages.txt
├── requirements.txt
├── runtime.txt
```

---
## Tech Stack
- **Python 3.8+**  
- **OpenCV** for webcam video capture & face detection  
- **TensorFlow & Keras** (Xception-based model) for emotion classification  
- **Streamlit** for web UI  
- **PySimpleGUI** for desktop GUI  
- **webbrowser** for launching YouTube searches  
---
## Code Structure Deep Dive


- **code/model/**  
  Contains the pre-trained emotion-recognition model `fer2013_mini_XCEPTION.102-0.66.hdf5`.

- **code/new_models/**  
  Stores any additional or experimental `.hdf5` models here.

- **code/ui_interfaces/cli_main.py**  
  - Captures webcam frames via OpenCV  
  - Converts to grayscale, detects faces (Haar cascades embedded in this script)  
  - Loads the `.hdf5` model and predicts emotion  
  - Maps emotion → YouTube keywords and opens the browser (`webbrowser.open()`)

- **code/ui_interfaces/app_local_streamlit.py**  
  - Initializes a Streamlit layout: video feed, emotion label, and “Play Music” button  
  - On button click, runs the same detection + recommendation pipeline as in `cli_main.py`

- **code/ui_interfaces/app_PySimpleGUI.py**  
  - Builds a desktop GUI window with live camera feed  
  - Displays current emotion label  
  - “Play Music” button triggers YouTube search logic

- **code/deployment/app.py**  
  - Entry point for deploying the Streamlit app (e.g., to Heroku or Streamlit Cloud)  
  - Wraps `app_local_streamlit.py` logic for production environments

---
## Interface Options
- **CLI Mode:**  
  ```bash
  python code/ui_interfaces/cli_main.py
  ```
- **Streamlit Web App:**  
  ```bash
  streamlit run code/ui_interfaces/app_local_streamlit.py
  ```
- **PySimpleGUI Desktop App:**  
  ```bash
  python code/ui_interfaces/app_PySimpleGUI.py
  ```

---

## Getting Started Locally
From **[README.md](README.md)**:
```bash
git clone https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions.git
cd Music-Recommendation-Using-Facial-Expressions
pip install -r requirements.txt --quiet
```
---

## Dependencies
All Python dependencies are listed in **requirements.txt** and **packages.txt**. Install with:
```bash
pip install -r requirements.txt --quiet
```
---

## How to Contribute
As detailed in **[CONTRIBUTING.md](CONTRIBUTING.md)**:
1. Fork the repository  
2. Create a branch:  
   ```bash
   git checkout -b feature/your-feature
   ```  
3. Make changes and commit with a clear message  
4. Push to your fork and open a Pull Request against `main`

---

## How to Extend the Project
Check the **Issues** tab on GitHub for open labels like `enhancement`, `feature`, or `good first issue` to find areas needing new functionality. Comment on an issue you’d like to tackle to let maintainers know, then follow the standard fork-and-pull workflow.

When contributing, consider:

=> Code Quality: Follow existing patterns and conventions

=> Documentation: Update this LEARN.md file when adding features

=> Testing: Manually test all functionality

=> User Experience: Ensure changes enhance usability

---

## Debugging Tips
- Confirm camera index and permissions if the webcam isn’t detected.  
- Ensure the model file exists under `code/model/`.  
- Verify that dependencies from **requirements.txt** are installed if imports fail.

---

## Additional Resources
- **[README.md](README.md)**: Quick start and overview  
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Contribution guidelines  
- **GitHub Issues**: Track feature requests and bugs  
- **GitHub Actions**: Check the **Actions** tab for CI status  
---

## Next Steps

1. **Explore the Code**: Open each file and read through the comments  
2. **Make Changes**: Try modifying colors, text, or functionality  
3. **Share Your Work**: Create a pull request with your improvements  
---

## Code of Conduct
Please review **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** for community guidelines and standards before contributing.

---

## License
This project is licensed under the terms of the **MIT License** found in **LICENSE**.
