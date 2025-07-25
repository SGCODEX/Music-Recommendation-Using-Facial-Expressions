import gradio as gr
import random

# Dummy function to simulate emotion detection
def detect_emotion(image):
    emotions = ['happy', 'sad', 'angry', 'neutral', 'surprised']
    detected_emotion = random.choice(emotions)
    return detected_emotion

# Function to recommend music based on emotion
def recommend_music(image):
    emotion = detect_emotion(image)
    
    playlist_map = {
        'happy': '🎵 Happy Hits Playlist',
        'sad': '💧 Soft & Sad Songs',
        'angry': '🔥 Chill & Calm Instrumentals',
        'neutral': '🎧 Lo-Fi Beats',
        'surprised': '🚀 Latest Trending Songs',
    }

    recommendation = playlist_map.get(emotion, "🎶 Top Songs")
    return f"🧠 Detected Emotion: {emotion.capitalize()}\n\n🎶 Music Recommendation: {recommendation}"

# Gradio Interface
demo = gr.Interface(
    fn=recommend_music,
    inputs=gr.Image(type="pil", label="📸 Upload or Capture an Image"),
    outputs=gr.Textbox(label="🎼 Your Personalized Music Suggestion"),
    title="🎵 Emotion-based Music Recommendation",
    description=(
        "👋 Welcome! Upload your image or take a webcam photo.\n\n"
        "We'll try to guess your emotion and suggest music tailored just for you! 🎧💖"
    ),
    theme="soft",  # using Gradio's soft theme
    allow_flagging="never"
)

if __name__ == "__main__":
    demo.launch()
