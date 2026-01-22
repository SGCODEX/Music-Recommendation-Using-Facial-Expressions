# Music Recommendation Using Facial Expressions

A system that suggests music based on your real-time facial expressions. This project uses computer vision and deep learning to detect emotions (Happy, Sad, Angry, Neutral, etc.) and plays a suitable song from YouTube.

## Features

*   **Real-time Emotion Detection**: Uses a trained deep learning model (Mini-XCEPTION) to detect facial expressions from your webcam.
*   **Music Recommendation**: Automatically searches and plays a song on YouTube based on the detected mood.
*   **Multiple Interfaces**:
    *   **CLI**: A lightweight command-line interface.
    *   **Streamlit Web App**: A user-friendly web interface with live visualization.
    *   **PySimpleGUI**: A desktop GUI application (legacy).

## Project Structure

```
code/
├── deployment/             # deployment related files
├── model/                  # Pre-trained emotion detection models
├── new_models/             # Newer model experiments and docs
├── ui_interfaces/          # Application entry points (CLI, Streamlit, etc.)
├── requirements.txt        # Project dependencies
└── README.md               # This file
```

## Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions.git
    cd Music-Recommendation-Using-Facial-Expressions/code
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    # Linux/Mac
    source venv/bin/activate
    # Windows
    venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Command Line Interface (CLI)

Run the simple CLI version:

```bash
python ui_interfaces/cli_main.py
```

*   A window will open showing your webcam feed.
*   Click inside the window to capture your emotion.
*   The script will detect the emotion and open a relevant YouTube song in your browser.
*   Press `q` to quit.

### Streamlit Web App

Run the interactive web application:

```bash
streamlit run ui_interfaces/app_local_streamlit.py
```

*   Opens in your default browser.
*   Displays live emotion detection statistics and a video feed.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License
