### Make new contributions here!!
# 🎨 Emotion-Based Music Recommendation – Gradio UI

This module provides a simple, beautiful, and interactive **frontend interface** using [Gradio](https://www.gradio.app/) to simulate music recommendations based on emotions detected from user-uploaded or webcam images.

---

## 🚀 How It Works

1. The user uploads or captures an image via webcam.
2. A dummy emotion detection function randomly selects one emotion from:
   - 😄 Happy
   - 😢 Sad
   - 😠 Angry
   - 😐 Neutral
   - 😲 Surprised
3. Based on the detected emotion, a matching music playlist is recommended with emojis for an enhanced UX.

---

## 🖥️ Preview

> Once the server is running, the UI looks like this:


🎼 Emotion-based Music Recommendation

Upload your image or take a webcam photo to get music recommendations based on your emotion!
code/new_models/Screenshot 2025-07-23 at 1.18.39 PM.png
code/new_models/Screenshot 2025-07-23 at 1.19.05 PM.png
code/new_models/Screenshot 2025-07-23 at 1.19.31 PM.png



---

## 🛠️ How to Run the UI

### 1. Activate your virtual environment

```bash
source venv/bin/activate

2. Navigate to the UI directory
cd code/new_models/

3. Run the Gradio app
python frontend_gradio_ui.py

4. Open the app in browser

Visit:
http://127.0.0.1:7860

🧾 Requirements
Install Gradio (if not already installed):
pip install gradio

You can also install all project dependencies via:
pip install -r requirements.txt

📁 Project Structure
code/
└── new_models/
    ├── frontend_gradio_ui.py   # Main Gradio UI file
    └── README_UI.md            # Documentation (this file)
👩‍💻 Developer Note
This frontend does not use actual facial emotion recognition logic yet — instead, it simulates detection with random choices for demonstration purposes. You can easily plug in a real model into the detect_emotion(image) function.


🙋‍♀️ Contributor
Developed with ❤️ by @Sanskriti10247
As part of GirlScript Summer of Code 2025

📄 License
This project is licensed under the MIT License.