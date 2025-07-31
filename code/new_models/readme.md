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


<img width="1470" height="811" alt="Screenshot 2025-07-23 at 1 32 06 PM" src="https://github.com/user-attachments/assets/c9dae10c-21c4-47ca-86f2-f1ef08bfa807" />


<img width="1470" height="811" alt="Screenshot 2025-07-23 at 1 19 23 PM" src="https://github.com/user-attachments/assets/3d478b80-6a05-49ca-b078-7b311c4f1309" />


---

## 🛠️ How to Run the UI

### 1. Activate your virtual environment
Run this:

source venv/bin/activate

2. Navigate to the UI directory
   
3. cd code/new_models/

4. Run the Gradio app
   
python frontend_gradio_ui.py

7. Open the app in browser

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

    ├── frontend_gradio_ui.py
    # Main Gradio UI file
    └── README_UI.md          
    # Documentation (this file)

    
👩‍💻 Developer Note
This frontend does not use actual facial emotion recognition logic yet — instead, it simulates detection with random choices for demonstration purposes. You can easily plug in a real model into the detect_emotion(image) function.


🙋‍♀️ Contributor
Developed with ❤️ by @Sanskriti10247
As part of GirlScript Summer of Code 2025

📄 License
This project is licensed under the MIT License.
